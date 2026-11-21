(() => {
  const cards = [...document.querySelectorAll('.overview-card-art')];
  const motion = matchMedia('(prefers-reduced-motion: no-preference)');
  const period = 8000;
  const duration = 1200;
  const stagger = 240;
  const waveWidth = 0.55;
  const waveform = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <defs>
      <linearGradient id="wave">
        <stop offset="0" stop-color="#808080"/>
        <stop offset=".25" stop-color="#802680"/>
        <stop offset=".5" stop-color="#808080"/>
        <stop offset=".75" stop-color="#80da80"/>
        <stop offset="1" stop-color="#808080"/>
      </linearGradient>
      <linearGradient id="fade" x2="0" y2="1">
        <stop offset="0" stop-color="white" stop-opacity="0"/>
        <stop offset=".25" stop-color="white"/>
        <stop offset=".75" stop-color="white"/>
        <stop offset="1" stop-color="white" stop-opacity="0"/>
      </linearGradient>
      <mask id="edges"><rect width="100" height="100" fill="url(#fade)"/></mask>
    </defs>
    <rect width="100" height="100" fill="url(#wave)" mask="url(#edges)"/>
  </svg>`;
  const map = `data:image/svg+xml;base64,${btoa(waveform)}`;
  const definitions = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  definitions.setAttribute('aria-hidden', 'true');
  definitions.setAttribute('width', '0');
  definitions.setAttribute('height', '0');
  definitions.style.position = 'absolute';
  definitions.innerHTML = `<defs>${[0, 1, 2, 3].map(index => `
    <filter id="overview-ripple-${index}" x="0" y="0" width="1" height="1"
            primitiveUnits="objectBoundingBox" color-interpolation-filters="sRGB">
      <feImage href="${map}" x="0" y="0" width="${waveWidth}" height="1"
               preserveAspectRatio="none" result="wave"/>
      <feOffset in="wave" dx="-${waveWidth}" x="0" y="0" width="1" height="1" result="travel"/>
      <feFlood flood-color="#808080" result="neutral"/>
      <feComposite in="travel" in2="neutral" operator="over" result="displacement"/>
      <feDisplacementMap in="SourceGraphic" in2="displacement" scale=".045"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>`).join('')}</defs>`;
  document.body.prepend(definitions);

  const waves = [...definitions.querySelectorAll('filter')].map((filter, index) => ({
    filter: `url(#${filter.id})`,
    offset: filter.querySelector('feOffset'),
    images: cards.filter(card => Number(card.dataset.waveOrder) === index),
    active: false,
  }));

  let frame;
  let timer;

  function setActive(wave, active) {
    if (wave.active === active) return;
    for (const image of wave.images) image.style.filter = active ? wave.filter : '';
    wave.active = active;
  }

  function render(start, now) {
    const elapsed = now - start;
    waves.forEach((wave, index) => {
      const progress = (elapsed - index * stagger) / duration;
      const active = progress >= 0 && progress < 1;
      if (active) {
        wave.offset.setAttribute('dx', -waveWidth + progress * (1 + waveWidth));
      }
      setActive(wave, active);
    });

    if (elapsed < duration + stagger * (waves.length - 1)) {
      frame = requestAnimationFrame(now => render(start, now));
    } else {
      timer = setTimeout(startWave, Math.max(0, period - elapsed));
    }
  }

  function startWave() {
    frame = requestAnimationFrame(now => render(now, now));
  }

  function updateMotion() {
    cancelAnimationFrame(frame);
    clearTimeout(timer);
    waves.forEach(wave => setActive(wave, false));
    if (motion.matches && !document.hidden) timer = setTimeout(startWave, 650);
  }

  motion.addEventListener('change', updateMotion);
  document.addEventListener('visibilitychange', updateMotion);
  updateMotion();
})();
