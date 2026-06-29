import { existsSync, readFileSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const checks = [];
let failed = false;

function mark(level, message) {
  checks.push({ level, message });
  if (level === "FAIL") failed = true;
}

function ok(message) {
  mark("OK", message);
}

function warn(message) {
  mark("WARN", message);
}

function fail(message) {
  mark("FAIL", message);
}

function pathOf(rel) {
  return join(root, rel);
}

function exists(rel) {
  return existsSync(pathOf(rel));
}

function read(rel) {
  return readFileSync(pathOf(rel), "utf8");
}

function nonEmpty(rel) {
  return exists(rel) && statSync(pathOf(rel)).size > 0;
}

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    shell: false,
    ...options,
  });
  return {
    ok: result.status === 0,
    status: result.status,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? "",
    error: result.error,
  };
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function containsTerm(text, term) {
  const normalized = text.toLowerCase();
  const escaped = escapeRegex(term.toLowerCase());
  const asciiOnly = /^[a-z0-9 ]+$/i.test(term);
  const boundary = asciiOnly ? "\\b" : "(?<![\\p{L}\\p{N}_])";
  const endBoundary = asciiOnly ? "\\b" : "(?![\\p{L}\\p{N}_])";
  return new RegExp(`${boundary}${escaped}${endBoundary}`, "iu").test(normalized);
}

function checkRequiredFiles() {
  const files = [
    "config.yml",
    "domain.yml",
    "endpoints.yml",
    "credentials.yml",
    "webhook/server.py",
    "azabot/package.json",
    "azabot/pnpm-lock.yaml",
    "azabot/src/lib/config.ts",
    "azabot/src/lib/chat-service.ts",
  ];

  for (const file of files) {
    if (nonEmpty(file)) ok(`${file} موجود`);
    else fail(`${file} مفقود أو فارغ`);
  }
}

function checkComposeMountedPaths() {
  for (const rel of ["docker/docker-compose.yaml", "docker/docker-compose.prod.yaml"]) {
    if (!exists(rel)) continue;
    const text = read(rel);
    const mountMatches = [...text.matchAll(/-\s+\.\.\/([^:\r\n]+):/g)].map((m) => m[1].trim());
    for (const mounted of mountMatches) {
      const target = mounted.replaceAll("/", "\\");
      if (exists(target)) ok(`${rel}: mount موجود ../${mounted}`);
      else fail(`${rel}: mount يشير لمسار غير موجود ../${mounted}`);
    }
  }
}

function checkFrontend() {
  if (!exists("azabot/dist/index.html")) {
    warn("azabot/dist/index.html غير موجود. شغل pnpm build قبل بناء صورة الإنتاج.");
    return;
  }

  const html = read("azabot/dist/index.html");
  if (html.includes("/assets/")) ok("واجهة azabot مبنية وفيها assets");
  else fail("azabot/dist/index.html لا يشير إلى assets");

  const config = read("azabot/src/lib/config.ts");
  const service = read("azabot/src/lib/chat-service.ts");
  const admin = read("azabot/src/lib/adminApi.ts");

  if (config.includes("VITE_CHAT_API_URL") && config.includes("window.location.origin")) {
    ok("إعدادات الواجهة تدعم نفس الدومين أو VITE_CHAT_API_URL");
  } else {
    fail("إعدادات الواجهة لا تحتوي fallback واضح للـ API origin");
  }

  for (const endpoint of ["chat", "upload", "audio", "tts"]) {
    if (config.includes(`${endpoint}:`)) ok(`واجهة API تحتوي ${endpoint}`);
    else fail(`واجهة API لا تحتوي ${endpoint}`);
  }

  if (service.includes("responses?: unknown[]")) ok("chat-service متوافق مع رد /chat الحالي");
  else warn("راجع توافق chat-service مع رد /chat");

  if (admin.includes("/admin/login") && admin.includes("/admin/api")) {
    ok("لوحة الإدارة متصلة بمسارات FastAPI المتوقعة");
  } else {
    fail("لوحة الإدارة لا تشير لمسارات /admin/login و /admin/api");
  }
}

function checkWebhookRoutes() {
  const text = read("webhook/server.py");
  const routes = [
    '@app.get("/health"',
    '@app.get("/brands"',
    '@app.post("/chat"',
    '@app.post("/chat/upload"',
    '@app.post("/chat/audio"',
    '@app.post("/chat/tts"',
    '@app.post("/admin/login"',
    '@app.api_route("/admin/api"',
  ];

  for (const route of routes) {
    if (text.includes(route)) ok(`FastAPI route موجود: ${route}`);
    else fail(`FastAPI route مفقود: ${route}`);
  }

  if (text.includes("FRONTEND_DIST_DIR") && text.includes("azabot")) {
    ok("FastAPI يعرف مسار azabot/dist");
  } else {
    fail("FastAPI لا يوضح مسار خدمة الواجهة المبنية");
  }
}

function checkBackendSafety() {
  const webhook = read("webhook/server.py");
  const compose = exists("docker/docker-compose.yaml") ? read("docker/docker-compose.yaml") : "";
  const prodCompose = exists("docker/docker-compose.prod.yaml") ? read("docker/docker-compose.prod.yaml") : "";
  const domain = read("domain.yml");
  const labanAction = read("actions/brand_actions/laban_alasfour.py");
  const uberfixAction = read("actions/brand_actions/uberfix.py");

  if (webhook.includes("ADMIN_PASSWORD = os.getenv(\"ADMIN_PASSWORD\", \"\").strip()")) {
    ok("Admin password لا يحتوي قيمة افتراضية صلبة");
  } else {
    fail("ADMIN_PASSWORD يجب أن يأتي من البيئة فقط بدون قيمة افتراضية");
  }

  if (webhook.includes("ADMIN_SESSION_SECRET = os.getenv(\"ADMIN_SESSION_SECRET\", \"\").strip()")) {
    ok("Admin session secret لا يحتوي fallback قابل للتخمين");
  } else {
    fail("ADMIN_SESSION_SECRET يجب أن يأتي من البيئة فقط");
  }

  if (webhook.includes("os.replace(tmp_path, ADMIN_DATA_FILE)")) {
    ok("حفظ بيانات الإدارة يتم باستبدال ذري لتقليل تلف JSON");
  } else {
    fail("حفظ بيانات الإدارة ليس atomic وقد يفسد JSON تحت الضغط");
  }

  if (webhook.includes("_is_relative_to(file_path, UPLOADS_ROOT)")) {
    ok("تحميل ملفات الإدارة مقيد داخل UPLOADS_DIR");
  } else {
    fail("تحميل ملفات الإدارة لا يتحقق من بقاء المسار داخل UPLOADS_DIR");
  }

  if (webhook.includes("_is_internal_lead_notify_url(WEBHOOK_NOTIFY)")) {
    ok("FastAPI يمنع حلقة WEBHOOK_NOTIFY_URL عند الإشارة إلى /lead الداخلي");
  } else {
    fail("WEBHOOK_NOTIFY_URL قد يسبب حلقة إشعارات إذا أشار إلى /lead الداخلي");
  }

  if (webhook.includes("Meta app secret is not configured") && !webhook.includes("if META_SECRET and not _verify_meta_signature")) {
    ok("Meta webhook يرفض POST بدون FB_APP_SECRET وتوقيع صالح");
  } else {
    fail("Meta webhook يجب أن يرفض POST غير الموقع أو غير المضبوط");
  }

  if (webhook.includes("TG_WEBHOOK_SECRET") && webhook.includes("X-Telegram-Bot-Api-Secret-Token")) {
    ok("Telegram webhook محمي بـ secret token");
  } else {
    fail("Telegram webhook غير محمي بـ secret token");
  }

  if (webhook.includes("uuid.uuid4().hex[:10]")) {
    ok("أسماء الملفات المرفوعة تحتوي جزء فريد يمنع التصادم");
  } else {
    fail("أسماء الملفات المرفوعة قد تتصادم عند تكرار الاسم داخل نفس الثانية");
  }

  if (compose.includes("--cors \"*\"") || prodCompose.includes("--cors \"*\"")) {
    fail("Docker Compose يشغل Rasa بـ CORS مفتوح على *");
  } else if (compose || prodCompose) {
    ok("Docker Compose لا يشغل Rasa بـ CORS مفتوح");
  } else {
    ok("Docker غير مطلوب في مسار الإنتاج الحالي");
  }

  const submitLead = read("actions/action_submit_lead.py");
  if (submitLead.includes("LEAD_RECEIVER_URL") && !submitLead.includes("logger.info(f\"New lead: {lead_data}\"")) {
    ok("Action submit lead يفصل receiver الداخلي عن CRM webhook ولا يطبع بيانات العميل كاملة");
  } else {
    fail("action_submit_lead يحتاج فصل LEAD_RECEIVER_URL ومنع logging لبيانات العميل كاملة");
  }

  if (
    uberfixAction.includes("MaintenanceService")
    && !uberfixAction.includes("httpx")
    && !uberfixAction.includes("os.getenv")
    && exists("actions/maintenance/service.py")
    && exists("actions/maintenance/gateway_client.py")
    && exists("actions/maintenance/schemas.py")
  ) {
    ok("UberFix action معزول خلف طبقة maintenance service");
  } else {
    fail("UberFix action يجب أن يبقى رفيعاً والمنطق ينتقل إلى actions/maintenance");
  }

  const forbiddenBrandWords = [
    "ألبان العصفور",
    "جبن",
    "زبادي",
    "منتجات ألبان",
    "dairy",
    "milk",
    "cheese",
  ];
  const backendBrandText = [domain, labanAction, webhook].join("\n");
  const foundForbidden = forbiddenBrandWords.filter((word) => containsTerm(backendBrandText, word));
  if (foundForbidden.length) {
    fail(`محتوى الباك اند يحتوي وصف لبن العصفور كمنتجات غذائية: ${foundForbidden.join(", ")}`);
  } else {
    ok("محتوى الباك اند لا يخلط لبن العصفور بمنتجات ألبان");
  }
}

function checkRasaConsistency() {
  const dataPatterns = read("data/system/patterns/patterns.yml");
  const knownRasaProPatternActions = ["action_correct_flow_slot", "action_trigger_search"];
  for (const actionName of knownRasaProPatternActions) {
    if (dataPatterns.includes(`action: ${actionName}`)) {
      warn(`${actionName} موجود في Rasa Pro patterns؛ اعتبره built-in وراجعه فقط إذا فشل rasa train`);
    }
  }

  if (exists("data/brands/uberfix/storie.yml")) {
    warn("data/brands/uberfix/storie.yml اسمه غير قياسي؛ Rasa يقرأه كـ yml لكن يفضل تسميته stories.yml لاحقاً");
  } else {
    ok("لا توجد أسماء story غير قياسية في UberFix");
  }
}

function checkPythonSyntax() {
  const py = process.platform === "win32" ? "python" : "python3";
  const result = run(py, ["-m", "compileall", "actions", "webhook"]);
  if (result.ok) ok("Python syntax check مر بنجاح");
  else warn(`تعذر تشغيل Python syntax check: ${(result.stderr || result.stdout || result.error?.message || "").trim()}`);
}

function checkDocsConsistency() {
  const readme = read("README.md");
  if (readme.includes("chatbot-widget")) {
    fail("README ما زال يذكر chatbot-widget القديم");
  } else {
    ok("README لا يشير للمجلد القديم chatbot-widget");
  }

  if (readme.includes("webhook/static/widget")) ok("README يذكر مسار widget الحالي");
  else warn("README لا يذكر مسار widget الحالي");
}

function print() {
  for (const item of checks) {
    console.log(`[${item.level.padEnd(4)}] ${item.message}`);
  }
}

checkRequiredFiles();
checkComposeMountedPaths();
checkFrontend();
checkWebhookRoutes();
checkBackendSafety();
checkRasaConsistency();
checkPythonSyntax();
checkDocsConsistency();

print();

if (failed) {
  console.error("\nProduction readiness failed.");
  process.exit(1);
}

console.log("\nProduction readiness completed.");
