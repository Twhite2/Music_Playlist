<script setup>
defineProps({
  variant: { type: String, required: true, validator: (v) => ['success', 'fallback', 'error'].includes(v) },
  label: { type: String, required: true },
  message: { type: String, default: '' },
})
</script>

<template>
  <div class="status-pill" :class="variant">
    <span class="dot" aria-hidden="true"></span>
    <div class="status-text">
      <p class="status-label">{{ label }}</p>
      <p v-if="message" class="status-message">{{ message }}</p>
    </div>
  </div>
</template>

<style scoped>
.status-pill {
  display: inline-flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  margin-top: 0.35rem;
  flex-shrink: 0;
  background: var(--teal-lt);
}

.status-pill.fallback .dot,
.status-pill.error .dot {
  background: var(--burgundy-lt);
}

.status-label {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--beige);
  margin: 0;
}

.status-message {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--beige-dim);
  margin: 0.2rem 0 0;
}
</style>
