import { ref, onMounted, onUnmounted } from 'vue'

export function usePrefersReducedMotion() {
  const prefersReducedMotion = ref(false)
  let mediaQuery

  function update(event) {
    prefersReducedMotion.value = event.matches
  }

  onMounted(() => {
    mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotion.value = mediaQuery.matches
    mediaQuery.addEventListener('change', update)
  })

  onUnmounted(() => {
    mediaQuery?.removeEventListener('change', update)
  })

  return prefersReducedMotion
}
