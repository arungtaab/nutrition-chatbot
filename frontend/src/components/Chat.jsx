import { useEffect, useRef, useState } from "react";
import { sendMessage } from "../api.js";

const SUGGESTIONS = [
  "High-protein vegetarian dinners—three ideas and why they work.",
  "A low-sodium lunch I can prep in under 30 minutes.",
  "Breakfast ideas with more protein, kept simple for busy mornings.",
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
    <section className="message-dock" aria-label="Chat">
      <div className="message-dock-messages" ref={listRef}>
        {messages.length === 0 && !loading && (
          <div className="message-empty-wrap">
            <p className="message-empty">
              Ask for meal ideas, gentle nutrition tips, or a clearer take on a
              recommendation. If your project ingests docs, answers can draw on
              that knowledge base.
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
              m.role === "user"
                ? "message message-user"
                : "message message-assistant"
            }
          >
            <div className="message-role">
              {m.role === "user" ? "You" : "Companion"}
            </div>
            <div className="message-content">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant loading-msg">
            <div className="message-role">Companion</div>
            <div className="message-content muted">Thinking…</div>
          </div>
        )}
      </div>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <div className="message-dock-composer">
        <form className="dock-form" onSubmit={onSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about meals, swaps, or nutrition in plain language…"
            autoComplete="off"
            disabled={loading}
            aria-label="Message"
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "…" : "Send"}
          </button>
        </form>
      </div>
    </section>
  );
}
