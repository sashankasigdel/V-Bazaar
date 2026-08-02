/* ===== BAZAAR — API Client ===== */
const API_BASE = 'https://v-bazaar.onrender.com/api';

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
    let resp = await fetch(`${API_BASE}${endpoint}`, config);
    if (resp.status === 401 && Auth.getRefresh()) {
      const r = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: Auth.getRefresh() }),
      });
      if (r.ok) {
        const { access } = await r.json();
        Auth.setTokens(access, null);
        headers['Authorization'] = `Bearer ${access}`;
        config.headers = headers;
        resp = await fetch(`${API_BASE}${endpoint}`, config);
      } else { Auth.clearTokens(); window.location.href = '/login/'; return; }
    }
    const result = { status: resp.status, ok: resp.ok };
    try { result.data = await resp.json(); } catch { result.data = null; }
    return result;
  },
  get: (ep) => http.request('GET', ep),
  post: (ep, d, f) => http.request('POST', ep, d, f),
  put: (ep, d, f) => http.request('PUT', ep, d, f),
  patch: (ep, d, f) => http.request('PATCH', ep, d, f),
  delete: (ep) => http.request('DELETE', ep),
};

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
  logout: () => http.post('/auth/logout/', { refresh: Auth.getRefresh() }),
  getProfile: () => http.get('/auth/profile/'),
  updateProfile: (data) => http.put('/auth/profile/', data),
  changePassword: (data) => http.post('/auth/profile/change-password/', data),
  getSavedBusinesses: () => http.get('/auth/saved-businesses/'),
  toggleSave: (id) => http.post(`/auth/saved-businesses/${id}/toggle/`),
  getBusinesses: (params = {}) => http.get(`/businesses/?${new URLSearchParams(params)}`),
  getBusiness: (slug) => http.get(`/businesses/${slug}/`),
  getFeatured: () => http.get('/businesses/featured/'),
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
      <div class="card-logo">${b.logo ? `<img src="${b.logo}" alt="">` : (b.category_icon || '🏪')}</div>
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

function renderProductCard(p, businessId, businessName) {
  return `<div class="product-card">
    <div class="product-img">${p.image ? `<img src="${p.image}" alt="${p.name}" loading="lazy">` : '🍽️'}</div>
    <div class="product-body">
      <div class="product-name">${p.name}</div>
      ${p.description ? `<div class="product-desc">${p.description.substring(0,80)}...</div>` : ''}
      <div class="product-footer">
        <div class="product-price">${UI.formatPrice(p.effective_price)}</div>
        ${p.is_available && p.in_stock
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
