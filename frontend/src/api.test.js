import { beforeEach, describe, expect, it, vi } from "vitest";
import { fetchHistory, sendMessage } from "./api.js";

describe("sendMessage", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("POSTs JSON and returns reply and conversation_id", async () => {
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        reply: "Try lentils.",
        conversation_id: "abc-123",
      }),
    });

    const out = await sendMessage("High protein dinner?", null);
    expect(out.reply).toBe("Try lentils.");
    expect(out.conversation_id).toBe("abc-123");
    expect(globalThis.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/chat"),
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("includes conversation_id in body when provided", async () => {
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ reply: "Ok", conversation_id: "same" }),
    });

    await sendMessage("Hi", "same");
    const [, init] = globalThis.fetch.mock.calls[0];
    const body = JSON.parse(init.body);
    expect(body.conversation_id).toBe("same");
  });
});

describe("fetchHistory", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("returns messages array on success", async () => {
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        messages: [{ id: 1, role: "user", content: "Hi" }],
      }),
    });

    const rows = await fetchHistory("conv-1");
    expect(rows).toHaveLength(1);
    expect(rows[0].content).toBe("Hi");
  });
});
