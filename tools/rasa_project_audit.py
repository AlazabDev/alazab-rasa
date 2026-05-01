import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except Exception as e:
    print("ERROR: PyYAML غير مثبت داخل البيئة الحالية.")
    print("نفذ: pip install pyyaml")
    sys.exit(2)

ROOT = Path.cwd()

EXCLUDED_DIRS = {
    ".git", ".venv", "node_modules", "dist", "build", "__pycache__",
    ".rasa", ".mypy_cache", ".pytest_cache", "models", "logs"
}

SCAN_DIRS = [
    ROOT / "data",
    ROOT / "domain",
]

ROOT_YAML_FILES = [
    ROOT / "domain.yml",
    ROOT / "config.yml",
    ROOT / "credentials.yml",
    ROOT / "endpoints.yml",
]

issues = []
flow_locations = {}
response_locations = {}
declared_actions = set()
used_actions = []
yaml_docs = []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path)


def add(severity, code, file, message, flow=None, step=None):
    issues.append({
        "severity": severity,
        "code": code,
        "file": rel(file) if file else None,
        "flow": flow,
        "step": step,
        "message": message,
    })


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def yaml_files():
    files = []
    for base in SCAN_DIRS:
        if base.exists():
            for p in list(base.rglob("*.yml")) + list(base.rglob("*.yaml")):
                if not is_excluded(p):
                    files.append(p)

    for p in ROOT_YAML_FILES:
        if p.exists() and not is_excluded(p):
            files.append(p)

    return sorted(set(files))


def load_yaml(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")

    try:
        data = yaml.safe_load(text)
        return data if data else {}
    except Exception as e:
        add("ERROR", "YAML_PARSE_ERROR", path, f"YAML غير صالح: {e}")
        return None


def collect_metadata(path: Path, data):
    if not isinstance(data, dict):
        return

    flows = data.get("flows")
    if isinstance(flows, dict):
        for flow_id in flows.keys():
            flow_locations.setdefault(flow_id, []).append(path)

    responses = data.get("responses")
    if isinstance(responses, dict):
        for response_id in responses.keys():
            response_locations.setdefault(response_id, []).append(path)

    actions = data.get("actions")
    if isinstance(actions, list):
        for action in actions:
            if isinstance(action, str):
                declared_actions.add(action)


def action_target_from_step(step):
    if not isinstance(step, dict):
        return None

    for key in ("action", "collect"):
        val = step.get(key)
        if isinstance(val, str):
            return val

    return None


def validate_next_target(path, flow_id, step_id, target, step_ids):
    if target is None:
        add("ERROR", "NULL_NEXT", path, "next: null غير صالح. استخدم END.", flow_id, step_id)
        return

    if not isinstance(target, str):
        add("ERROR", "BAD_NEXT_TARGET", path, f"قيمة next/then يجب أن تكون نصًا. القيمة الحالية: {target!r}", flow_id, step_id)
        return

    if target == "END":
        return

    if target not in step_ids:
        add(
            "ERROR",
            "MISSING_STEP_REFERENCE",
            path,
            f"الخطوة تشير إلى '{target}' لكنها غير موجودة داخل نفس الـ flow. لا تستخدم خطوة من Flow آخر.",
            flow_id,
            step_id,
        )


def validate_next_block(path, flow_id, step_id, next_block, step_ids):
    if next_block is None:
        add("ERROR", "NULL_NEXT", path, "next: null غير صالح. استخدم END.", flow_id, step_id)
        return

    if isinstance(next_block, str):
        validate_next_target(path, flow_id, step_id, next_block, step_ids)
        return

    if isinstance(next_block, list):
        for idx, branch in enumerate(next_block, start=1):
            branch_id = f"{step_id}.branch[{idx}]"

            if not isinstance(branch, dict):
                add("ERROR", "BAD_NEXT_BRANCH", path, f"فرع next يجب أن يكون object وليس {type(branch).__name__}.", flow_id, branch_id)
                continue

            if "condition" in branch:
                add(
                    "ERROR",
                    "OLD_FLOW_CONDITION_SYNTAX",
                    path,
                    "استخدمت condition. الصحيح في Rasa Pro Flows هو if/then/else.",
                    flow_id,
                    branch_id,
                )

            if "next" in branch:
                add(
                    "ERROR",
                    "OLD_FLOW_NEXT_SYNTAX",
                    path,
                    "استخدمت next داخل فرع شرطي. الصحيح هو then.",
                    flow_id,
                    branch_id,
                )

            has_if = "if" in branch
            has_else = "else" in branch
            has_then = "then" in branch

            if not has_if and not has_else:
                add(
                    "ERROR",
                    "BAD_BRANCH_CONDITION",
                    path,
                    "فرع next يجب أن يحتوي if أو else.",
                    flow_id,
                    branch_id,
                )

            if has_if and not has_then:
                add(
                    "ERROR",
                    "MISSING_THEN",
                    path,
                    "فرع if يجب أن يحتوي then.",
                    flow_id,
                    branch_id,
                )

            if has_else:
                validate_next_target(path, flow_id, branch_id, branch.get("else"), step_ids)

            if has_then:
                validate_next_target(path, flow_id, branch_id, branch.get("then"), step_ids)

            condition = branch.get("if")
            if isinstance(condition, str):
                bare_slot_patterns = re.findall(r"\b(?!intent\b|slots\b|true\b|false\b|null\b)([a-zA-Z_][a-zA-Z0-9_]*)\b", condition)
                suspicious = []
                for token in bare_slot_patterns:
                    if token not in {"and", "or", "not", "in"} and f'"{token}"' not in condition and f"'{token}'" not in condition:
                        if token not in {"affirm", "deny"}:
                            suspicious.append(token)

                if suspicious and "slots." not in condition and "intent" not in condition:
                    add(
                        "WARNING",
                        "POSSIBLE_BARE_SLOT_CONDITION",
                        path,
                        f"الشرط قد يستخدم slot بدون slots.: {condition}",
                        flow_id,
                        branch_id,
                    )

        return

    add("ERROR", "BAD_NEXT_BLOCK", path, f"next يجب أن يكون نص أو قائمة شروط. النوع الحالي: {type(next_block).__name__}", flow_id, step_id)


def validate_flows(path: Path, data):
    if not isinstance(data, dict):
        return

    flows = data.get("flows")
    if not flows:
        return

    if not isinstance(flows, dict):
        add("ERROR", "BAD_FLOWS_BLOCK", path, "flows يجب أن تكون object.", None, None)
        return

    for flow_id, flow_def in flows.items():
        if not isinstance(flow_def, dict):
            add("ERROR", "BAD_FLOW_DEF", path, "تعريف flow يجب أن يكون object.", flow_id, None)
            continue

        steps = flow_def.get("steps")
        if not isinstance(steps, list):
            add("ERROR", "BAD_STEPS_BLOCK", path, "steps يجب أن تكون list.", flow_id, None)
            continue

        step_ids = set()
        step_id_count = {}

        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                add("ERROR", "BAD_STEP", path, f"الخطوة رقم {index} ليست object.", flow_id, f"index:{index}")
                continue

            step_id = step.get("id") or f"index:{index}"

            if "id" in step:
                step_id_count[step["id"]] = step_id_count.get(step["id"], 0) + 1
                step_ids.add(step["id"])

            target_action = action_target_from_step(step)
            if target_action:
                used_actions.append((path, flow_id, step_id, target_action))

            if set(step.keys()) == {"next"}:
                add(
                    "ERROR",
                    "NEXT_AS_STANDALONE_STEP",
                    path,
                    "next مكتوبة كخطوة منفصلة. يجب وضعها داخل نفس خطوة action/collect.",
                    flow_id,
                    step_id,
                )

        for sid, count in step_id_count.items():
            if count > 1:
                add("ERROR", "DUPLICATE_STEP_ID", path, f"Step id مكرر داخل نفس flow: {sid}", flow_id, sid)

        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                continue
            step_id = step.get("id") or f"index:{index}"

            if "next" in step:
                validate_next_block(path, flow_id, step_id, step.get("next"), step_ids)


def run_command(name, cmd):
    print(f"\n=== RUN: {name} ===")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        out = proc.stdout or ""
        report_file = ROOT / "reports" / f"{name}.log"
        report_file.write_text(out, encoding="utf-8")
        print(out[-4000:])
        if proc.returncode != 0:
            add("ERROR", "COMMAND_FAILED", report_file, f"الأمر فشل: {cmd} | exit={proc.returncode}")
        return proc.returncode
    except subprocess.TimeoutExpired:
        add("ERROR", "COMMAND_TIMEOUT", None, f"الأمر استغرق وقتًا طويلًا وتوقف: {cmd}")
        return 124
    except Exception as e:
        add("ERROR", "COMMAND_ERROR", None, f"تعذر تشغيل الأمر: {cmd} | {e}")
        return 1


def python_compile_check():
    targets = []
    for base in [ROOT / "actions", ROOT / "webhook"]:
        if base.exists():
            targets += [p for p in base.rglob("*.py") if not is_excluded(p)]

    if not targets:
        return

    for p in targets:
        cmd = f'"{sys.executable}" -m py_compile "{p}"'
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(ROOT),
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=60,
            )
            if proc.returncode != 0:
                add("ERROR", "PYTHON_COMPILE_ERROR", p, proc.stdout.strip())
        except Exception as e:
            add("ERROR", "PYTHON_COMPILE_ERROR", p, str(e))


def main():
    (ROOT / "reports").mkdir(exist_ok=True)
    files = yaml_files()

    print(f"Project: {ROOT}")
    print(f"YAML files scanned: {len(files)}")

    for path in files:
        data = load_yaml(path)
        if data is None:
            continue
        yaml_docs.append((path, data))
        collect_metadata(path, data)

    for flow_id, locations in flow_locations.items():
        if len(locations) > 1:
            add(
                "ERROR",
                "DUPLICATE_FLOW_ID",
                locations[0],
                "Flow ID مكرر في: " + ", ".join(rel(p) for p in locations),
                flow_id,
                None,
            )

    for response_id, locations in response_locations.items():
        if len(locations) > 1:
            add(
                "WARNING",
                "DUPLICATE_RESPONSE",
                locations[0],
                "Response مكرر في: " + ", ".join(rel(p) for p in locations),
                None,
                response_id,
            )

    for path, data in yaml_docs:
        validate_flows(path, data)

    all_responses = set(response_locations.keys())

    for path, flow_id, step_id, action_name in used_actions:
        if action_name.startswith("utter_"):
            if action_name not in all_responses:
                add(
                    "ERROR",
                    "MISSING_RESPONSE",
                    path,
                    f"الـ response غير معرّف: {action_name}",
                    flow_id,
                    step_id,
                )
        elif action_name.startswith("action_"):
            if action_name not in declared_actions:
                add(
                    "WARNING",
                    "CUSTOM_ACTION_NOT_DECLARED",
                    path,
                    f"الأكشن مستخدم لكنه غير موجود في actions: {action_name}",
                    flow_id,
                    step_id,
                )

    python_compile_check()

    if (ROOT / "domain.yml").exists() and (ROOT / "data").exists():
        run_command(
            "rasa-data-validate",
            'rasa data validate --domain ".\\domain.yml" --data ".\\data"',
        )

    package_json = ROOT / "azabot" / "package.json"
    if package_json.exists():
        run_command(
            "azabot-pnpm-build-check",
            'cd ".\\azabot" && pnpm run build',
        )

    severity_rank = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    issues_sorted = sorted(issues, key=lambda x: (severity_rank.get(x["severity"], 9), x["file"] or "", x["code"]))

    json_report = ROOT / "reports" / "rasa-project-audit.json"
    txt_report = ROOT / "reports" / "rasa-project-audit.txt"

    json_report.write_text(
        json.dumps({
            "project": str(ROOT),
            "total_issues": len(issues_sorted),
            "errors": sum(1 for i in issues_sorted if i["severity"] == "ERROR"),
            "warnings": sum(1 for i in issues_sorted if i["severity"] == "WARNING"),
            "issues": issues_sorted,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = []
    lines.append(f"PROJECT: {ROOT}")
    lines.append(f"TOTAL ISSUES: {len(issues_sorted)}")
    lines.append(f"ERRORS: {sum(1 for i in issues_sorted if i['severity'] == 'ERROR')}")
    lines.append(f"WARNINGS: {sum(1 for i in issues_sorted if i['severity'] == 'WARNING')}")
    lines.append("")

    for i, item in enumerate(issues_sorted, start=1):
        lines.append(f"{i}. [{item['severity']}] {item['code']}")
        lines.append(f"   FILE: {item['file']}")
        if item.get("flow"):
            lines.append(f"   FLOW: {item['flow']}")
        if item.get("step"):
            lines.append(f"   STEP: {item['step']}")
        lines.append(f"   MSG : {item['message']}")
        lines.append("")

    txt_report.write_text("\n".join(lines), encoding="utf-8")

    print("\n================ AUDIT SUMMARY ================")
    print(f"Errors  : {sum(1 for i in issues_sorted if i['severity'] == 'ERROR')}")
    print(f"Warnings: {sum(1 for i in issues_sorted if i['severity'] == 'WARNING')}")
    print(f"Report  : {rel(txt_report)}")
    print(f"JSON    : {rel(json_report)}")

    if issues_sorted:
        print("\nأول 20 مشكلة:")
        for item in issues_sorted[:20]:
            print(f"- [{item['severity']}] {item['code']} | {item['file']} | {item['message']}")

    sys.exit(1 if any(i["severity"] == "ERROR" for i in issues_sorted) else 0)


if __name__ == "__main__":
    main()
