<script setup>
defineProps({
  available: { type: Boolean, required: true },
  playing: { type: Boolean, default: false },
  title: { type: String, required: true },
})

defineEmits(['toggle'])
</script>

<template>
  <button
    v-if="available"
    type="button"
    class="preview-button"
    :class="{ playing }"
    :aria-label="playing ? `Stop ${title}` : `Play ${title}`"
    @click="$emit('toggle')"
  >
    <span v-if="playing" class="mini-wave" aria-hidden="true">
      <span /><span /><span />
    </span>
    <span v-else aria-hidden="true">▶</span>
  </button>
  <span v-else class="preview-unavailable" aria-hidden="true">—</span>
</template>

<style scoped>
.preview-button {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--beige-dim);
  background: var(--ink-2);
  border: 1px solid rgba(231, 223, 209, 0.15);
  cursor: pointer;
  font-size: 0.65rem;
  transition: background-color 180ms ease, border-color 180ms ease, color 180ms ease;
}

.preview-button:hover {
  border-color: var(--teal-lt);
  color: var(--teal-lt);
}

.preview-button.playing {
  color: var(--beige);
  background: var(--burgundy);
  border-color: var(--burgundy);
}

.preview-button.playing:hover {
  background: var(--burgundy-lt);
  border-color: var(--burgundy-lt);
}

.mini-wave {
  display: flex;
  align-items: center;
  gap: 2px;
  height: 0.8rem;
}

.mini-wave span {
  width: 2px;
  height: 100%;
  background: currentColor;
  border-radius: 1px;
  animation: mini-bounce 0.9s ease-in-out infinite;
  transform-origin: center;
}

.mini-wave span:nth-child(2) {
  animation-delay: -0.6s;
}

.mini-wave span:nth-child(3) {
  animation-delay: -0.3s;
}

@keyframes mini-bounce {
  0%,
  100% {
    transform: scaleY(0.3);
  }
  50% {
    transform: scaleY(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .mini-wave span {
    animation: none;
    transform: scaleY(0.7);
  }
}

.preview-unavailable {
  width: 2.25rem;
  height: 2.25rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--beige-dim);
  opacity: 0.4;
}
</style>
