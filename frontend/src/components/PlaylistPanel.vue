<script setup>
import { computed } from 'vue'
import TrackRow from './TrackRow.vue'

const props = defineProps({
  songs: { type: Array, required: true },
  genre: { type: String, required: true },
  playingUrl: { type: String, default: null },
})

defineEmits(['toggle', 'play-all'])

const heroArtwork = computed(() => props.songs.find((song) => song.artwork_url)?.artwork_url ?? null)
</script>

<template>
  <section class="playlist" :aria-label="`${genre} playlist`">
    <p class="section-label">Your playlist</p>

    <div class="hero-card">
      <div class="hero-artwork">
        <img v-if="heroArtwork" :src="heroArtwork" alt="" />
        <div v-else class="hero-artwork-fallback">
          <span class="fallback-label">Genre</span>
          <span class="fallback-genre">{{ genre }}</span>
        </div>
      </div>
      <div class="hero-meta">
        <p class="hero-genre">{{ genre }}</p>
        <p class="hero-subtitle">AI generated playlist</p>
        <p class="hero-count">{{ songs.length }} tracks</p>
        <button type="button" class="play-all" @click="$emit('play-all')">
          <span aria-hidden="true">▶</span> Play all
        </button>
      </div>
    </div>

    <TransitionGroup tag="div" name="track-row" class="track-list">
      <TrackRow
        v-for="(song, index) in songs"
        :key="`${song.title}-${song.artist}`"
        :song="song"
        :index="index"
        :playing="Boolean(song.preview_url) && song.preview_url === playingUrl"
        :style="{ transitionDelay: `${index * 40}ms` }"
        @toggle="$emit('toggle', song.preview_url)"
      />
    </TransitionGroup>
  </section>
</template>

<style scoped>
.playlist {
  border-top: 1px solid var(--ink-2);
  padding-top: 2rem;
}

.section-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--beige-dim);
  margin: 0 0 1.25rem;
}

.hero-card {
  display: flex;
  align-items: center;
  gap: 1.75rem;
  background: var(--ink-2);
  border: 1px solid rgba(231, 223, 209, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 640px) {
  .hero-card {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
}

.hero-artwork {
  flex-shrink: 0;
  width: clamp(150px, 20vw, 240px);
  height: clamp(150px, 20vw, 240px);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.hero-artwork img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-artwork-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  background: radial-gradient(circle at 30% 20%, var(--teal) 0%, transparent 60%),
    radial-gradient(circle at 75% 85%, var(--burgundy) 0%, transparent 60%), var(--ink);
  position: relative;
}

.hero-artwork-fallback::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.06;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

.fallback-label {
  position: relative;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--beige-dim);
}

.fallback-genre {
  position: relative;
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--beige);
  text-align: center;
  padding: 0 0.75rem;
}

.hero-meta {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.hero-genre {
  font-family: var(--font-display);
  font-variation-settings: 'WONK' 1;
  font-size: var(--step-3);
  font-weight: 600;
  color: var(--beige);
  margin: 0;
}

.hero-subtitle {
  font-family: var(--font-body);
  color: var(--beige-dim);
  margin: 0;
}

.hero-count {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--beige-dim);
  margin: 0.15rem 0 1rem;
}

.play-all {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-body);
  font-weight: 600;
  color: var(--beige);
  background: var(--burgundy);
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1.35rem;
  cursor: pointer;
  transition: background-color 180ms ease, box-shadow 180ms ease;
}

.play-all:hover {
  background: var(--burgundy-lt);
  box-shadow: 0 0 20px color-mix(in srgb, var(--burgundy-lt) 40%, transparent);
}

.track-list {
  position: relative;
  display: flex;
  flex-direction: column;
}

.track-row-enter-active {
  transition: opacity 400ms ease, transform 400ms ease;
}

.track-row-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.track-row-leave-active {
  transition: opacity 200ms ease;
  position: absolute;
  width: 100%;
}

.track-row-leave-to {
  opacity: 0;
}

.track-row-move {
  transition: transform 400ms ease;
}
</style>
