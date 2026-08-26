const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchPlaylist(genre) {
  let response
  try {
    response = await fetch(`${BASE_URL}/api/playlist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ genre }),
    })
  } catch {
    throw new Error("Couldn't reach the generator. Try again.")
  }

  if (!response.ok) {
    throw new Error("Couldn't reach the generator. Try again.")
  }

  return response.json()
}
