const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

/**
 * @param {string} message
 * @param {string | null} conversationId
 * @returns {Promise<{ reply: string, conversation_id: string }>}
 */
export async function sendMessage(message, conversationId) {
  const body = { message };
  if (conversationId) {
    body.conversation_id = conversationId;
  }

  let res;
  try {
    res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (e) {
    throw new Error(
      e instanceof Error
        ? e.message
        : "Network error — is the API running on " + API_BASE_URL + "?",
    );
  }

  let data = {};
  try {
    data = await res.json();
  } catch {
    /* ignore */
  }

  if (!res.ok) {
    const msg = data.error || `Request failed (${res.status})`;
    const err = new Error(msg);
    if (data.code) err.code = data.code;
    throw err;
  }

  return data;
}
