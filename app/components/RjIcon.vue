<script setup>
// Line icons used by the chrome and the `icon` options of rj-* blocks (Tabler-style paths).
defineProps({ name: { type: String, default: 'check' } });
const P = {
  truck: 'M3 6h11v10H3zM14 9h4l3 3v4h-7M7 19a2 2 0 100-4 2 2 0 000 4zM17 19a2 2 0 100-4 2 2 0 000 4z',
  box: 'M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5',
  gift: 'M3 8h18v4H3zM5 12v9h14v-9M12 8v13M12 8C10 4 6 4 6.5 6.5S12 8 12 8zM12 8c2-4 6-4 5.5-1.5S12 8 12 8z',
  mail: 'M3 5h18v14H3zM3 6l9 7 9-7',
  phone: 'M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z',
  star: 'M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3l-5.6 2.9 1.1-6.2L3 9.6l6.2-.9z',
  search: 'M10.5 18a7.5 7.5 0 100-15 7.5 7.5 0 000 15zM21 21l-5.2-5.2',
  cart: 'M3 4h2l2.4 11h11l2-8H6.2M9 20a1 1 0 100-2 1 1 0 000 2zM18 20a1 1 0 100-2 1 1 0 000 2z',
  user: 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 21c0-4 3.6-6 8-6s8 2 8 6',
  bolt: 'M13 3L4 14h7l-1 7 9-11h-7z',
  menu: 'M4 7h16M4 12h16M4 17h16',
  chevron: 'M9 6l6 6-6 6',
  shield: 'M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM8.5 12l2.5 2.5 4.5-5',
  return: 'M9 14L4 9l5-5M4 9h11a5 5 0 010 10h-3',
  euro: 'M17 6.5A7 7 0 1017 17.5M4 10h9M4 14h9',
  leaf: 'M5 19c0-8 5-14 15-14 0 10-6 15-14 15M5 19l7-7',
  clock: 'M12 21a9 9 0 100-18 9 9 0 000 18zM12 7v5l3 2',
  check: 'M12 21a9 9 0 100-18 9 9 0 000 18zM8 12.5l2.7 2.7L16 10',
  tag: 'M3 12V3h9l9 9-9 9zM7.5 7.5h.01',
  headset: 'M4 14v-2a8 8 0 0116 0v2M4 14h3v6H5a1 1 0 01-1-1zM20 14h-3v6h2a1 1 0 001-1zM17 20c0 1-2 2-5 2',
  factory: 'M3 21V10l6 4V10l6 4V6h6v15zM7 17h2M12 17h2M17 17h2',
  close: 'M6 6l12 12M18 6L6 18',
  copy: 'M8 8h12v12H8zM4 16V4h12',
  arrow: 'M5 12h14M13 6l6 6-6 6',
  mic: 'M12 3a3 3 0 00-3 3v6a3 3 0 006 0V6a3 3 0 00-3-3zM5 11a7 7 0 0014 0M12 18v3',
};
</script>

<template>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path :d="P[name] || P.check" />
  </svg>
</template>
