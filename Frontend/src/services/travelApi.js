const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function generateTravelPlan(tripRequest) {
  const response = await fetch(`${API_URL}/api/travel-plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(tripRequest),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}
