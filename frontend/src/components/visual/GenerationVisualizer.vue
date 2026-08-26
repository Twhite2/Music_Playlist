<template>
  <div class="visualizer" role="presentation">
    <span v-for="n in 7" :key="n" class="bar" :class="`bar-${n}`" />
  </div>
</template>

<style scoped>
.visualizer {
  display: flex;
  align-items: flex-end;
  gap: 0.3rem;
  height: 1.5rem;
}

.bar {
  width: 0.25rem;
  height: 100%;
  border-radius: 2px;
  background: var(--teal-lt);
  animation: bounce 1.1s ease-in-out infinite;
  transform-origin: bottom;
}

.bar-2,
.bar-5 {
  background: var(--burgundy-lt);
}

.bar-1 {
  animation-delay: -0.9s;
}
.bar-2 {
  animation-delay: -0.7s;
}
.bar-3 {
  animation-delay: -1.1s;
}
.bar-4 {
  animation-delay: -0.4s;
}
.bar-5 {
  animation-delay: -0.6s;
}
.bar-6 {
  animation-delay: -1s;
}
.bar-7 {
  animation-delay: -0.3s;
}

@keyframes bounce {
  0%,
  100% {
    transform: scaleY(0.25);
  }
  50% {
    transform: scaleY(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .bar {
    animation: none;
    transform: scaleY(0.6);
  }
}
</style>
