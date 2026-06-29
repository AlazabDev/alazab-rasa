import { createClient } from "https://esm.sh/@supabase/supabase-js@2.95.0";
import { handleCors, corsHeaders } from "../_shared/cors.ts";
import { errorResponse } from "../_shared/utils.ts";
import { dispatchAll } from "../_shared/integrations.ts";
const supabase = createClient(Deno.env.get("SUPABASE_URL"), Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"));
async function getBrandConfig(siteId, origin) {
  let query = supabase.from("brands").select("*");
  if (siteId) {
    query = query.eq("key", siteId);
  } else if (origin) {
    try {
      const hostname = new URL(origin).hostname;
      query = query.contains("domains", [
        hostname
      ]);
    } catch  {
      query = query.eq("key", "alazab");
    }
  } else {
    query = query.eq("key", "alazab");
  }
  const { data } = await query.limit(1).maybeSingle();
  if (data) return data;
  // Fallback to alazab
  const { data: fallback } = await supabase.from("brands").select("*").eq("key", "alazab").single();
  return fallback;
}
// ── Gemini / Lovable Gateway ─────────────────────────────────────────
async function callGeminiStream(systemContent, messages, conversationId, sessionId) {
  const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");
  if (!LOVABLE_API_KEY) throw new Error("LOVABLE_API_KEY missing");
  const response = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${LOVABLE_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "google/gemini-2.5-flash",
      messages: [
        {
          role: "system",
          content: systemContent
        },
        ...messages
      ],
      stream: true
    })
  });
  if (!response.ok) {
    if (response.status === 429) return errorResponse("تم تجاوز حد الطلبات، حاول لاحقاً.", 429);
    if (response.status === 402) return errorResponse("الرصيد غير كافٍ. يرجى إضافة رصيد لمساحة العمل.", 402);
    return errorResponse("AI gateway error", 500);
  }
  const [toClient, toCapture] = response.body.tee();
  captureAssistantReply(toCapture, conversationId, sessionId).catch(()=>{});
  return new Response(toClient, {
    headers: {
      ...corsHeaders,
      "Content-Type": "text/event-stream"
    }
  });
}
// ── Dialogflow Gateway ───────────────────────────────────────────────
async function callDialogflow(brand, messages, conversationId, sessionId) {
  const projectId = Deno.env.get("GCP_PROJECT_ID")?.trim();
  const agentId = Deno.env.get("DIALOGFLOW_AGENT_ID")?.trim();
  const location = Deno.env.get("GCP_LOCATION")?.trim() || "global";
  const accessToken = Deno.env.get("GCP_ACCESS_TOKEN")?.trim();
  if (!projectId || !agentId || !accessToken) throw new Error("DIALOGFLOW_CONFIG_MISSING");
  const lastUserMessage = [
    ...messages
  ].reverse().find((m)=>m.role === "user")?.content;
  if (!lastUserMessage) throw new Error("LAST_USER_MESSAGE_MISSING");
  const dfSessionId = crypto.randomUUID();
  const base = location === "global" ? "https://global-dialogflow.googleapis.com" : `https://${location}-dialogflow.googleapis.com`;
  const url = `${base}/v3/projects/${projectId}/locations/${location}/agents/${agentId}/sessions/${dfSessionId}:detectIntent`;
  const payload = {
    queryInput: {
      text: {
        text: `${brand.system_prompt}\n\nرسالة العميل:\n${lastUserMessage}`
      },
      languageCode: "ar"
    },
    queryParams: {
      parameters: {
        siteId: brand.key,
        siteName: brand.name,
        botPersona: brand.bot_persona
      }
    }
  };
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  const raw = await res.text();
  if (!res.ok) throw new Error(`Dialogflow error: ${raw}`);
  const data = JSON.parse(raw);
  const responseMessages = data.queryResult?.responseMessages;
  let reply = "";
  if (Array.isArray(responseMessages)) {
    for (const item of responseMessages){
      const texts = item?.text?.text;
      if (Array.isArray(texts) && typeof texts[0] === "string" && texts[0].trim()) {
        reply = texts[0].trim();
        break;
      }
    }
  }
  if (!reply) {
    const displayName = data.queryResult?.match?.intent?.displayName;
    if (typeof displayName === "string" && displayName.trim()) reply = displayName.trim();
  }
  if (!reply) throw new Error("DIALOGFLOW_EMPTY_RESPONSE");
  // Save reply to DB if we have a conversationId
  if (conversationId && reply) {
    await supabase.from("messages").insert({
      conversation_id: conversationId,
      role: "assistant",
      content: reply
    });
    dispatchAll(supabase, "message.created", {
      conversation_id: conversationId,
      session_id: sessionId,
      role: "assistant",
      content: reply
    }).catch(()=>{});
  }
  return new Response(JSON.stringify({
    reply,
    siteId: brand.key,
    botName: brand.bot_persona
  }), {
    status: 200,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json"
    }
  });
}
// ── Main Handler ─────────────────────────────────────────────────────
Deno.serve(async (req)=>{
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;
  try {
    const body = await req.json();
    const { messages, session_id, siteId, origin: bodyOrigin } = body;
    const headerOrigin = req.headers.get("origin") || bodyOrigin;
    // 1. Resolve Brand
    const brand = await getBrandConfig(siteId, headerOrigin);
    if (!brand) return errorResponse("Brand not found", 404);
    // 2. Persist conversation
    let conversationId = null;
    const lastUser = [
      ...messages || []
    ].reverse().find((m)=>m.role === "user");
    if (session_id) {
      const { data: existing } = await supabase.from("conversations").select("id").eq("session_id", session_id).maybeSingle();
      if (existing) {
        conversationId = existing.id;
      } else {
        const { data: created } = await supabase.from("conversations").insert({
          session_id,
          metadata: {
            brand_key: brand.key
          }
        }).select("id").single();
        conversationId = created?.id || null;
        if (conversationId) dispatchAll(supabase, "conversation.started", {
          session_id,
          conversation_id: conversationId
        });
      }
      if (conversationId && lastUser) {
        await supabase.from("messages").insert({
          conversation_id: conversationId,
          role: "user",
          content: lastUser.content
        });
        dispatchAll(supabase, "message.created", {
          conversation_id: conversationId,
          session_id,
          role: "user",
          content: lastUser.content
        }).catch(()=>{});
      }
    }
    // 3. Route to Engine
    if (brand.ai_engine === "dialogflow") {
      return await callDialogflow(brand, messages, conversationId, session_id);
    } else {
      return await callGeminiStream(brand.system_prompt, messages, conversationId, session_id);
    }
  } catch (e) {
    console.error("chat error:", e);
    return errorResponse(e instanceof Error ? e.message : "Unknown", 500);
  }
});
// ── Stream Capture Helper ────────────────────────────────────────────
async function captureAssistantReply(stream, conversationId, sessionId) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let full = "", buffer = "";
  while(true){
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, {
      stream: true
    });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines){
      const t = line.trim();
      if (!t.startsWith("data:")) continue;
      const data = t.slice(5).trim();
      if (data === "[DONE]") continue;
      try {
        const json = JSON.parse(data);
        const delta = json.choices?.[0]?.delta?.content;
        if (delta) full += delta;
      } catch (_e) {}
    }
  }
  if (full && conversationId) {
    await supabase.from("messages").insert({
      conversation_id: conversationId,
      role: "assistant",
      content: full
    });
    dispatchAll(supabase, "message.created", {
      conversation_id: conversationId,
      session_id: sessionId,
      role: "assistant",
      content: full
    }).catch(()=>{});
  }
}
