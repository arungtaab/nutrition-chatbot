import { useEffect, useRef, useState } from "react";
import { fetchHistory, sendMessage } from "../api.js";

const STORAGE_KEY = "nutrition_chat_conversation_id";

const SUGGESTIONS = [
  "High-protein vegetarian dinners—three ideas and why they work.",
  "A low-sodium lunch I can prep in under 30 minutes.",
  "Breakfast ideas with more protein, kept simple for busy mornings.",
];

function prefersReducedMotion() {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hydrating, setHydrating] = useState(true);
  const [error, setError] = useState(null);
  const listRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      setHydrating(false);
      return () => {
        cancelled = true;
      };
    }

    (async () => {
      try {
        const rows = await fetchHistory(stored);
        if (cancelled) return;
        setConversationId(stored);
        setMessages(
          rows.map((r) => ({
            id: r.id,
            role: r.role,
            content: r.content,
          })),
        );
      } catch {
        if (!cancelled) localStorage.removeItem(STORAGE_KEY);
      } finally {
        if (!cancelled) setHydrating(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const behavior = prefersReducedMotion() ? "auto" : "smooth";
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior,
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
      localStorage.setItem(STORAGE_KEY, res.conversation_id);
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

  const showEmptyState =
    messages.length === 0 && !loading && !hydrating;

  return (
    <section className="message-dock" aria-label="Chat">
      <div className="message-dock-messages" ref={listRef}>
        {hydrating && (
          <p className="message-empty muted" role="status">
            Loading your conversation…
          </p>
        )}
        {showEmptyState && (
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
            key={
              m.id != null ? `${m.role}-${m.id}` : `${idx}-${m.role}-${m.content?.slice(0, 12)}`
            }
            className={
              m.role === "user"
                ? "message message-user"
                : "message message-assistant"
            }
          >
            <div className="message-role">
              {m.role === "user" ? "You" : "Nourish"}
            </div>
            <div className="message-content">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant loading-msg">
            <div className="message-role">Nourish</div>
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
            disabled={loading || hydrating}
            aria-label="Message"
          />
          <button type="submit" disabled={loading || hydrating || !input.trim()}>
            {loading ? "…" : "Send"}
          </button>
        </form>
      </div>
    </section>
  );
}
