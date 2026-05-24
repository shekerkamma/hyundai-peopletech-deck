const BACKEND_URL = "http://127.0.0.1:8025";

async function backendRequest(path, options = {}) {
  const response = await fetch(`${BACKEND_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });
  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status}`);
  }
  return response.json();
}

window.BackendClient = {
  health: () => backendRequest("/api/health"),
  events: (limit = 25) => backendRequest(`/api/events?limit=${limit}`),
  incidents: () => backendRequest("/api/incidents"),
  modelVersions: () => backendRequest("/api/model-versions"),
  generateEvent: (payload) => backendRequest("/api/events/generate", {
    method: "POST",
    body: JSON.stringify(payload)
  }),
  retrain: (payload) => backendRequest("/api/model-versions/retrain", {
    method: "POST",
    body: JSON.stringify(payload)
  })
};
