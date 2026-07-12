
const galleryGrid = document.getElementById("galleryGrid");
const galleryFilters = document.getElementById("galleryFilters");
const galleryCounter = document.getElementById("galleryCounter");

const lightbox = document.getElementById("lightbox");
const lightboxImage = document.getElementById("lightboxImage");
const lightboxTitle = document.getElementById("lightboxTitle");
const lightboxPosition = document.getElementById("lightboxPosition");
const lightboxClose = document.getElementById("lightboxClose");
const lightboxPrev = document.getElementById("lightboxPrev");
const lightboxNext = document.getElementById("lightboxNext");

let products = [];
let activeCategory = "Wszystkie";
let currentImages = [];
let currentImageIndex = 0;
let currentTitle = "";

async function loadGallery() {
  try {
    const response = await fetch("data/gallery.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    products = await response.json();
    buildFilters();
    renderGallery();
  } catch (error) {
    console.error(error);
    galleryGrid.innerHTML = `
      <p class="gallery-empty">
        Nie udało się odczytać galerii. Uruchom skrypt tools/build_gallery.py
        lub opublikuj stronę przez dołączony workflow GitHub Pages.
      </p>`;
  }
}

function buildFilters() {
  const categories = ["Wszystkie", ...new Set(products.map(item => item.category))];
  galleryFilters.innerHTML = categories.map(category => `
    <button class="filter-button ${category === activeCategory ? "active" : ""}"
      type="button" data-category="${escapeHtml(category)}">
      ${escapeHtml(category)}
    </button>
  `).join("");

  galleryFilters.querySelectorAll("button").forEach(button => {
    button.addEventListener("click", () => {
      activeCategory = button.dataset.category;
      buildFilters();
      renderGallery();
    });
  });
}

function renderGallery() {
  const filtered = activeCategory === "Wszystkie"
    ? products
    : products.filter(item => item.category === activeCategory);

  galleryCounter.textContent = `${filtered.length} ${filtered.length === 1 ? "realizacja" : "realizacje"}`;

  if (!filtered.length) {
    galleryGrid.innerHTML = '<p class="gallery-empty">Brak realizacji w tej kategorii.</p>';
    return;
  }

  galleryGrid.innerHTML = filtered.map((item, index) => `
    <article class="gallery-card reveal visible" tabindex="0" role="button"
      data-index="${products.indexOf(item)}"
      aria-label="Otwórz galerię: ${escapeHtml(item.title)}">
      <img class="gallery-card-image" src="${item.cover}" alt="${escapeHtml(item.title)}" loading="lazy">
      <div class="gallery-card-content">
        <small>${escapeHtml(item.category)}</small>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.description || "")}</p>
      </div>
    </article>
  `).join("");

  galleryGrid.querySelectorAll(".gallery-card").forEach(card => {
    const open = () => openLightbox(Number(card.dataset.index), 0);
    card.addEventListener("click", open);
    card.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
  });
}

function openLightbox(productIndex, imageIndex) {
  const product = products[productIndex];
  currentImages = product.images;
  currentImageIndex = imageIndex;
  currentTitle = product.title;
  updateLightbox();
  lightbox.classList.add("open");
  lightbox.setAttribute("aria-hidden", "false");
  document.body.classList.add("no-scroll");
}

function updateLightbox() {
  lightboxImage.src = currentImages[currentImageIndex];
  lightboxImage.alt = `${currentTitle} — zdjęcie ${currentImageIndex + 1}`;
  lightboxTitle.textContent = currentTitle;
  lightboxPosition.textContent = `${currentImageIndex + 1} / ${currentImages.length}`;
}

function closeLightbox() {
  lightbox.classList.remove("open");
  lightbox.setAttribute("aria-hidden", "true");
  document.body.classList.remove("no-scroll");
}

function showPrevious() {
  currentImageIndex = (currentImageIndex - 1 + currentImages.length) % currentImages.length;
  updateLightbox();
}

function showNext() {
  currentImageIndex = (currentImageIndex + 1) % currentImages.length;
  updateLightbox();
}

lightboxClose.addEventListener("click", closeLightbox);
lightboxPrev.addEventListener("click", showPrevious);
lightboxNext.addEventListener("click", showNext);
lightbox.addEventListener("click", event => {
  if (event.target === lightbox) closeLightbox();
});

document.addEventListener("keydown", event => {
  if (!lightbox.classList.contains("open")) return;
  if (event.key === "Escape") closeLightbox();
  if (event.key === "ArrowLeft") showPrevious();
  if (event.key === "ArrowRight") showNext();
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadGallery();
