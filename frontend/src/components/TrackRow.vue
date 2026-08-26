<script setup>
import PreviewButton from './PreviewButton.vue'

const props = defineProps({
  song: { type: Object, required: true },
  index: { type: Number, required: true },
  playing: { type: Boolean, default: false },
})

defineEmits(['toggle'])
</script>

<template>
  <div class="track-row" :class="{ playing }">
    <span class="track-number">
      <span v-if="playing" class="active-dot" aria-hidden="true" />
      {{ String(props.index + 1).padStart(2, '0') }}
    </span>

    <img
      v-if="song.artwork_url"
      class="track-artwork"
      :src="song.artwork_url"
      alt=""
    />
    <span v-else class="track-artwork track-artwork--empty" aria-hidden="true" />

    <span class="track-info">
      <span class="track-title">{{ song.title }}</span>
      <a
        v-if="song.store_url"
        class="track-artist"
        :href="song.store_url"
        target="_blank"
        rel="noopener"
        title="Opens in Apple Music"
      >
        {{ song.artist }}
      </a>
      <span v-else class="track-artist">{{ song.artist }}</span>
    </span>

    <span class="track-duration">{{ song.preview_url ? '0:30' : '' }}</span>

    <PreviewButton
      :available="Boolean(song.preview_url)"
      :playing="playing"
      :title="song.title"
      @toggle="$emit('toggle')"
    />
  </div>
</template>

<style scoped>
.track-row {
  display: grid;
  grid-template-columns: 2rem 56px 1fr auto auto;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 0.5rem;
  border-bottom: 1px solid rgba(231, 223, 209, 0.06);
}

.track-row:last-child {
  border-bottom: none;
}

.track-row:hover {
  background: color-mix(in srgb, var(--ink-2) 60%, transparent);
}

.track-number {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--beige-dim);
  font-variant-numeric: tabular-nums;
}

.active-dot {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background: var(--burgundy-lt);
  flex-shrink: 0;
}

.track-artwork {
  width: 56px;
  height: 56px;
  border-radius: 6px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.track-artwork--empty {
  background: var(--ink-2);
  border: 1px solid rgba(231, 223, 209, 0.08);
}

.track-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  gap: 0.15rem;
}

.track-title {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 500;
  color: var(--beige);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.track-row.playing .track-title {
  color: var(--beige);
  font-weight: 600;
}

.track-artist {
  font-family: var(--font-body);
  font-size: 0.8rem;
  color: var(--beige-dim);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

a.track-artist:hover {
  color: var(--teal-lt);
  text-decoration: underline;
}

.track-duration {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--beige-dim);
}
</style>
