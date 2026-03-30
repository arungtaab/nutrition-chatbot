import { useEffect, useRef, useState } from "react";
import { sendMessage } from "../api.js";

const SUGGESTIONS = [
  "High-protein vegetarian dinner ideas — explain why each works.",
  "Low-sodium lunch I can prep in 30 minutes.",
  "Three breakfast ideas with more protein and why.",
];

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const listRef = useRef(null);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function onSubmit(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setError(null);
    setLoading(true);

    try {
      const res = await sendMessage(trimmed, conversationId);
      setConversationId(res.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.reply },
      ]);
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Something went wrong.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  function useSuggestion(text) {
    setInput(text);
  }

  return (
    <section className="chat-shell chrome-card" aria-label="Chat">
      <div className="messages" ref={listRef}>
        {messages.length === 0 && !loading && (
          <div className="message-empty-wrap">
            <p className="message-empty">
              Ask for meal ideas, nutrition tips, or an explanation of a
              recommendation. Grounded answers use your local knowledge base
              after ingest.
            </p>
            <div className="suggestions">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  className="chip"
                  onClick={() => useSuggestion(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={
              m.role === "user" ? "message message-user" : "message message-assistant"
            }
          >
            <div className="message-role">
              {m.role === "user" ? "You" : "Food Planner"}
            </div>
            <div className="message-content">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant loading-msg">
            <div className="message-role">Food Planner</div>
            <div className="message-content muted">Thinking…</div>
          </div>
        )}
      </div>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <form className="input-row" onSubmit={onSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask for meal ideas, nutrition tips, or explain a recommendation…"
          autoComplete="off"
          disabled={loading}
          aria-label="Message"
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "…" : "Send"}
        </button>
      </form>
    </section>
  );
}
