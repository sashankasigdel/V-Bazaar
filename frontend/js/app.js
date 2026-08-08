/* ===== BAZAAR — API Client ===== */
const API_BASE = ['localhost', '127.0.0.1'].includes(location.hostname)
  ? `${location.protocol}//${location.hostname}:8000/api`
  : 'https://v-bazaar.onrender.com/api';
const GOOGLE_CLIENT_ID = '866560142277-0htji2mqlg4r18395oqga97pln33420a.apps.googleusercontent.com';

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
  default: '<path d="M3 9l1-5h16l1 5"/><path d="M3 9v10a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9"/><path d="M3 9h18"/><path d="M9 20v-6h6v6"/>',
};

function categoryIcon(slug, sizePx = 24) {
  const inner = CATEGORY_ICON_PATHS[slug] || CATEGORY_ICON_PATHS.default;
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color:var(--saffron);vertical-align:middle;">${inner}</svg>`;
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
};

function uiIcon(name, sizePx = 18) {
  const inner = UI_ICON_PATHS[name] || '';
  return `<svg width="${sizePx}" height="${sizePx}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color:var(--saffron);vertical-align:middle;">${inner}</svg>`;
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
    meta.content = '#E8630A';
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
