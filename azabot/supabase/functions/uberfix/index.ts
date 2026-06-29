import { createClient } from "https://esm.sh/@supabase/supabase-js@2.95.0";
import { handleCors } from "../_shared/cors.ts";
import { jsonResponse, errorResponse, flatten } from "../_shared/utils.ts";
const TRACK_BASE = Deno.env.get("UBERFIX_TRACK_BASE_URL") || "https://uberfix.shop/track";
const API_KEY = Deno.env.get("UBERFIX_API_KEY") || Deno.env.get("MAINTENANCE_API_KEY") || "";
const sb = createClient(Deno.env.get("SUPABASE_URL"), Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"));
function ok(data) {
  return jsonResponse({
    success: true,
    ...flatten(data)
  });
}
function err(msg, s = 400) {
  return errorResponse(msg, s);
}
function genTicket() {
  const d = new Date();
  const ymd = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}`;
  const rand = Math.floor(Math.random() * 9000) + 1000;
  return `UBF-${ymd}-${rand}`;
}
function publicRequest(r) {
  return {
    id: r.id,
    request_number: r.request_number || r.ticket_number,
    status: r.status,
    title: r.title,
    description: r.description,
    service_type: r.service_type || r.fault_category,
    priority: r.priority || r.maintenance_priority,
    client_name: r.client_name,
    client_phone: r.client_phone,
    location: r.location,
    track_url: r.track_url,
    created_at: r.created_at,
    updated_at: r.updated_at
  };
}
function verifyKey(req) {
  if (!API_KEY) return true; // dev mode
  const k = req.headers.get("x-api-key") || req.headers.get("authorization")?.replace("Bearer ", "");
  return k === API_KEY;
}
// ── Actions ───────────────────────────────────────────────────
async function createRequest(payload, sessionId) {
  const { client_name, client_phone, description, service_type, priority, location, channel } = payload;
  if (!client_name) return err("client_name مطلوب");
  if (!client_phone) return err("client_phone مطلوب");
  if (!description) return err("description مطلوب");
  const ticket = genTicket();
  const trackUrl = `${TRACK_BASE}/${ticket}`;
  const { data, error } = await sb.from("maintenance_requests").insert({
    ticket_number: ticket,
    session_id: sessionId,
    client_name: String(client_name).slice(0, 120),
    client_phone: String(client_phone).slice(0, 40),
    description: String(description).slice(0, 1000),
    title: payload.title || String(description).slice(0, 120),
    fault_category: service_type || "other",
    maintenance_priority: [
      "low",
      "medium",
      "high",
      "urgent"
    ].includes(String(priority)) ? priority : "medium",
    location: location || "غير محدد",
    track_url: trackUrl,
    channel: channel || "bot_gateway",
    status: "new",
    metadata: payload.metadata || {}
  }).select().single();
  if (error) {
    console.error("create_request error:", error);
    return err("خطأ في إنشاء الطلب", 500);
  }
  await sb.from("bot_gateway_audit_logs").insert({
    action: "BOT_CREATE_REQUEST",
    entity_type: "maintenance_request",
    entity_id: data.id,
    new_data: data,
    metadata: {
      session_id: sessionId
    }
  }).catch(()=>{});
  return ok({
    message: `تم إنشاء الطلب بنجاح. رقم التتبع: ${ticket}`,
    request_id: data.id,
    request_number: ticket,
    tracking_number: ticket,
    track_url: trackUrl,
    data: publicRequest(data)
  });
}
async function checkStatus(payload) {
  const ref = payload.request_number || payload.request_id || payload.tracking_number;
  if (!ref) return err("request_number أو request_id مطلوب");
  const { data, error } = await sb.from("maintenance_requests").select("*").or(`ticket_number.eq.${ref},id.eq.${ref}`).maybeSingle();
  if (error || !data) return err("الطلب غير موجود", 404);
  const statusMap = {
    new: "جديد — جارٍ المراجعة",
    assigned: "تم تعيين فني",
    in_progress: "جارٍ التنفيذ",
    completed: "مكتمل",
    cancelled: "ملغي"
  };
  return ok({
    request_id: data.id,
    request_number: data.ticket_number,
    status: data.status,
    status_label: statusMap[data.status] || data.status,
    track_url: data.track_url,
    data: publicRequest(data),
    text: `حالة الطلب ${data.ticket_number}: ${statusMap[data.status] || data.status}`
  });
}
async function updateRequest(payload) {
  const id = payload.request_id || payload.id;
  if (!id) return err("request_id مطلوب");
  const allowed = [
    "status",
    "title",
    "description",
    "location",
    "fault_category",
    "maintenance_priority",
    "metadata"
  ];
  const patch = {};
  for (const k of allowed)if (k in payload) patch[k] = payload[k];
  if (!Object.keys(patch).length) return err("لا توجد حقول للتحديث");
  const { data, error } = await sb.from("maintenance_requests").update(patch).eq("id", id).select().single();
  if (error || !data) return err("الطلب غير موجود أو خطأ في التحديث", 404);
  return ok({
    message: "تم التحديث",
    data: publicRequest(data)
  });
}
async function cancelRequest(payload) {
  const id = payload.request_id || payload.id;
  if (!id) return err("request_id مطلوب");
  const { data, error } = await sb.from("maintenance_requests").update({
    status: "cancelled",
    metadata: {
      cancel_reason: payload.reason || "cancelled by bot"
    }
  }).eq("id", id).select().single();
  if (error || !data) return err("الطلب غير موجود", 404);
  return ok({
    message: `تم إلغاء الطلب ${data.ticket_number}`
  });
}
async function addNote(payload) {
  const id = payload.request_id || payload.id;
  const note = payload.note || payload.text;
  if (!id || !note) return err("request_id والـ note مطلوبان");
  const { data: current } = await sb.from("maintenance_requests").select("metadata").eq("id", id).single();
  const notes = current?.metadata?.notes || [];
  notes.push({
    text: note,
    created_at: new Date().toISOString(),
    source: "bot"
  });
  const { error } = await sb.from("maintenance_requests").update({
    metadata: {
      ...current?.metadata || {},
      notes
    }
  }).eq("id", id);
  if (error) return err("خطأ في إضافة الملاحظة", 500);
  return ok({
    message: "تمت إضافة الملاحظة"
  });
}
async function listCategories() {
  const categories = [
    {
      key: "electrical",
      label: "كهرباء",
      label_en: "Electrical"
    },
    {
      key: "plumbing",
      label: "سباكة",
      label_en: "Plumbing"
    },
    {
      key: "hvac",
      label: "تكييف وتهوية",
      label_en: "HVAC"
    },
    {
      key: "carpentry",
      label: "نجارة",
      label_en: "Carpentry"
    },
    {
      key: "painting",
      label: "دهانات",
      label_en: "Painting"
    },
    {
      key: "cleaning",
      label: "تنظيف",
      label_en: "Cleaning"
    },
    {
      key: "structural",
      label: "أعمال مدنية",
      label_en: "Structural"
    },
    {
      key: "other",
      label: "أخرى",
      label_en: "Other"
    }
  ];
  return ok({
    categories,
    text: "أنواع خدمات الصيانة المتاحة"
  });
}
async function listServices() {
  const services = [
    {
      key: "emergency_repair",
      label: "إصلاح طارئ",
      category: "general"
    },
    {
      key: "preventive",
      label: "صيانة دورية",
      category: "general"
    },
    {
      key: "inspection",
      label: "فحص وتقييم",
      category: "general"
    },
    {
      key: "installation",
      label: "تركيب جديد",
      category: "general"
    },
    {
      key: "ac_service",
      label: "خدمة تكييف",
      category: "hvac"
    },
    {
      key: "plumbing_leak",
      label: "إصلاح تسرب مياه",
      category: "plumbing"
    },
    {
      key: "electrical_fault",
      label: "إصلاح عطل كهربائي",
      category: "electrical"
    }
  ];
  return ok({
    services
  });
}
async function getBranches(payload) {
  const { data } = await sb.from("projects").select("id, name, location").limit(20).order("name");
  if (!data?.length) {
    return ok({
      branches: [
        {
          name: "المقر الرئيسي",
          location: "القاهرة"
        }
      ]
    });
  }
  return ok({
    branches: data
  });
}
async function assignTechnician(payload) {
  const id = payload.request_id || payload.id;
  const tech = payload.technician_name || payload.technician_id;
  if (!id) return err("request_id مطلوب");
  const { data, error } = await sb.from("maintenance_requests").update({
    status: "assigned",
    metadata: {
      technician: tech,
      assigned_at: new Date().toISOString()
    }
  }).eq("id", id).select().single();
  if (error || !data) return err("خطأ في تعيين الفني", 500);
  return ok({
    message: `تم تعيين الفني للطلب ${data.ticket_number}`
  });
}
async function transitionStage(payload) {
  const id = payload.request_id || payload.request_number || payload.id;
  const toStage = payload.to_stage || payload.status;
  if (!id || !toStage) return err("request_id و to_stage مطلوبان");
  const validStages = [
    "new",
    "assigned",
    "in_progress",
    "completed",
    "cancelled"
  ];
  if (!validStages.includes(String(toStage))) return err(`مرحلة غير صحيحة: ${toStage}`);
  const { data, error } = await sb.from("maintenance_requests").update({
    status: toStage
  }).or(`id.eq.${id},ticket_number.eq.${id}`).select().single();
  if (error || !data) return err("الطلب غير موجود", 404);
  return ok({
    message: `تم تحديث حالة الطلب إلى ${toStage}`,
    data: publicRequest(data)
  });
}
async function getQuote(payload) {
  const { service_type } = payload;
  const priceMap = {
    electrical: {
      min: 200,
      max: 800,
      unit: "جنيه"
    },
    plumbing: {
      min: 150,
      max: 600,
      unit: "جنيه"
    },
    hvac: {
      min: 300,
      max: 1200,
      unit: "جنيه"
    },
    carpentry: {
      min: 250,
      max: 1000,
      unit: "جنيه"
    },
    painting: {
      min: 15,
      max: 50,
      unit: "جنيه/م²"
    },
    cleaning: {
      min: 300,
      max: 800,
      unit: "جنيه"
    },
    other: {
      min: 200,
      max: 1000,
      unit: "جنيه"
    }
  };
  const key = String(service_type || "other");
  const price = priceMap[key] || priceMap.other;
  return ok({
    service_type: key,
    estimate_min: price.min,
    estimate_max: price.max,
    unit: price.unit,
    text: `تقدير سعر ${key}: ${price.min}–${price.max} ${price.unit} (تقديري — يتحدد بعد المعاينة)`
  });
}
// ── Main Handler ──────────────────────────────────────────────
Deno.serve(async (req)=>{
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;
  if (!verifyKey(req)) return err("Unauthorized", 401);
  let body = {};
  try {
    body = await req.json();
  } catch  {
    body = {};
  }
  const action = String(body.action || "");
  const payload = body.payload || body;
  const sessionId = String(body.session_id || payload.session_id || "");
  switch(action){
    case "create_request":
      return await createRequest(payload, sessionId);
    case "check_status":
      return await checkStatus(payload);
    case "update_request":
      return await updateRequest(payload);
    case "cancel_request":
      return await cancelRequest(payload);
    case "add_note":
      return await addNote(payload);
    case "assign_technician":
      return await assignTechnician(payload);
    case "list_categories":
      return await listCategories();
    case "list_services":
      return await listServices();
    case "get_branches":
      return await getBranches(payload);
    case "transition_stage":
      return await transitionStage(payload);
    case "get_quote":
      return await getQuote(payload);
    default:
      return err(`action غير معروف: ${action}`);
  }
});
