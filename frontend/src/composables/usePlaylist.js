import { ref } from 'vue'
import { fetchPlaylist } from '../services/api.js'

export function usePlaylist() {
  const status = ref('idle')
  const songs = ref([])
  const source = ref(null)
  const errorMessage = ref('')

  async function generate(genre) {
    status.value = 'loading'
    try {
      const result = await fetchPlaylist(genre)
      songs.value = result.songs
      source.value = result.source
      status.value = 'success'
    } catch (error) {
      errorMessage.value = error.message
      status.value = 'error'
    }
  }

  return { status, songs, source, errorMessage, generate }
}
