const BUFFER_API_URL = "https://api.buffer.com";

const CHANNELS = Object.freeze({
  youtopia: { id: "6ac242196a5c39ccb60f2f0a", name: "Youtopia Life" },
  biohacker: { id: "6ac242196a5c39ccb60f2f0b", name: "Biohacker Australia" },
});

const BLOCKED_CHANNEL_IDS = new Set([
  "6ac242196a5c39ccb60f2f0c", // Cardinia Tigers Junior Football Club
]);

const json = (body, status = 200) =>
  new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

export default async (request) => {
  if (request.method !== "POST") {
    return json({ ok: false, error: "POST required." }, 405);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "Valid JSON body required." }, 400);
  }

  const target = CHANNELS[body.channel];
  if (!target || BLOCKED_CHANNEL_IDS.has(target?.id)) {
    return json({ ok: false, error: "Channel is not approved for Youtopia automation." }, 403);
  }

  const text = typeof body.text === "string" ? body.text.trim() : "";
  if (!text) return json({ ok: false, error: "Post text is required." }, 400);

  const dueAt = body.dueAt || null;
  const proposedInput = {
    text,
    channelId: target.id,
    schedulingType: "automatic",
    mode: dueAt ? "customScheduled" : "addToQueue",
    ...(dueAt ? { dueAt } : {}),
  };

  // Safety gate: preview is the default and NEVER calls Buffer.
  if (body.confirm !== true) {
    return json({
      ok: true,
      executed: false,
      mode: "preview-only",
      target: target.name,
      proposedInput,
      message: "Nothing was sent to Buffer. Set confirm=true only after explicit approval.",
    });
  }

  // Write execution remains disabled during this preview stage.
  return json({
    ok: false,
    executed: false,
    mode: "write-disabled",
    target: target.name,
    proposedInput,
    message: "Approved channel, but Buffer write execution is intentionally disabled in this preview.",
  }, 409);
};
