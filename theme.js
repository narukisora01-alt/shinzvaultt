const THEMES = {
  dark:       { '--bg':'#0c0c0c', '--surface':'rgba(255,255,255,0.03)', '--border':'rgba(255,255,255,0.08)', '--text':'#ffffff', '--muted':'rgba(255,255,255,0.3)',  '--dot':'#c0392b' },
  light:      { '--bg':'#f0f0f0', '--surface':'rgba(0,0,0,0.04)',       '--border':'rgba(0,0,0,0.1)',         '--text':'#111111', '--muted':'rgba(0,0,0,0.4)',      '--dot':'#c0392b' },
  system:     null,
  'dark-blue':{ '--bg':'#080d1a', '--surface':'rgba(255,255,255,0.04)', '--border':'rgba(255,255,255,0.09)', '--text':'#ffffff', '--muted':'rgba(255,255,255,0.3)', '--dot':'#c0392b' },
};

function applyTheme(name) {
  const resolved = name === 'system'
    ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    : name;
  const vars = THEMES[resolved] || THEMES.dark;
  const root = document.documentElement;
  Object.entries(vars).forEach(([k,v]) => root.style.setProperty(k, v));
  localStorage.setItem('sv_theme', name);
}

function loadTheme() {
  applyTheme(localStorage.getItem('sv_theme') || 'dark');
}

loadTheme();
