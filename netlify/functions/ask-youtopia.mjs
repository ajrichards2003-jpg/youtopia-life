import OpenAI from "openai";
import { getUser } from "@netlify/identity";
import { getStore } from "@netlify/blobs";

const DAILY_LIMIT = 3;
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req) => {
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);
  try {
    const user = await getUser();
    if (!user?.id) return json({ error: "Please sign in to Ask Youtopia." }, 401);

    const body = await req.json().catch(() => ({}));
    const question = String(body.question || "").trim().slice(0, 600);
    if (!question) return json({ error: "Ask a question first." }, 400);

    const day = new Date().toISOString().slice(0, 10);
    const key = `${user.id}/${day}`;
    const store = getStore({ name: "ask-youtopia-daily-usage", consistency: "strong" });
    const usage = (await store.get(key, { type: "json" })) || { used: 0 };
    if (usage.used >= DAILY_LIMIT) return json({ error: "Your three Youtopia wishes are used for today. The genie resets tomorrow (UTC). 🧞" }, 429);

    const client = new OpenAI();
    const response = await client.responses.create({
      model: "gpt-5.6-luna",
      input: [
        { role: "system", content: "You are Ask Youtopia, the evidence-aware discovery guide for Youtopia Life. Be concise, curious and useful. Distinguish established evidence, promising evidence, emerging research, anecdote and unresolved claims. Never treat a product claim as proof. Do not diagnose or prescribe. When relevant suggest what primary-source evidence the user should inspect and note uncertainty. Youtopia philosophy: curious enough to investigate, rigorous enough to question, independent enough to change our minds." },
        { role: "user", content: question }
      ],
      max_output_tokens: 500
    });
    const answer = response.output_text || "I couldn't produce an answer this time.";
    const used = usage.used + 1;
    await store.setJSON(key, { used, day });
    return json({ answer, remaining: DAILY_LIMIT - used });
  } catch (error) {
    console.error("Ask Youtopia failed", error);
    return json({ error: "Ask Youtopia is temporarily unavailable. Please try again later." }, 503);
  }
};