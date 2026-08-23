/* ===== BAZAAR — API Client ===== */
const API_BASE = ['localhost', '127.0.0.1'].includes(location.hostname)
  ? `${location.protocol}//${location.hostname}:8000/api`
  : 'https://v-bazaar.onrender.com/api';
const GOOGLE_CLIENT_ID = '866560142277-0htji2mqlg4r18395oqga97pln33420a.apps.googleusercontent.com';

// ===== Nepal city list (major + other), used everywhere a business's city is entered =====
const NEPAL_CITIES = {
  major: ['Kathmandu','Pokhara','Lalitpur','Bhaktapur','Biratnagar','Birgunj','Dharan','Bharatpur','Butwal','Hetauda','Nepalgunj','Dhangadhi','Itahari','Janakpur','Ghorahi','Tulsipur'],
  other: ['Banepa','Panauti','Dhulikhel','Kirtipur','Madhyapur Thimi','Tokha','Budhanilkantha','Chandragiri','Tarakeshwor','Gokarneshwor','Suryabinayak','Changunarayan','Gorkha','Tansen','Baglung','Beni','Waling','Damauli','Kawasoti','Ratnanagar','Bidur','Trishuli','Ilam','Damak','Rajbiraj','Lahan','Siraha','Gaur','Kalaiya','Jaleshwor','Bhairahawa','Kapilvastu','Tikapur','Mahendranagar','Birendranagar','Musikot','Jumla','Charikot','Malekhu'],
};

function cityOptionsHTML(selected = '') {
  const opt = c => `<option value="${c}"${c === selected ? ' selected' : ''}>${c}</option>`;
  const known = [...NEPAL_CITIES.major, ...NEPAL_CITIES.other];
  const otherSelected = selected && !known.includes(selected);
  return `<option value="">Select city...</option>` +
    `<optgroup label="Major Cities">${NEPAL_CITIES.major.map(opt).join('')}</optgroup>` +
    `<optgroup label="Other Cities">${NEPAL_CITIES.other.map(opt).join('')}</optgroup>` +
    `<option value="__other__"${otherSelected ? ' selected' : ''}>Other (type below)</option>`;
}

function onCitySelectChange(prefix) {
  const sel = document.getElementById(`${prefix}-city`);
  const other = document.getElementById(`${prefix}-city-other`);
  if (!sel || !other) return;
  other.style.display = sel.value === '__other__' ? '' : 'none';
  if (sel.value === '__other__') other.focus();
}

function setCityValue(prefix, value) {
  const sel = document.getElementById(`${prefix}-city`);
  const other = document.getElementById(`${prefix}-city-other`);
  if (!sel) return;
  const known = [...NEPAL_CITIES.major, ...NEPAL_CITIES.other];
  if (value && !known.includes(value)) {
    sel.value = '__other__';
    if (other) { other.style.display = ''; other.value = value; }
  } else {
    sel.value = value || '';
    if (other) other.style.display = 'none';
  }
}

function getCityValue(prefix) {
  const sel = document.getElementById(`${prefix}-city`);
  if (!sel) return '';
  if (sel.value === '__other__') {
    const other = document.getElementById(`${prefix}-city-other`);
    return other ? other.value.trim() : '';
  }
  return sel.value;
}

// ===== Brand-colored category icons (replace multicolor emoji everywhere) =====
const CATEGORY_ICON_PATHS = {
  restaurants: '<path d="M6 2v6c0 1.1.9 2 2 2s2-.9 2-2V2"/><path d="M8 10v12"/><path d="M17 2v20"/><path d="M14 2c0 3 1 5 3 5s3-2 3-5"/>',
  cafes: '<path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8z"/><path d="M17 9h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 2c0 1-1 1-1 2s1 1 1 2"/><path d="M12 2c0 1-1 1-1 2s1 1 1 2"/>',
  grocery: '<path d="M3 8h18l-2 11a2 2 0 0 1-2 1.7H7A2 2 0 0 1 5 19L3 8z"/><path d="M8 8 6 3"/><path d="M16 8l2-5"/><path d="M9 12v5"/><path d="M15 12v5"/>',
  clothing: '<path d="M8 3 4 6l2 3 2-1v11h8V8l2 1 2-3-4-3-2 2h-4L8 3z"/>',
  electronics: '<rect x="7" y="2" width="10" height="20" rx="2"/><line x1="11" y1="18" x2="13" y2="18"/>',
  salons: '<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><line x1="20" y1="4" x2="8.5" y2="15.5"/><line x1="8.5" y1="8.5" x2="20" y2="20"/>',
  pharmacies: '<rect x="9" y="3" width="6" height="18" rx="1.5"/><rect x="3" y="9" width="18" height="6" rx="1.5"/>',
  hotels: '<path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M3 18v2"/><path d="M21 18v2"/><path d="M3 12V8a2 2 0 0 1 2-2h4v4"/><circle cx="7" cy="8" r="1.3"/>',
  repair: '<path d="M14.7 6.3a4 4 0 1 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.8 2.8-2-2 2.8-2.8z"/>',
  education: '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="M6 10.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/>',
  hospitals: '<circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/>',
  sports: '<path d="M6 7v10"/><path d="M4 9v6"/><path d="M18 7v10"/><path d="M20 9v6"/><path d="M6 12h12"/>',
  'information-technology': '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/><path d="M7 9l3 2-3 2M13 13h4"/>',
  bakery: '<path d="M4 11a8 4 0 0 1 16 0v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M9 11v8M15 11v8"/>',
  'bars-pubs': '<path d="M4 4h16l-8 9-8-9z"/><path d="M12 13v7"/><path d="M8 20h8"/>',
  'gym-fitness': '<rect x="2" y="10" width="3" height="4"/><rect x="19" y="10" width="3" height="4"/><rect x="6" y="8" width="2" height="8"/><rect x="16" y="8" width="2" height="8"/><line x1="8" y1="12" x2="16" y2="12"/>',
  'banking-finance': '<path d="M3 10l9-6 9 6"/><path d="M4 10v9M9 10v9M15 10v9M20 10v9"/><path d="M3 21h18"/>',
  'real-estate': '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h4v-6h2v6h4a1 1 0 0 0 1-1v-9"/>',
  'travel-agency': '<path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2.5 1.5V22l4-1 4 1v-1.5L13 19v-5.5z"/>',
  photography: '<rect x="2" y="7" width="20" height="14" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M8 7l2-3h4l2 3"/>',
  laundry: '<rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="13" r="6"/><circle cx="12" cy="13" r="2.5"/><circle cx="7" cy="5" r="0.8" fill="currentColor" stroke="none"/><circle cx="10" cy="5" r="0.8" fill="currentColor" stroke="none"/>',
  furniture: '<path d="M5 11V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v5"/><path d="M3 11h18v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M5 18v3M19 18v3"/>',
  hardware: '<path d="M15 4l5 5-3 3-5-5z"/><path d="M13 8 3 18l3 3 10-10"/>',
  jewelry: '<path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M9 3l3 6-3 12M15 3l-3 6 3 12"/>',
  bookstore: '<path d="M12 6c-2-1.5-5-2-8-1v13c3-1 6-0.5 8 1 2-1.5 5-2 8-1V5c-3-1-6-0.5-8 1z"/><path d="M12 6v13"/>',
  'pet-store': '<circle cx="7" cy="8" r="1.6"/><circle cx="12" cy="6" r="1.6"/><circle cx="17" cy="8" r="1.6"/><path d="M12 12c-3 0-5.5 2-5.5 4.5S9 21 12 21s5.5-2 5.5-4.5S15 12 12 12z"/>',
  florist: '<circle cx="12" cy="8" r="2.2"/><circle cx="8" cy="12" r="2.2"/><circle cx="16" cy="12" r="2.2"/><circle cx="12" cy="14" r="2.2"/><path d="M12 16v6"/>',
  'event-planning': '<path d="M12 2a5 5 0 0 1 5 5c0 3-2 5-5 8-3-3-5-5-5-8a5 5 0 0 1 5-5z"/><path d="M12 15v7"/>',
  insurance: '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
  'legal-services': '<path d="M12 3v18M5 8l-3 6a3 3 0 0 0 6 0zM19 8l-3 6a3 3 0 0 0 6 0z"/><path d="M5 8h14M8 21h8"/>',
  accounting: '<rect x="4" y="2" width="16" height="20" rx="2"/><rect x="7" y="5" width="10" height="4"/><circle cx="8" cy="13" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="13" r="1" fill="currentColor" stroke="none"/><circle cx="16" cy="13" r="1" fill="currentColor" stroke="none"/><circle cx="8" cy="17" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="17" r="1" fill="currentColor" stroke="none"/><circle cx="16" cy="17" r="1" fill="currentColor" stroke="none"/>',
  veterinary: '<circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/>',
  'dental-clinic': '<path d="M8 3c-2.5 0-4 2-4 4.5 0 3 1 5.5 1.5 8 .3 1.5 1 2.5 2 2.5s1.5-2 2-3.5c.2-.6.3-1 .5-1s.3.4.5 1c.5 1.5 1 3.5 2 3.5s1.7-1 2-2.5c.5-2.5 1.5-5 1.5-8 0-2.5-1.5-4.5-4-4.5-1 0-1.7.5-2 1-.3-.5-1-1-2-1z"/>',
  opticians: '<circle cx="6" cy="14" r="3.5"/><circle cx="18" cy="14" r="3.5"/><path d="M9.5 14h5M2 12l1.5-4h2M22 12l-1.5-4h-2"/>',
  tailors: '<circle cx="12" cy="12" r="8"/><path d="M8 9c2 1 6 1 8 0M8 15c2-1 6-1 8 0"/>',
  'printing-copy': '<path d="M6 9V3h12v6"/><rect x="4" y="9" width="16" height="8" rx="1.5"/><path d="M6 17v4h12v-4"/>',
  'car-dealership': '<path d="M3 13l1.5-5A2 2 0 0 1 6.4 6.5h11.2A2 2 0 0 1 19.5 8L21 13"/><rect x="2" y="13" width="20" height="5" rx="1.5"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
  'gas-station': '<rect x="3" y="4" width="10" height="17" rx="1.5"/><path d="M6 8h4"/><path d="M13 9h3a2 2 0 0 1 2 2v6a1.5 1.5 0 0 0 3 0V8l-3-3"/>',
  'transport-taxi': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M12 3v7M6 16l4.5-2.5M18 16l-4.5-2.5"/>',
  'courier-logistics': '<path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/>',
  'spa-wellness': '<path d="M12 21c-4-3-7-7-7-11a7 7 0 0 1 14 0c0 4-3 8-7 11z"/><path d="M12 10v11"/>',
  'tattoo-piercing': '<path d="M4 20l6-6M14 4l6 6-9 9-4-4z"/><circle cx="8" cy="16" r="1" fill="currentColor" stroke="none"/>',
  'music-school': '<path d="M9 18V4l10-2v14"/><circle cx="7" cy="18" r="2.2"/><circle cx="17" cy="16" r="2.2"/>',
  'art-craft': '<path d="M12 2a10 10 0 1 0 0 20c1.5 0 2.5-1 2.5-2.3 0-.6-.3-1.1-.3-1.7 0-1 .8-1.5 1.8-1.5H18a4 4 0 0 0 4-4c0-5.5-4.5-10.5-10-10.5z"/><circle cx="7.5" cy="10.5" r="1.2" fill="currentColor" stroke="none"/><circle cx="11" cy="7" r="1.2" fill="currentColor" stroke="none"/><circle cx="15.5" cy="8" r="1.2" fill="currentColor" stroke="none"/>',
  'toy-store': '<rect x="4" y="9" width="16" height="11" rx="2"/><circle cx="9" cy="14" r="1.3" fill="currentColor" stroke="none"/><circle cx="15" cy="14" r="1.3" fill="currentColor" stroke="none"/><path d="M9 17.5h6"/><path d="M12 9V5M9 5h6"/>',
  'mobile-telecom': '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M10 18h4"/><path d="M3 14a9 9 0 0 1 3-6M21 14a9 9 0 0 0-3-6"/>',
  'cinema-entertainment': '<path d="M3 9l1.5-4h14L20 9"/><rect x="3" y="9" width="18" height="12" rx="1.5"/><path d="M3 9l3-4M9 9l3-4M15 9l3-4"/>',
  'night-clubs': '<circle cx="12" cy="10" r="6"/><path d="M12 4V2M12 16v6M6 10H2M22 10h-4"/><path d="M7.8 5.8 6.3 4.3M18.2 5.8l1.5-1.5M7.8 14.2l-1.5 1.5M18.2 14.2l1.5 1.5"/>',
  catering: '<path d="M6 2v6c0 1.1.9 2 2 2s2-.9 2-2V2"/><path d="M8 10v12"/><path d="M17 2v20"/><path d="M14 2c0 3 1 5 3 5s3-2 3-5"/>',
  agriculture: '<path d="M12 22V10"/><path d="M12 10c-4 0-6-3-6-7 4 0 6 2 6 7z"/><path d="M12 10c4 0 6-3 6-7-4 0-6 2-6 7z"/>',
  construction: '<path d="M4 18a8 8 0 0 1 16 0z"/><path d="M2 18h20"/><path d="M12 6v4"/>',
  'interior-design': '<rect x="3" y="3" width="18" height="6" rx="1.5"/><rect x="7" y="9" width="3" height="10" rx="1"/>',
  'cleaning-services': '<path d="M14 3l-3 6"/><path d="M9 21l4-9 6-6"/><path d="M6 21l3-6 3 3"/>',
  'security-services': '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  daycare: '<circle cx="12" cy="13" r="6"/><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="9.5" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="14.5" cy="12" r="1" fill="currentColor" stroke="none"/><path d="M10 16c1 1 3 1 4 0"/>',
  'ngo-nonprofit': '<path d="M12 21s-7-4.35-9.5-8.5C.5 8.5 3 4.5 7 4.5c2 0 3.5 1 5 2.5 1.5-1.5 3-2.5 5-2.5 4 0 6.5 4 4.5 8-2.5 4.15-9.5 8.5-9.5 8.5z"/>',
  'government-services': '<path d="M3 21h18"/><path d="M5 21V10l7-6 7 6v11"/><path d="M10 21v-6h4v6"/>',
  'religious-temple': '<path d="M12 2 4 8h16z"/><path d="M6 8v13M18 8v13M3 21h18"/><path d="M10 21v-5h4v5"/>',
  'wedding-planners': '<circle cx="9" cy="14" r="5"/><circle cx="15" cy="14" r="5"/>',
  'driving-school': '<path d="M3 13l1.5-5A2 2 0 0 1 6.4 6.5h11.2A2 2 0 0 1 19.5 8L21 13"/><rect x="2" y="13" width="20" height="5" rx="1.5"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
  'coaching-centers': '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="M6 10.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/>',
  'cosmetics-beauty': '<rect x="9" y="10" width="6" height="10" rx="1"/><path d="M10 10 9 4h6l-1 6"/>',
  'motorcycle-bike': '<circle cx="6" cy="17" r="3.5"/><circle cx="18" cy="17" r="3.5"/><path d="M6 17l4-9h4l3 9M10 8h3"/>',
  default: '<path d="M3 9l1-5h16l1 5"/><path d="M3 9v10a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9"/><path d="M3 9h18"/><path d="M9 20v-6h6v6"/>',
};

function categoryIcon(slug, sizePx = 24, color = 'var(--saffron)') {
  const inner = CATEGORY_ICON_PATHS[slug] || CATEGORY_ICON_PATHS.default;
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color:${color};vertical-align:middle;">${inner}</svg>`;
}

// ===== Brand-colored UI icons (replace multicolor emoji in nav/tabs) =====
const UI_ICON_PATHS = {
  menu: '<path d="M6 7h12l1 13H5L6 7z"/><path d="M9 7a3 3 0 0 1 6 0"/>',
  about: '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4.5"/><circle cx="12" cy="8" r="0.9" fill="currentColor" stroke="none"/>',
  gallery: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15.5 16 10l-4.5 5-2-2L3 18.5"/>',
  reviews: '<path d="M12 3 14.5 9.5 21 10 16 14.3 17.5 21 12 17.3 6.5 21 8 14.3 3 10 9.5 9.5 12 3z"/>',
  location: '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.3"/>',
  chart: '<path d="M5 20V12"/><path d="M12 20V6"/><path d="M19 20v-9"/><path d="M3 20h18"/>',
  box: '<path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/>',
  shop: '<path d="M3 9l1-5h16l1 5"/><path d="M3 9v10a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9"/><path d="M9 20v-6h6v6"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
  branch: '<circle cx="6" cy="6" r="2.3"/><circle cx="18" cy="6" r="2.3"/><circle cx="6" cy="18" r="2.3"/><path d="M6 8.3V18"/><path d="M18 8.3a6 6 0 0 1-6 6H8"/>',
  plus: '<path d="M12 5v14"/><path d="M5 12h14"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
  lock: '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  logout: '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/>',
  photo: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 15.5 16 10l-4.5 5-2-2L3 18.5"/>',
  message: '<path d="M4 4h16v12H8l-4 4V4z"/>',
  user: '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.5 3-6 7-6s7 2.5 7 6"/>',
  heart: '<path d="M12 21s-7-4.35-9.5-8.5C.5 8.5 3 4.5 7 4.5c2 0 3.5 1 5 2.5 1.5-1.5 3-2.5 5-2.5 4 0 6.5 4 4.5 8-2.5 4.15-9.5 8.5-9.5 8.5z"/>',
  bell: '<path d="M6 8a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M9.5 20a2.5 2.5 0 0 0 5 0"/>',
  home: '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h4v-6h2v6h4a1 1 0 0 0 1-1v-9"/>',
  pause: '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
  play: '<path d="M6 4l14 8-14 8V4z"/>',
  arrow: '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
  phone: '<path d="M13.4 15.6 15 14a1 1 0 0 1 1.1-.2 12 12 0 0 0 3.4.9 1 1 0 0 1 .9 1V19a1 1 0 0 1-1 1A16 16 0 0 1 3 4a1 1 0 0 1 1-1h3.3a1 1 0 0 1 1 .9c.1 1.2.4 2.3.9 3.4a1 1 0 0 1-.2 1.1L7.6 10.6a10.6 10.6 0 0 0 5.8 5.8z"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
  cart: '<circle cx="9" cy="20" r="1.3"/><circle cx="18" cy="20" r="1.3"/><path d="M3 4h2l2.4 12.2a2 2 0 0 0 2 1.6h8.4a2 2 0 0 0 2-1.6L21 8H6"/>',
  directions: '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><path d="M9.5 9.5h5l-2-2m2 2-2 2"/>',
  web: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18"/><path d="M12 3a14 14 0 0 0 0 18"/>',
  facebook: '<path d="M14 9h3V6h-3a4 4 0 0 0-4 4v2H7v3h3v6h3v-6h3l1-3h-4v-2a1 1 0 0 1 1-1z"/>',
  instagram: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1"/>',
  compass: '<circle cx="12" cy="12" r="9"/><path d="M15.8 8.2L13.9 13.9L8.2 15.8L10.1 10.1Z"/>',
  crown: '<path d="M3 8l3 3 3-5 3 5 3-5 3 5 3-3v9H3V8z"/><path d="M4 20h16"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  chevronLeft: '<path d="M15 5l-7 7 7 7"/>',
  chevronRight: '<path d="M9 5l7 7-7 7"/>',
  chevronDown: '<path d="M5 9l7 7 7-7"/>',
  starFilled: '<path d="M12 2.5l3 6.6 7.2.9-5.3 4.9 1.4 7.1L12 18.2l-6.3 3.8 1.4-7.1-5.3-4.9 7.2-.9z" fill="currentColor" stroke="none"/>',
  more: '<circle cx="5" cy="12" r="1.8" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.8" fill="currentColor" stroke="none"/>',
  megaphone: '<path d="M3 10v4h3l6 4V6l-6 4H3z"/><path d="M15 9a3 3 0 0 1 0 6"/>',
  filter: '<path d="M4 5h16l-6 7.5V19l-4 2v-8.5z"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
  card: '<rect x="2" y="5" width="20" height="14" rx="2.2"/><line x1="2" y1="10" x2="22" y2="10"/><line x1="5.5" y1="14.5" x2="9.5" y2="14.5"/>',
  wifi: '<path d="M2 8.5a16 16 0 0 1 20 0"/><path d="M5.5 12.3a11 11 0 0 1 13 0"/><path d="M9 16a6 6 0 0 1 6 0"/><circle cx="12" cy="19.3" r="1" fill="currentColor" stroke="none"/>',
  truck: '<rect x="1" y="7" width="13" height="9" rx="1.2"/><path d="M14 10.5h4l3 2.8V16h-7z"/><circle cx="5.5" cy="18" r="1.6"/><circle cx="17.5" cy="18" r="1.6"/>',
  parking: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 16.5V7.5h3.6a3 3 0 0 1 0 6H9"/>',
  smoking: '<path d="M2 15h13v3H2z"/><path d="M15 15h3v3h-3z"/><path d="M17 8.5c1 1 1 2.5 0 3.5M20 8.5c1 1 1 2.5 0 3.5"/>',
};

function uiIcon(name, sizePx = 18) {
  const inner = UI_ICON_PATHS[name] || '';
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color:var(--saffron);vertical-align:middle;">${inner}</svg>`;
}

function coloredIcon(name, sizePx = 18, color = 'var(--saffron)') {
  const inner = UI_ICON_PATHS[name] || '';
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color:${color};vertical-align:middle;">${inner}</svg>`;
}

// Inherits color from parent (no inline color) — use when the icon's color must react to a CSS class toggle.
function plainIcon(name, sizePx = 18) {
  const inner = UI_ICON_PATHS[name] || '';
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;">${inner}</svg>`;
}

const Auth = {
  getToken: () => localStorage.getItem('access_token'),
  getRefresh: () => localStorage.getItem('refresh_token'),
  setTokens: (access, refresh) => {


    localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
  },
  clearTokens: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  getUser: () => { try { return JSON.parse(localStorage.getItem('user') || 'null'); } catch { return null; } },
  setUser: (u) => localStorage.setItem('user', JSON.stringify(u)),
  isLoggedIn: () => !!localStorage.getItem('access_token'),
};

const http = {
  async request(method, endpoint, data = null, isForm = false) {
    const headers = {};
    if (Auth.getToken()) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    if (!isForm) headers['Content-Type'] = 'application/json';
    const config = { method, headers };
    if (data) config.body = isForm ? data : JSON.stringify(data);
    let resp;
    try { resp = await fetch(`${API_BASE}${endpoint}`, config); }
    catch { return { ok: false, status: 0, data: { error: 'Could not reach the server. Check your connection and try again.', detail: 'Could not reach the server. Check your connection and try again.' } }; }
    if (resp.status === 401 && Auth.getRefresh()) {
      let r;
      try {
        r = await fetch(`${API_BASE}/auth/token/refresh/`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: Auth.getRefresh() }),
        });
      } catch { return { ok: false, status: 0, data: { error: 'Could not reach the server. Check your connection and try again.', detail: 'Could not reach the server. Check your connection and try again.' } }; }
      if (r.ok) {
        const { access } = await r.json();
        Auth.setTokens(access, null);
        headers['Authorization'] = `Bearer ${access}`;
        config.headers = headers;
        try { resp = await fetch(`${API_BASE}${endpoint}`, config); }
        catch { return { ok: false, status: 0, data: { error: 'Could not reach the server. Check your connection and try again.', detail: 'Could not reach the server. Check your connection and try again.' } }; }
      } else { Auth.clearTokens(); window.location.href = '/login/'; return { ok: false, status: 401, data: null }; }
    }
    const result = { status: resp.status, ok: resp.ok };
    try { result.data = await resp.json(); } catch { result.data = resp.ok ? null : { error: `Server error (${resp.status}).`, detail: `Server error (${resp.status}).` }; }
    return result;
  },
  get: (ep) => http.request('GET', ep),
  post: (ep, d, f) => http.request('POST', ep, d, f),
  put: (ep, d, f) => http.request('PUT', ep, d, f),
  patch: (ep, d, f) => http.request('PATCH', ep, d, f),
  delete: (ep) => http.request('DELETE', ep),
};

// Renders a "Sign in with Google" button into `buttonId` and routes successful
// sign-ins through the same token/redirect flow as normal login/register.
// `getRole` (optional) is called at click time to pick the role for new accounts.
function initGoogleSignIn(buttonId, getRole) {
  if (!window.google?.accounts?.id) return;
  google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: async (resp) => {
      const role = getRole ? getRole() : undefined;
      const apiResp = await API.googleAuth(resp.credential, role);
      if (apiResp.ok) {
        Auth.setTokens(apiResp.data.access, apiResp.data.refresh);
        Auth.setUser(apiResp.data.user);
        UI.toast('Welcome to Bazaar! 🎉', 'success');
        setTimeout(() => {
          window.location.href = apiResp.data.user.role === 'business_owner' ? '/business-dashboard/' : '/';
        }, 600);
      } else {
        UI.toast(apiResp.data?.error || 'Google sign-in failed', 'error');
      }
    },
  });
  google.accounts.id.renderButton(document.getElementById(buttonId), { theme: 'outline', size: 'large', width: 320 });
}

// Helper to build FormData from an object (needed for file uploads)
function toFormData(obj) {
  const fd = new FormData();
  Object.entries(obj).forEach(([key, val]) => {
    if (val === null || val === undefined || val === '') return;
    fd.append(key, val);
  });
  return fd;
}

const API = {
  login: (email, password) => http.post('/auth/login/', { email, password }),
  register: (data) => http.post('/auth/register/', data),
  googleAuth: (credential, role) => http.post('/auth/google/', { credential, role }),
  logout: () => http.post('/auth/logout/', { refresh: Auth.getRefresh() }),
  getProfile: () => http.get('/auth/profile/'),
  updateProfile: (data) => http.put('/auth/profile/', data),
  changePassword: (data) => http.post('/auth/profile/change-password/', data),
  getSavedBusinesses: () => http.get('/auth/saved-businesses/'),
  toggleSave: (id) => http.post(`/auth/saved-businesses/${id}/toggle/`),
  getBusinesses: (params = {}) => http.get(`/businesses/?${new URLSearchParams(params)}`),
  getBusiness: (slug) => http.get(`/businesses/${slug}/`),
  getFeatured: () => http.get('/businesses/featured/'),
  getAdvertisements: () => http.get('/businesses/advertisements/'),
  getNearby: (lat, lon, radius = 5) => http.get(`/businesses/nearby/?lat=${lat}&lon=${lon}&radius=${radius}`),
  getCategories: () => http.get('/businesses/categories/'),
  getMyBusinesses: () => http.get('/businesses/my/'),
  createBusiness: (data) => http.post('/businesses/my/', data),
  updateBusiness: (slug, data) => http.put(`/businesses/my/${slug}/`, data),
  uploadBusinessImages: (slug, formData) => http.patch(`/businesses/my/${slug}/`, formData, true),
  getGallery: (slug) => http.get(`/businesses/my/${slug}/gallery/`),
  addGalleryPhoto: (slug, formData) => http.post(`/businesses/my/${slug}/gallery/`, formData, true),
  deleteGalleryPhoto: (id) => http.delete(`/businesses/gallery/${id}/`),
  getBusinessHours: (slug) => http.get(`/businesses/my/${slug}/hours/`),
  saveBusinessHours: (slug, data) => http.post(`/businesses/my/${slug}/hours/`, data),
  getAnalytics: (slug) => http.get(`/businesses/my/${slug}/analytics/`),
  getProducts: (slug) => http.get(`/products/${slug}/products/`),
  getMyProducts: (slug) => http.get(`/products/${slug}/products/manage/`),
  createProduct: (slug, formData) => http.post(`/products/${slug}/products/manage/`, formData, true),
  updateProduct: (id, data) => http.patch(`/products/products/${id}/`, data, typeof FormData !== 'undefined' && data instanceof FormData),
  deleteProduct: (id) => http.delete(`/products/products/${id}/`),
  getProductCategories: (slug) => http.get(`/products/${slug}/categories/`),
  createProductCategory: (slug, data) => http.post(`/products/${slug}/categories/`, data),
  updateProductCategory: (id, data) => http.patch(`/products/categories/${id}/`, data),
  deleteProductCategory: (id) => http.delete(`/products/categories/${id}/`),
  getOrders: () => http.get('/orders/'),
  getOrder: (id) => http.get(`/orders/${id}/`),
  createOrder: (data) => http.post('/orders/', data),
  getBusinessOrders: (slug) => http.get(`/orders/business/${slug}/`),
  updateOrderStatus: (slug, id, status) => http.patch(`/orders/business/${slug}/${id}/`, { status }),
  getReviews: (slug) => http.get(`/reviews/${slug}/reviews/`),
  createReview: (slug, data) => http.post(`/reviews/${slug}/reviews/`, data),
  replyReview: (id, reply) => http.post(`/reviews/${id}/reply/`, { reply }),
  getNotifications: () => http.get('/notifications/'),
  markAllRead: () => http.post('/notifications/read-all/'),
  markRead: (id) => http.post(`/notifications/${id}/read/`),
};

const Cart = {
  _k: 'bazaar_cart',
  get() { try { return JSON.parse(localStorage.getItem(this._k) || '{"businessId":null,"businessName":"","items":[]}'); } catch { return { businessId: null, businessName: '', items: [] }; } },
  save(c) { localStorage.setItem(this._k, JSON.stringify(c)); },
  clear() { localStorage.removeItem(this._k); },
  add(product, businessId, businessName) {
    let cart = this.get();
    if (cart.businessId && cart.businessId !== businessId) {
      if (!confirm(`Your cart has items from "${cart.businessName}". Start a new cart from "${businessName}"?`)) return false;
      cart = { businessId, businessName, items: [] };
    }
    cart.businessId = businessId; cart.businessName = businessName;
    const ex = cart.items.find(i => i.id === product.id);
    if (ex) ex.qty++; else cart.items.push({ id: product.id, name: product.name, price: parseFloat(product.effective_price), image: product.image, qty: 1 });
    this.save(cart); return true;
  },
  remove(id) { const c = this.get(); c.items = c.items.filter(i => i.id !== id); if (!c.items.length) c.businessId = null; this.save(c); },
  updateQty(id, qty) { const c = this.get(); const item = c.items.find(i => i.id === id); if (item) { if (qty <= 0) return this.remove(id); item.qty = qty; this.save(c); } },
  get total() { return this.get().items.reduce((s, i) => s + (i.price * i.qty), 0); },
  get count() { return this.get().items.reduce((s, i) => s + i.qty, 0); },
};

const Location = {
  get() { try { return JSON.parse(sessionStorage.getItem('user_location') || 'null'); } catch { return null; } },
  set(c) { sessionStorage.setItem('user_location', JSON.stringify(c)); },
  detect() {
    return new Promise((res, rej) => {
      if (!navigator.geolocation) return rej(new Error('Not supported'));
      navigator.geolocation.getCurrentPosition(
        pos => { const c = { lat: pos.coords.latitude, lon: pos.coords.longitude }; this.set(c); res(c); },
        rej, { timeout: 10000 }
      );
    });
  },
};

const UI = {
  toast(msg, type = 'default', dur = 3500) {
    let c = document.querySelector('.toast-container');
    if (!c) { c = document.createElement('div'); c.className = 'toast-container'; document.body.appendChild(c); }
    const t = document.createElement('div');
    t.className = `toast toast-${type}`; t.innerHTML = `<span>${msg}</span>`;
    c.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(100%)'; t.style.transition = '0.3s'; setTimeout(() => t.remove(), 300); }, dur);
  },
  formatPrice: (p) => `Rs. ${parseFloat(p).toLocaleString('en-NP', { minimumFractionDigits: 0 })}`,
  stars: (r) => { const f = Math.floor(r); return '★'.repeat(f) + (r % 1 >= 0.5 ? '½' : '') + '☆'.repeat(5 - f - (r % 1 >= 0.5 ? 1 : 0)); },
  formatDate: (d) => new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }),
  timeAgo: (d) => { const s = (Date.now() - new Date(d)) / 1000; if (s < 60) return 'just now'; if (s < 3600) return `${Math.floor(s/60)}m ago`; if (s < 86400) return `${Math.floor(s/3600)}h ago`; return `${Math.floor(s/86400)}d ago`; },
  loading: (el, n = 3) => { el.innerHTML = Array(n).fill('<div class="skeleton" style="height:240px;border-radius:18px;"></div>').join(''); },
};

// ===== Shared vb- navbar, used by index.html/business.html/search.html so all three match exactly =====
function setVbTheme(mode) {
  document.documentElement.setAttribute('data-theme', mode);
  localStorage.setItem('vb_theme', mode);
  const btn = document.getElementById('vb-theme-btn');
  if (btn) btn.innerHTML = mode === 'light' ? plainIcon('moon', 15) : plainIcon('sun', 15);
}

function toggleVbTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  setVbTheme(current === 'light' ? 'dark' : 'light');
}

function renderVbNavbar(mountId, opts = {}) {
  const { exploreActive = false, searchValue = '' } = opts;
  const mount = document.getElementById(mountId);
  if (!mount) return;
  const user = Auth.getUser();
  const initials = user ? (((user.first_name?.[0]||'')+(user.last_name?.[0]||'')).toUpperCase() || (user.email?.[0]||'U').toUpperCase()) : 'U';
  mount.innerHTML = `
    <div class="vb-nav-left">
      <a href="/" class="vb-brand"><span class="vb-brand-icon"><img src="/images/icon-192.png" alt="V-Bazaar" style="width:100%;height:100%;object-fit:cover;border-radius:inherit;"></span><span class="vb-brand-text"> V-Bazaar</span></a>
      <a href="/search/" class="vb-explore-pill${exploreActive ? ' active' : ''}">${plainIcon('compass',15)} <span>Explore</span></a>
    </div>
    <div class="vb-nav-center">
      <div class="vb-search-pill">
        ${plainIcon('search',16)}
        <input type="text" id="vb-nav-search-input" value="${searchValue}" placeholder="Search business near you !!!" onkeydown="if(event.key==='Enter')window.location.href='/search/?q='+encodeURIComponent(this.value)">
      </div>
    </div>
    <div class="vb-nav-right">
      <button class="vb-theme-btn" id="vb-theme-btn" onclick="toggleVbTheme()" title="Toggle theme"></button>
      <span data-guest-only class="vb-guest-actions">
        <a href="/login/" class="nav-link">Log in</a>
        <a href="/register/" class="btn-nav">Sign up</a>
      </span>
      <a data-guest-only href="/login/" class="vb-avatar-link" title="Log in"><span class="vb-avatar">${plainIcon('user',14)}</span></a>
      <span data-auth-required style="display:none;">
        <a href="/dashboard/#profile" class="vb-profile-pill"><span class="vb-avatar">${initials}</span><span class="vb-profile-text"> My Profile</span></a>
      </span>
    </div>`;
  setVbTheme(localStorage.getItem('vb_theme') || 'light');
  document.querySelectorAll('[data-auth-required]').forEach(el => el.style.display = user ? '' : 'none');
  document.querySelectorAll('[data-guest-only]').forEach(el => el.style.display = user ? 'none' : '');
}

// ===== Shared vb- business card, used by index.html/business.html/search.html =====
function renderVbCard(b, featured, lat, lon) {
  const dist = lat && lon && b.latitude ? calcDistance(lat, lon, b.latitude, b.longitude) : null;
  const rating = b.average_rating > 0 ? parseFloat(b.average_rating).toFixed(1) : null;
  const distText = dist !== null ? (dist < 1 ? (dist*1000).toFixed(0)+'m' : dist.toFixed(1)+'km') : '';
  return `<div class="vb-card ${featured ? 'vb-card-featured' : ''}" onclick="window.location.href='/business/?slug=${b.slug}'">
    <div class="vb-card-img">
      ${b.banner ? `<img src="${b.banner}" alt="${b.name}" loading="lazy">` : `<div style="width:100%;height:100%;background:linear-gradient(135deg,var(--saffron-light),#FDE0C8);"></div>`}
      ${featured ? `<span class="vb-badge vb-badge-gold">${plainIcon('starFilled',11)} Featured</span>` : ''}
      <button class="vb-save-btn ${b.is_saved ? 'saved' : ''}" onclick="event.stopPropagation();handleToggleSave(${b.id},this)">${plainIcon('heart',15)}</button>
    </div>
    <div class="vb-card-body">
      <div class="vb-card-category">${b.category_name || 'Business'}</div>
      <div class="vb-card-title-row">
        <span class="vb-card-title">${b.name}${b.is_verified ? coloredIcon('about',14,'var(--saffron)') : ''}</span>
        ${rating ? `<span class="vb-rating-badge">${plainIcon('starFilled',11)} ${rating}</span>` : ''}
      </div>
      <div class="vb-card-address">${plainIcon('location',13)} ${b.city || ''}</div>
      <div class="vb-card-actions">
        <a href="tel:${b.phone || ''}" class="vb-act-btn" onclick="event.stopPropagation()" title="Call">${plainIcon('phone',14)}</a>
        <a href="${b.phone ? 'https://wa.me/'+b.phone.replace(/\D/g,'') : '#'}" target="_blank" class="vb-act-btn" onclick="event.stopPropagation()" title="Message">${plainIcon('message',14)}</a>
        <a href="https://www.google.com/maps/dir/?api=1&destination=${b.latitude},${b.longitude}" target="_blank" class="vb-act-btn ${distText ? 'vb-act-btn-wide' : ''}" onclick="event.stopPropagation()" title="Directions">${plainIcon('directions',14)}${distText ? ` <span style="font-size:0.72rem;font-weight:600;">${distText}</span>` : ''}</a>
      </div>
    </div>
  </div>`;
}

function calcDistance(lat1, lon1, lat2, lon2) {
  const R = 6371, dL = (lat2 - lat1) * Math.PI / 180, dN = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dL/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dN/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function renderBusinessCard(b, lat = null, lon = null) {
  const dist = lat && lon && b.latitude ? calcDistance(lat, lon, b.latitude, b.longitude) : null;
  const stars = b.average_rating > 0 ? `<span class="stars">${UI.stars(b.average_rating)}</span> <span>${parseFloat(b.average_rating).toFixed(1)}</span> <span class="count">(${b.total_reviews})</span>` : '<span class="count">No reviews yet</span>';
  return `<div class="business-card" onclick="window.location.href='/business/?slug=${b.slug}'">
    <div class="card-banner">
      ${b.banner ? `<img src="${b.banner}" alt="${b.name}" loading="lazy">` : `<div style="width:100%;height:100%;background:linear-gradient(135deg,#FFF0E8,#FDE8D0);"></div>`}
      ${b.is_open !== null ? `<div class="card-badge"><span class="${b.is_open ? 'badge-open' : 'badge-closed'}">●</span> ${b.is_open ? 'Open' : 'Closed'}</div>` : ''}
      <button class="card-save-btn ${b.is_saved ? 'saved' : ''}" onclick="event.stopPropagation();handleToggleSave(${b.id},this)">♥</button>
      <div class="card-logo">${b.logo ? `<img src="${b.logo}" alt="">` : categoryIcon(b.category_slug)}</div>
    </div>
    <div class="card-body">
      <div class="card-category">${b.category_name || 'Business'}</div>
      <div class="card-title">${b.name}</div>
      <div class="card-location">📍 ${b.city || ''}</div>
      <div class="card-footer">
        <div class="card-rating">${stars}</div>
        ${dist ? `<div class="card-distance">📍 ${dist < 1 ? (dist*1000).toFixed(0)+'m' : dist.toFixed(1)+'km'}</div>` : ''}
      </div>
    </div>
  </div>`;
}

function renderProductCard(p, businessId, businessName, categorySlug = null, acceptsOrders = true) {
  return `<div class="product-card">
    <div class="product-img">${p.image ? `<img src="${p.image}" alt="${p.name}" loading="lazy">` : categoryIcon(categorySlug, 32)}</div>
    <div class="product-body">
      <div class="product-name">${p.name}</div>
      ${p.description ? `<div class="product-desc">${p.description.substring(0,80)}...</div>` : ''}
      <div class="product-footer">
        <div class="product-price">${UI.formatPrice(p.effective_price)}</div>
        ${!acceptsOrders
          ? `<span style="font-size:0.75rem;color:var(--danger);font-weight:600;">Not accepting orders</span>`
          : p.is_available && p.in_stock
          ? `<button class="add-to-cart-btn" onclick='addToCart(${JSON.stringify(p)},${businessId},"${businessName}")'>+</button>`
          : `<span style="font-size:0.75rem;color:var(--danger);font-weight:600;">Out of Stock</span>`}
      </div>
    </div>
  </div>`;
}

function addToCart(product, businessId, businessName) {
  const ok = Cart.add(product, businessId, businessName);
  if (ok) { UI.toast(`${product.name} added to cart!`, 'success'); updateCartBadge(); if (typeof renderMiniCart === 'function') renderMiniCart(); }
}

async function handleToggleSave(id, btn) {
  if (!Auth.isLoggedIn()) { window.location.href = '/login/'; return; }
  const resp = await API.toggleSave(id);
  if (resp.ok) { btn.classList.toggle('saved', resp.data.saved); UI.toast(resp.data.saved ? 'Saved!' : 'Removed from saved'); }
}

function updateCartBadge() {
  const count = Cart.count;
  document.querySelectorAll('.cart-count').forEach(el => { el.textContent = count; el.style.display = count ? 'flex' : 'none'; });
}

async function doLogout() {
  await API.logout();
  Auth.clearTokens();
  window.location.href = '/';
}

document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  const user = Auth.getUser();
  document.querySelectorAll('[data-auth-required]').forEach(el => el.style.display = user ? '' : 'none');
  document.querySelectorAll('[data-guest-only]').forEach(el => el.style.display = user ? 'none' : '');
  if (user) document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = user.first_name || user.email);

  // Business owners can shop as customers too — show "My Business" link
  // in addition to the regular "Dashboard" (order history) link.
  if (user && user.role === 'business_owner') {
    document.querySelectorAll('[data-owner-only]').forEach(el => el.style.display = '');
  }
});

// ===== PWA: manifest/theme tags + service worker (applies site-wide via this shared script) =====
(function setupPWA() {
  if (!document.querySelector('link[rel="manifest"]')) {
    const link = document.createElement('link');
    link.rel = 'manifest';
    link.href = '/manifest.json';
    document.head.appendChild(link);
  }
  if (!document.querySelector('meta[name="theme-color"]')) {
    const meta = document.createElement('meta');
    meta.name = 'theme-color';
    meta.content = '#EE6C29';
    document.head.appendChild(meta);
  }
  if (!document.querySelector('link[rel="apple-touch-icon"]')) {
    const link = document.createElement('link');
    link.rel = 'apple-touch-icon';
    link.href = '/images/apple-touch-icon.png';
    document.head.appendChild(link);
  }
  if (!document.querySelector('link[rel="icon"]')) {
    const link = document.createElement('link');
    link.rel = 'icon';
    link.href = '/images/icon-192.png';
    document.head.appendChild(link);
  }
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    });
  }
})();

// ===== PWA install prompt — browsers don't reliably show their own banner,
// so capture the event and surface our own "Install App" bar. =====
(function setupInstallPrompt() {
  let deferredPrompt = null;

  function showInstallBar() {
    if (localStorage.getItem('pwa_install_dismissed')) return;
    if (document.getElementById('pwa-install-bar')) return;
    const bar = document.createElement('div');
    bar.id = 'pwa-install-bar';
    bar.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9998;background:var(--charcoal,#282B2B);color:white;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:0.75rem 1.25rem;font-family:var(--font-body,sans-serif);box-shadow:0 -4px 16px rgba(0,0,0,0.2);';
    bar.innerHTML = `
      <span style="font-size:0.85rem;">📲 Install V-Bazaar for quick access from your home screen</span>
      <span style="display:flex;gap:0.5rem;flex-shrink:0;">
        <button id="pwa-install-btn" style="background:var(--saffron,#EE6C29);color:white;border:none;padding:0.45rem 1rem;border-radius:999px;font-size:0.82rem;font-weight:600;cursor:pointer;">Install</button>
        <button id="pwa-install-dismiss" style="background:none;border:none;color:rgba(255,255,255,0.6);font-size:1.1rem;cursor:pointer;padding:0 0.4rem;">✕</button>
      </span>`;
    document.body.appendChild(bar);
    document.getElementById('pwa-install-btn').onclick = async () => {
      bar.remove();
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    };
    document.getElementById('pwa-install-dismiss').onclick = () => {
      bar.remove();
      localStorage.setItem('pwa_install_dismissed', '1');
    };
  }

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallBar();
  });

  window.addEventListener('appinstalled', () => {
    const bar = document.getElementById('pwa-install-bar');
    if (bar) bar.remove();
    localStorage.setItem('pwa_install_dismissed', '1');
  });
})();
