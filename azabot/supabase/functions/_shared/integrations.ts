export async function dispatchAll(supabase, event, payload) {
  const { data: integs } = await supabase.from("integrations").select("*").eq("enabled", true);
  if (!integs?.length) return;
  for (const integ of integs){
    if (!(integ.events || []).includes(event)) continue;
    fireOne(supabase, integ, event, payload).catch((e)=>console.error("Integration dispatch error", e));
  }
}
export async function fireOne(supabase, integ, event, payload) {
  const startedAt = Date.now();
  let status = "failed", statusCode = 0, responseBody = "", errorMessage = "";
  try {
    if (integ.type === "webhook") {
      const url = integ.config?.url;
      if (!url) throw new Error("Webhook URL not configured");
      const headers = {
        "Content-Type": "application/json"
      };
      if (integ.config?.secret) headers["X-AzaBot-Secret"] = integ.config.secret;
      const res = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify({
          event,
          integration: integ.name,
          data: payload
        })
      });
      statusCode = res.status;
      responseBody = (await res.text()).slice(0, 2000);
      status = res.ok ? "success" : "failed";
    } else if (integ.type === "telegram") {
      const { bot_token, chat_id } = integ.config || {};
      if (!bot_token || !chat_id) throw new Error("Telegram bot_token & chat_id required");
      const text = formatForChat(event, payload);
      const res = await fetch(`https://api.telegram.org/bot${bot_token}/sendMessage`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          chat_id,
          text,
          parse_mode: "HTML"
        })
      });
      statusCode = res.status;
      responseBody = (await res.text()).slice(0, 2000);
      status = res.ok ? "success" : "failed";
    } else if (integ.type === "whatsapp") {
      const { phone_number_id, access_token, recipient } = integ.config || {};
      if (!phone_number_id || !access_token || !recipient) throw new Error("WhatsApp config incomplete");
      const text = formatForChat(event, payload);
      const res = await fetch(`https://graph.facebook.com/v20.0/${phone_number_id}/messages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`
        },
        body: JSON.stringify({
          messaging_product: "whatsapp",
          to: recipient,
          type: "text",
          text: {
            body: text
          }
        })
      });
      statusCode = res.status;
      responseBody = (await res.text()).slice(0, 2000);
      status = res.ok ? "success" : "failed";
    } else if (integ.type === "twilio") {
      const { account_sid, auth_token, from, to } = integ.config || {};
      if (!account_sid || !auth_token || !from || !to) throw new Error("Twilio config incomplete");
      const text = formatForChat(event, payload);
      const basic = btoa(`${account_sid}:${auth_token}`);
      const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${account_sid}/Messages.json`, {
        method: "POST",
        headers: {
          Authorization: `Basic ${basic}`,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          To: to,
          From: from,
          Body: text
        })
      });
      statusCode = res.status;
      responseBody = (await res.text()).slice(0, 2000);
      status = res.ok ? "success" : "failed";
    } else {
      throw new Error(`Unsupported integration type: ${integ.type}`);
    }
  } catch (e) {
    errorMessage = e instanceof Error ? e.message : "Unknown error";
  }
  await supabase.from("webhook_logs").insert({
    integration_id: integ.id,
    integration_type: integ.type,
    event,
    status,
    status_code: statusCode || null,
    request_payload: payload,
    response_body: responseBody,
    error_message: errorMessage
  });
  return {
    status,
    statusCode,
    errorMessage,
    responseBody,
    durationMs: Date.now() - startedAt
  };
}
function formatForChat(event, p) {
  if (event === "test.event") return `🧪 <b>اختبار AzaBot</b>\n${p.message}`;
  if (event === "conversation.started") {
    return `🆕 <b>محادثة جديدة</b>\nالجلسة: <code>${p.session_id}</code>`;
  }
  if (event === "message.created") {
    const role = p.role === "user" ? "👤 الزائر" : "🤖 البوت";
    return `${role}:\n${p.content}`;
  }
  return JSON.stringify(p);
}
