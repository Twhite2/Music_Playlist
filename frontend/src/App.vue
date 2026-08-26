<script setup>
import { ref, computed } from 'vue'
import GeneratorControl from './components/GeneratorControl.vue'
import PlaylistPanel from './components/PlaylistPanel.vue'
import StatusNote from './components/StatusNote.vue'
import AmbientBackground from './components/visual/AmbientBackground.vue'
import { usePlaylist } from './composables/usePlaylist.js'
import { useAudioPreview } from './composables/useAudioPreview.js'

const GENRES = ['Afrobeats', 'Amapiano', 'Highlife', 'Jazz', 'Hip hop', 'Rock', 'Classical', 'Electronic']

const selectedGenre = ref(GENRES[0])
const showInfo = ref(false)
const { status, songs, source, errorMessage, generate } = usePlaylist()
const { playingUrl, toggle, playAll, stop } = useAudioPreview()

const previewUrls = computed(() => songs.value.map((song) => song.preview_url).filter(Boolean))

async function handleGenerate() {
  stop()
  await generate(selectedGenre.value)
}

function handlePlayAll() {
  playAll(previewUrls.value)
}
</script>

<template>
  <AmbientBackground />

  <div class="app-shell">
    <header class="site-header">
      <span class="brand">AI Playlist</span>
      <button
        type="button"
        class="info-toggle"
        :aria-expanded="showInfo"
        aria-controls="how-it-works"
        @click="showInfo = !showInfo"
      >
        How it works
      </button>
    </header>

    <p v-if="showInfo" id="how-it-works" class="info-panel">
      Pick a genre and an AI model writes a five-track playlist for it. Each track is matched
      against Apple's music catalog for a 30-second preview, artwork, and a link to listen in full.
    </p>

    <section class="hero">
      <p class="eyebrow">AI Playlist</p>
      <h1 class="hero-title">Discover<br />your next sound.</h1>
      <p class="hero-subtitle">
        Choose a genre and let AI build a five-track playlist you can actually listen to.
      </p>

      <GeneratorControl v-model="selectedGenre" :genres="GENRES" :status="status" @generate="handleGenerate" />

      <div aria-live="polite" class="status-region">
        <StatusNote v-if="status === 'success' && source === 'model'" variant="success" label="Playlist generated" />
        <StatusNote
          v-else-if="status === 'success' && source === 'fallback'"
          variant="fallback"
          label="Using curated backup"
          message="The AI service was unavailable, so we've loaded a verified playlist."
        />
        <StatusNote v-else-if="status === 'error'" variant="error" label="Couldn't generate a playlist" :message="errorMessage" />
      </div>
    </section>

    <Transition name="playlist-reveal">
      <PlaylistPanel
        v-if="songs.length"
        class="playlist-wrapper"
        :class="{ dimmed: status === 'loading' }"
        :songs="songs"
        :genre="selectedGenre"
        :playing-url="playingUrl"
        @toggle="toggle"
        @play-all="handlePlayAll"
      />
    </Transition>
  </div>
</template>

<style scoped>
.app-shell {
  max-width: 1140px;
  margin: 0 auto;
  padding: 2rem 1.5rem 5rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--beige-dim);
}

.info-toggle {
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--beige-dim);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0;
}

.info-toggle:hover {
  color: var(--teal-lt);
}

.info-panel {
  max-width: 34rem;
  color: var(--beige-dim);
  font-size: 0.9rem;
  margin: -1rem 0 0;
}

.hero {
  padding: 1.5rem 0 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  max-width: 42rem;
}

.eyebrow {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--teal-lt);
  margin: 0;
  animation: rise 600ms ease-out both;
}

.hero-title {
  font-family: var(--font-display);
  font-variation-settings: 'WONK' 1;
  font-optical-sizing: auto;
  font-size: clamp(2.75rem, 7vw, var(--step-4));
  font-weight: 600;
  line-height: 1.05;
  margin: 0;
  animation: rise 650ms ease-out both;
  animation-delay: 60ms;
}

.hero-subtitle {
  color: var(--beige-dim);
  font-size: 1.05rem;
  margin: 0;
  max-width: 30rem;
  animation: rise 650ms ease-out both;
  animation-delay: 120ms;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status-region:empty {
  display: none;
}

.playlist-wrapper {
  transition: opacity 200ms ease;
}

.playlist-wrapper.dimmed {
  opacity: 0.4;
}

.playlist-reveal-enter-active {
  transition: opacity 550ms ease, transform 550ms ease;
}

.playlist-reveal-enter-from {
  opacity: 0;
  transform: translateY(16px);
}
</style>
