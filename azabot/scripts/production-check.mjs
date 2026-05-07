import { existsSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));

const checks = [];
let failed = false;

function pass(message) {
  checks.push({ level: "OK", message });
}

function warn(message) {
  checks.push({ level: "WARN", message });
}

function fail(message) {
  failed = true;
  checks.push({ level: "FAIL", message });
}

function read(rel) {
  return readFileSync(join(root, rel), "utf8");
}

function exists(rel) {
  return existsSync(join(root, rel));
}

function size(rel) {
  return statSync(join(root, rel)).size;
}

function validateBuildOutput() {
  if (!exists("dist/index.html")) {
    fail("dist/index.html غير موجود. شغل pnpm build قبل فحص الإنتاج.");
    return;
  }

  const html = read("dist/index.html");
  if (!html.includes("/assets/")) {
    fail("dist/index.html لا يحتوي روابط assets مبنية.");
  } else {
    pass("ملفات dist موجودة ومربوطة بالـ assets.");
  }

  const assetsDir = join(root, "dist", "assets");
  if (!existsSync(assetsDir)) {
    fail("dist/assets غير موجود.");
  } else {
    pass("dist/assets موجود.");
  }
}

function validateFrontendRouting() {
  const config = read("src/lib/config.ts");
  const chatService = read("src/lib/chat-service.ts");
  const adminApi = read("src/lib/adminApi.ts");

  if (!config.includes("VITE_CHAT_API_URL") || !config.includes("window.location.origin")) {
    fail("src/lib/config.ts لا يوضح fallback إلى نفس الدومين.");
  } else {
    pass("إعداد API يستخدم VITE_CHAT_API_URL أو نفس دومين الواجهة.");
  }

  const expectedConfigKeys = ["chat:", "upload:", "audio:", "tts:"];
  for (const key of expectedConfigKeys) {
    if (!config.includes(key)) warn(`راجع إعداد ${key} داخل src/lib/config.ts.`);
  }

  if (!chatService.includes("responses?: unknown[]")) {
    warn("طبقة chat-service لا تبدو مضبوطة على شكل رد FastAPI الحالي.");
  } else {
    pass("chat-service متوافق مع ردود FastAPI /chat.");
  }

  if (!adminApi.includes("/admin/login") || !adminApi.includes("/admin/api")) {
    fail("adminApi لا يشير لمسارات الإدارة المتوقعة.");
  } else {
    pass("لوحة الإدارة تتصل بمسارات /admin/login و /admin/api.");
  }
}

function validateSupabaseSeparation() {
  const hasSupabase = exists("supabase/functions");
  const readme = read("README.md");

  if (!hasSupabase) {
    pass("لا يوجد مسار Supabase داخل الواجهة.");
    return;
  }

  if (!readme.includes("مسار Supabase")) {
    warn("يوجد Supabase Functions داخل المشروع، لكن README لا يوضح أنها مسار منفصل.");
  } else {
    pass("README يوضح فصل مسار Supabase عن مسار FastAPI.");
  }

  if (exists("supabase/migrations/20260428074048_init_schema.sql") && size("supabase/migrations/20260428074048_init_schema.sql") === 0) {
    warn("يوجد migration فارغ: supabase/migrations/20260428074048_init_schema.sql");
  }
}

function validatePackageManager() {
  if (!exists("pnpm-lock.yaml")) {
    fail("pnpm-lock.yaml غير موجود.");
  } else {
    pass("pnpm-lock.yaml موجود.");
  }

  if (exists("package-lock.json")) {
    warn("يوجد package-lock.json بجانب pnpm-lock.yaml. الأفضل الاعتماد على pnpm فقط لهذا المشروع.");
  }
}

function printChecks() {
  for (const item of checks) {
    const icon = item.level.padEnd(4);
    console.log(`[${icon}] ${item.message}`);
  }
}

validateBuildOutput();
validateFrontendRouting();
validateSupabaseSeparation();
validatePackageManager();

printChecks();

if (failed) {
  console.error("\nProduction check failed.");
  process.exit(1);
}

console.log("\nProduction check completed.");
