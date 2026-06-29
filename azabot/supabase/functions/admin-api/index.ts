import { createClient } from "https://esm.sh/@supabase/supabase-js@2.95.0";
import { verifyJWT } from "../_shared/jwt.ts";
import { handleCors } from "../_shared/cors.ts";
import { jsonResponse, errorResponse } from "../_shared/utils.ts";
import { fireOne } from "../_shared/integrations.ts";
const SECRET = Deno.env.get("ADMIN_JWT_SECRET");
const supabase = createClient(Deno.env.get("SUPABASE_URL"), Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"));
async function requireAdmin(req) {
  const auth = req.headers.get("Authorization");
  if (!auth?.startsWith("Bearer ")) return false;
  const claims = await verifyJWT(auth.slice(7), SECRET);
  return claims?.role === "admin";
}
Deno.serve(async (req)=>{
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;
  if (!await requireAdmin(req)) return errorResponse("Unauthorized", 401);
  try {
    const url = new URL(req.url);
    const action = url.searchParams.get("action") || "";
    const body = req.method !== "GET" ? await req.json().catch(()=>({})) : {};
    switch(action){
      case "get_settings":
        {
          const { data } = await supabase.from("bot_settings").select("*").eq("id", 1).single();
          return jsonResponse(data);
        }
      case "update_settings":
        {
          const allowed = [
            "bot_name",
            "primary_color",
            "welcome_message",
            "quick_replies",
            "ai_model",
            "system_prompt",
            "voice_enabled",
            "voice_name",
            "auto_speak",
            "business_hours_enabled",
            "business_hours",
            "offline_message",
            "position"
          ];
          const patch = {};
          for (const k of allowed)if (k in body) patch[k] = body[k];
          const { data, error } = await supabase.from("bot_settings").update(patch).eq("id", 1).select().single();
          if (error) return errorResponse(error.message, 400);
          return jsonResponse(data);
        }
      case "list_integrations":
        {
          const { data } = await supabase.from("integrations").select("*").order("created_at", {
            ascending: false
          });
          return jsonResponse(data);
        }
      case "save_integration":
        {
          const { id, type, name, enabled, config, events } = body;
          if (id) {
            const { data, error } = await supabase.from("integrations").update({
              name,
              enabled,
              config,
              events
            }).eq("id", id).select().single();
            if (error) return errorResponse(error.message, 400);
            return jsonResponse(data);
          }
          const { data, error } = await supabase.from("integrations").insert({
            type,
            name,
            enabled: !!enabled,
            config: config || {},
            events: events || [
              "message.created"
            ]
          }).select().single();
          if (error) return errorResponse(error.message, 400);
          return jsonResponse(data);
        }
      case "delete_integration":
        {
          await supabase.from("integrations").delete().eq("id", body.id);
          return jsonResponse({
            ok: true
          });
        }
      case "test_integration":
        {
          const { data: integ } = await supabase.from("integrations").select("*").eq("id", body.id).single();
          if (!integ) return errorResponse("Integration not found", 404);
          const result = await fireOne(supabase, integ, "test.event", {
            message: "هذه رسالة اختبار من AzaBot 🚀",
            timestamp: new Date().toISOString()
          });
          return jsonResponse(result);
        }
      case "list_conversations":
        {
          const q = url.searchParams.get("q") || "";
          let query = supabase.from("conversations").select("*").order("last_message_at", {
            ascending: false
          }).limit(100);
          if (q) query = query.or(`visitor_name.ilike.%${q}%,visitor_email.ilike.%${q}%,session_id.ilike.%${q}%`);
          const { data } = await query;
          return jsonResponse(data);
        }
      case "get_conversation":
        {
          const id = url.searchParams.get("id");
          const { data: conv } = await supabase.from("conversations").select("*").eq("id", id).single();
          const { data: msgs } = await supabase.from("messages").select("*").eq("conversation_id", id).order("created_at");
          return jsonResponse({
            conversation: conv,
            messages: msgs
          });
        }
      case "delete_conversation":
        {
          await supabase.from("conversations").delete().eq("id", body.id);
          return jsonResponse({
            ok: true
          });
        }
      case "list_logs":
        {
          const { data } = await supabase.from("webhook_logs").select("*").order("created_at", {
            ascending: false
          }).limit(200);
          return jsonResponse(data);
        }
      case "stats":
        {
          const { count: convCount } = await supabase.from("conversations").select("*", {
            count: "exact",
            head: true
          });
          const { count: msgCount } = await supabase.from("messages").select("*", {
            count: "exact",
            head: true
          });
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          const { count: todayCount } = await supabase.from("conversations").select("*", {
            count: "exact",
            head: true
          }).gte("created_at", today.toISOString());
          return jsonResponse({
            conversations: convCount || 0,
            messages: msgCount || 0,
            today: todayCount || 0
          });
        }
      default:
        return errorResponse("Unknown action", 400);
    }
  } catch (e) {
    console.error("admin-api error:", e);
    return errorResponse(e instanceof Error ? e.message : "Unknown", 500);
  }
});
