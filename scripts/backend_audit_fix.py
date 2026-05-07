from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIRS = [
    ROOT / "actions",
    ROOT / "webhook",
    ROOT / "scripts",
    ROOT / "deploy" / "production",
]

TEXT_EXTENSIONS = {
    ".py",
    ".yml",
    ".yaml",
    ".sh",
    ".ps1",
    ".toml",
    ".ini",
    ".env",
    ".example",
    ".txt",
    ".md",
}

SECRET_SCAN_EXTENSIONS = {
    ".py",
    ".sh",
    ".ps1",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".env",
}

SKIP_SECRET_SCAN_FILES = {
    "first-deploy.example.sh",
    "server-setup.md",
}


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str


def is_text_candidate(path: Path) -> bool:
    if path.suffix in TEXT_EXTENSIONS:
        return True
    name = path.name.lower()
    return name.endswith(".env.example") or name.endswith(".env")


def iter_files(base_dirs: Iterable[Path]) -> Iterable[Path]:
    for base in base_dirs:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                yield path


def scan_hardcoded_secrets(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings

    assign_pattern = re.compile(
        r"(?i)\b(api[_-]?key|x-api-key|secret|token|password)\b\s*[:=]\s*[\"']([^\"']{4,})[\"']"
    )

    for match in assign_pattern.finditer(content):
        value = match.group(2).strip()
        value_l = value.lower()
        if any(
            marker in value_l
            for marker in (
                "change-me",
                "your_",
                "your-",
                "your ",
                "example",
                "placeholder",
                "xxxx",
                "todo",
            )
        ):
            continue
        if "${" in value or "$(" in value:
            continue
        if len(value) < 8:
            continue

        key_name = match.group(1).lower()
        if "api" in key_name:
            msg = "possible hardcoded api key"
        elif "x-api-key" in key_name:
            msg = "possible hardcoded x-api-key"
        else:
            msg = "possible hardcoded secret"

        findings.append(
            Finding(
                severity="high",
                code="secret-leak",
                path=str(path),
                message=msg,
            )
        )
    return findings


def scan_wildcard_cors(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if path.name == "backend_audit_fix.py":
        return findings
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings

    if "--cors \"*\"" in content or "--cors '*'" in content:
        findings.append(
            Finding(
                severity="high",
                code="wildcard-cors",
                path=str(path),
                message="wildcard cors detected",
            )
        )

    if re.search(r"allow_origins\s*=\s*\[\s*[\"']\*[\"']\s*\]", content):
        findings.append(
            Finding(
                severity="high",
                code="wildcard-cors",
                path=str(path),
                message="FastAPI wildcard CORS detected",
            )
        )

    return findings


def scan_required_files() -> list[Finding]:
    findings: list[Finding] = []
    required = [
        ROOT / "actions" / "action_human_handoff.py",
        ROOT / "actions" / "action_submit_lead.py",
        ROOT / "actions" / "form_validation.py",
        ROOT / "actions" / "brand_actions" / "uberfix.py",
        ROOT / "actions" / "maintenance" / "service.py",
        ROOT / "actions" / "maintenance" / "gateway_client.py",
        ROOT / "actions" / "maintenance" / "schemas.py",
        ROOT / "actions" / "maintenance" / "responses.py",
        ROOT / "webhook" / "server.py",
        ROOT / "endpoints.yml",
    ]

    for path in required:
        if not path.exists():
            findings.append(
                Finding(
                    severity="critical",
                    code="missing-file",
                    path=str(path),
                    message="required backend file is missing",
                )
            )
    return findings


def scan_endpoints_file() -> list[Finding]:
    findings: list[Finding] = []
    endpoint_path = ROOT / "endpoints.yml"
    if not endpoint_path.exists():
        return findings

    content = endpoint_path.read_text(encoding="utf-8", errors="ignore")

    required_tokens = [
        "action_endpoint",
        "url:",
        "tracker_store",
        "lock_store",
    ]
    for token in required_tokens:
        if token not in content:
            findings.append(
                Finding(
                    severity="medium",
                    code="endpoints-missing-token",
                    path=str(endpoint_path),
                    message=f"missing token in endpoints config: {token}",
                )
            )
    return findings


def ensure_init_files(apply_fix: bool) -> list[Finding]:
    findings: list[Finding] = []
    actions_root = ROOT / "actions"
    if not actions_root.exists():
        return findings

    for path in actions_root.rglob("*"):
        if not path.is_dir():
            continue
        if path.name == "__pycache__":
            continue
        py_files = [p for p in path.glob("*.py")]
        if not py_files:
            continue
        init_file = path / "__init__.py"
        if init_file.exists():
            continue
        if apply_fix:
            init_file.write_text("", encoding="utf-8")
            findings.append(
                Finding(
                    severity="low",
                    code="fixed-missing-init",
                    path=str(init_file),
                    message="created missing __init__.py",
                )
            )
        else:
            findings.append(
                Finding(
                    severity="medium",
                    code="missing-init",
                    path=str(init_file),
                    message="python package folder without __init__.py",
                )
            )
    return findings


def cleanup_python_cache(apply_fix: bool) -> list[Finding]:
    findings: list[Finding] = []
    for base in BACKEND_DIRS:
        if not base.exists():
            continue
        for cache_dir in base.rglob("__pycache__"):
            if apply_fix:
                shutil.rmtree(cache_dir, ignore_errors=True)
                findings.append(
                    Finding(
                        severity="low",
                        code="fixed-pycache",
                        path=str(cache_dir),
                        message="removed __pycache__ directory",
                    )
                )
            else:
                findings.append(
                    Finding(
                        severity="low",
                        code="pycache-found",
                        path=str(cache_dir),
                        message="python cache directory should stay untracked",
                    )
                )
    return findings


def audit(apply_fix: bool) -> dict[str, object]:
    findings: list[Finding] = []
    findings.extend(scan_required_files())
    findings.extend(scan_endpoints_file())
    findings.extend(ensure_init_files(apply_fix=apply_fix))
    findings.extend(cleanup_python_cache(apply_fix=apply_fix))

    for path in iter_files(BACKEND_DIRS):
        if not is_text_candidate(path):
            continue
        if path.suffix in SECRET_SCAN_EXTENSIONS and path.name not in SKIP_SECRET_SCAN_FILES:
            findings.extend(scan_hardcoded_secrets(path))
        findings.extend(scan_wildcard_cors(path))

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda f: (severity_order.get(f.severity, 9), f.code, f.path))

    summary = {
        "total_findings": len(findings),
        "critical": sum(1 for f in findings if f.severity == "critical"),
        "high": sum(1 for f in findings if f.severity == "high"),
        "medium": sum(1 for f in findings if f.severity == "medium"),
        "low": sum(1 for f in findings if f.severity == "low"),
    }

    return {
        "summary": summary,
        "findings": [asdict(f) for f in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Backend audit and safe auto-fix")
    parser.add_argument("--apply", action="store_true", help="apply safe automatic fixes")
    parser.add_argument("--output", type=Path, default=None, help="write report json file")
    args = parser.parse_args()

    result = audit(apply_fix=args.apply)
    report = json.dumps(result, ensure_ascii=False, indent=2)
    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")

    summary = result["summary"]
    if summary["critical"] > 0 or summary["high"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
