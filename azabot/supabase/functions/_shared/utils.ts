import { corsHeaders } from "./cors.ts";
export function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json"
    }
  });
}
export function errorResponse(message, status = 400) {
  return jsonResponse({
    success: false,
    error: message
  }, status);
}
export function flatten(data) {
  return typeof data === "object" && data !== null ? data : {
    data
  };
}
