<script setup>
import { computed } from 'vue'
import GenerationVisualizer from './visual/GenerationVisualizer.vue'
import { usePrefersReducedMotion } from '../composables/usePrefersReducedMotion.js'
import { useMagneticHover } from '../composables/useMagneticHover.js'

const props = defineProps({
  modelValue: { type: String, required: true },
  genres: { type: Array, required: true },
  status: { type: String, required: true },
})

const emit = defineEmits(['update:modelValue', 'generate'])

const loading = computed(() => props.status === 'loading')
const prefersReducedMotion = usePrefersReducedMotion()
const { offset, handleMouseMove, handleMouseLeave } = useMagneticHover(prefersReducedMotion)

const buttonStyle = computed(() => ({
  transform: `translate(${offset.value.x}px, ${offset.value.y}px)`,
}))
</script>

<template>
  <div class="generator" :class="{ loading }">
    <template v-if="!loading">
      <div class="field">
        <label for="genre-select">Genre</label>
        <div class="select-wrap">
          <select
            id="genre-select"
            :value="modelValue"
            @change="$emit('update:modelValue', $event.target.value)"
          >
            <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
          </select>
          <span class="chevron" aria-hidden="true">⌄</span>
        </div>
      </div>

      <button
        type="button"
        class="generate-action"
        :style="buttonStyle"
        @mousemove="handleMouseMove"
        @mouseleave="handleMouseLeave"
        @click="$emit('generate')"
      >
        Generate playlist
        <span class="arrow" aria-hidden="true">→</span>
      </button>
    </template>

    <template v-else>
      <div class="loading-state">
        <p class="loading-label">Generating playlist</p>
        <p class="loading-genre">{{ modelValue }}</p>
        <p class="loading-copy">Finding a sequence of tracks…</p>
      </div>
      <GenerationVisualizer />
    </template>
  </div>
</template>

<style scoped>
.generator {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  background: var(--ink-2);
  border: 1px solid rgba(231, 223, 209, 0.1);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  transition: border-color 180ms ease, box-shadow 180ms ease;
}

.generator:hover,
.generator:focus-within {
  border-color: var(--teal-lt);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--teal-lt) 25%, transparent);
}

.generator.loading {
  justify-content: space-between;
}

@media (max-width: 560px) {
  .generator {
    flex-direction: column;
    align-items: stretch;
  }
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.field label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--beige-dim);
}

.select-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
}

select {
  appearance: none;
  font-family: var(--font-body);
  font-size: 1.15rem;
  font-weight: 500;
  color: var(--beige);
  background: transparent;
  border: none;
  padding: 0.1rem 1.5rem 0.1rem 0;
  cursor: pointer;
}

/* The opened dropdown list is rendered by the OS/browser, not by our page
styles, and falls back to a white popup background — so the options need
their own dark text regardless of the select's own light-on-dark color. */
select option {
  color: #0b0b0c;
  background: #ffffff;
}

.chevron {
  position: absolute;
  right: 0;
  color: var(--beige-dim);
  pointer-events: none;
}

.generate-action {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  color: var(--beige);
  background: var(--burgundy);
  border: none;
  border-radius: 999px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: background-color 180ms ease, box-shadow 180ms ease, transform 150ms ease;
}

.generate-action:hover {
  background: var(--burgundy-lt);
  box-shadow: 0 0 24px color-mix(in srgb, var(--burgundy-lt) 45%, transparent);
}

.generate-action:hover .arrow {
  transform: translateX(3px);
}

.generate-action:active {
  transform: scale(0.97);
}

.arrow {
  transition: transform 150ms ease;
}

.loading-state {
  min-width: 0;
}

.loading-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--teal-lt);
  margin: 0 0 0.3rem;
}

.loading-genre {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--beige);
  margin: 0;
}

.loading-copy {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--beige-dim);
  margin: 0.25rem 0 0;
}
</style>
