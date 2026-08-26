import { ref } from 'vue'

const RADIUS = 60
const STRENGTH = 5

export function useMagneticHover(disabled) {
  const offset = ref({ x: 0, y: 0 })
  const isTouch = typeof window !== 'undefined' && window.matchMedia('(pointer: coarse)').matches

  function handleMouseMove(event) {
    if (isTouch || disabled.value) return

    const rect = event.currentTarget.getBoundingClientRect()
    const dx = event.clientX - (rect.left + rect.width / 2)
    const dy = event.clientY - (rect.top + rect.height / 2)

    if (Math.hypot(dx, dy) < RADIUS) {
      offset.value = { x: dx / STRENGTH, y: dy / STRENGTH }
    } else {
      offset.value = { x: 0, y: 0 }
    }
  }

  function handleMouseLeave() {
    offset.value = { x: 0, y: 0 }
  }

  return { offset, handleMouseMove, handleMouseLeave }
}
