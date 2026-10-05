const ALLOWED_CHANNEL_IDS = new Set([
  "6ac242196a5c39ccb60f2f0b", // Biohacker Australia
  "6ac242196a5c39ccb60f2f0a", // Youtopia Life
]);
const BLOCKED_CHANNEL_IDS = new Set([
  "6ac242196a5c39ccb60f2f0c", // Cardinia Tigers Junior Football Club
]);

const BUFFER_API_URL = "https://api.buffer.com";

async function bufferQuery(apiKey, query, variables = {}) {
  const response = await fetch(BUFFER_API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ query, variables }),
  });

  const payload = await response.json();
  if (!response.ok || payload.errors?.length) {
    const message = payload.errors?.map((e) => e.message).join("; ") || `HTTP ${response.status}`;
    throw new Error(message);
  }
  return payload.data;
}

export default async () => {
  const apiKey = Netlify.env.get("BUFFER_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ ok: false, error: "BUFFER_API_KEY is not configured." }), {
      status: 500,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }

  try {
    const accountData = await bufferQuery(apiKey, `
      query BufferOrganizations {
        account {
          organizations { id name }
        }
      }
    `);

    const organizations = accountData?.account?.organizations || [];
    const results = [];

    for (const organization of organizations) {
      const channelData = await bufferQuery(apiKey, `
        query BufferChannels($organizationId: OrganizationId!) {
          channels(input: { organizationId: $organizationId }) {
            id
            name
            displayName
            service
            descriptor
            isDisconnected
            isLocked
            isQueuePaused
          }
        }
      `, { organizationId: organization.id });

      results.push({
        organization: { id: organization.id, name: organization.name },
        channels: (channelData?.channels || []).map((channel) => ({
          ...channel,
          automationAccess: ALLOWED_CHANNEL_IDS.has(channel.id) ? "allowed" : BLOCKED_CHANNEL_IDS.has(channel.id) ? "blocked" : "blocked-by-default",
        })),
      });
    }

    return new Response(JSON.stringify({ ok: true, mode: "read-only", organizations: results }, null, 2), {
      status: 200,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ ok: false, error: error.message }), {
      status: 502,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }
};
