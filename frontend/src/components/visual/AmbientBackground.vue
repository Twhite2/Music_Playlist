<template>
  <div class="ambient" aria-hidden="true">
    <div class="glow glow-teal" />
    <div class="glow glow-burgundy" />
    <div class="grain" />
  </div>
</template>

<style scoped>
.ambient {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
}

.glow-teal {
  width: 46rem;
  height: 46rem;
  top: -16rem;
  left: -8rem;
  background: var(--teal);
  opacity: 0.16;
  animation: drift-teal 42s ease-in-out infinite alternate;
}

.glow-burgundy {
  width: 30rem;
  height: 30rem;
  top: 6rem;
  right: -10rem;
  background: var(--burgundy);
  opacity: 0.14;
  animation: drift-burgundy 36s ease-in-out infinite alternate;
}

.grain {
  position: absolute;
  inset: 0;
  opacity: 0.035;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

@keyframes drift-teal {
  from {
    transform: translate(0, 0);
  }
  to {
    transform: translate(2.5rem, 3rem);
  }
}

@keyframes drift-burgundy {
  from {
    transform: translate(0, 0);
  }
  to {
    transform: translate(-2rem, 2.5rem);
  }
}
</style>
