import { ref } from 'vue'

export function useAudioPreview() {
  const playingUrl = ref(null)
  const audio = new Audio()
  let queue = []

  audio.addEventListener('ended', () => {
    const next = queue.shift()
    if (next) {
      playUrl(next)
    } else {
      playingUrl.value = null
    }
  })

  function playUrl(url) {
    audio.src = url
    // play() can reject with AbortError if interrupted by a fast switch to
    // another track or a stop() call before it resolves; that's expected.
    audio.play().catch(() => {})
    playingUrl.value = url
  }

  function toggle(url) {
    queue = []
    if (playingUrl.value === url) {
      audio.pause()
      playingUrl.value = null
      return
    }
    playUrl(url)
  }

  function playAll(urls) {
    const [first, ...rest] = urls
    if (!first) return
    queue = rest
    playUrl(first)
  }

  function stop() {
    queue = []
    audio.pause()
    playingUrl.value = null
  }

  return { playingUrl, toggle, playAll, stop }
}
