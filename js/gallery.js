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
const modelModal = document.getElementById("modelModal");
const modelModalClose = document.getElementById("modelModalClose");
const modelModalTitle = document.getElementById("modelModalTitle");
const productModelViewer = document.getElementById("productModelViewer");
const modelProgressBar = document.getElementById("modelProgressBar");
const modelError = document.getElementById("modelError");
let products = [], activeCategory = "Wszystkie", currentImages = [], currentImageIndex = 0, currentTitle = "";
async function loadGallery(){try{const r=await fetch("data/gallery.json",{cache:"no-store"});if(!r.ok)throw new Error(`HTTP ${r.status}`);products=await r.json();buildFilters();renderGallery()}catch(e){console.error(e);galleryGrid.innerHTML='<p class="gallery-empty">Nie udało się odczytać galerii. Uruchom skrypt tools/build_gallery.py lub opublikuj stronę przez workflow GitHub Pages.</p>'}}
function buildFilters(){const categories=["Wszystkie",...new Set(products.map(i=>i.category))];galleryFilters.innerHTML=categories.map(c=>`<button class="filter-button ${c===activeCategory?"active":""}" type="button" data-category="${escapeHtml(c)}">${escapeHtml(c)}</button>`).join("");galleryFilters.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>{activeCategory=b.dataset.category;buildFilters();renderGallery()}))}
function renderGallery(){const filtered=activeCategory==="Wszystkie"?products:products.filter(i=>i.category===activeCategory);galleryCounter.textContent=`${filtered.length} ${filtered.length===1?"realizacja":"realizacje"}`;if(!filtered.length){galleryGrid.innerHTML='<p class="gallery-empty">Brak realizacji w tej kategorii.</p>';return}galleryGrid.innerHTML=filtered.map(item=>{const idx=products.indexOf(item),hasImages=Array.isArray(item.images)&&item.images.length>0,hasModel=Boolean(item.model);const visual=item.cover?`<img class="gallery-card-image" src="${item.cover}" alt="${escapeHtml(item.title)}" loading="lazy">`:`<div class="gallery-card-placeholder" aria-hidden="true"><span>3D</span></div>`;return `<article class="gallery-card reveal visible" data-index="${idx}">${visual}<div class="gallery-card-content"><small>${escapeHtml(item.category)}</small><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.description||"")}</p><div class="gallery-card-actions">${hasImages?`<button class="gallery-action gallery-action-images" type="button" data-product-index="${idx}">Zdjęcia</button>`:""}${hasModel?`<button class="gallery-action gallery-action-model" type="button" data-product-index="${idx}">Model 3D</button>`:""}</div></div></article>`}).join("");galleryGrid.querySelectorAll(".gallery-action-images").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();openLightbox(Number(b.dataset.productIndex),0)}));galleryGrid.querySelectorAll(".gallery-action-model").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();openModel(Number(b.dataset.productIndex))}))}
function openLightbox(productIndex,imageIndex){const p=products[productIndex];if(!p.images?.length)return;currentImages=p.images;currentImageIndex=imageIndex;currentTitle=p.title;updateLightbox();lightbox.classList.add("open");lightbox.setAttribute("aria-hidden","false");document.body.classList.add("no-scroll")}
function updateLightbox(){lightboxImage.src=currentImages[currentImageIndex];lightboxImage.alt=`${currentTitle} — zdjęcie ${currentImageIndex+1}`;lightboxTitle.textContent=currentTitle;lightboxPosition.textContent=`${currentImageIndex+1} / ${currentImages.length}`}
function closeLightbox(){lightbox.classList.remove("open");lightbox.setAttribute("aria-hidden","true");document.body.classList.remove("no-scroll")}
function showPrevious(){currentImageIndex=(currentImageIndex-1+currentImages.length)%currentImages.length;updateLightbox()}
function showNext(){currentImageIndex=(currentImageIndex+1)%currentImages.length;updateLightbox()}
lightboxClose.addEventListener("click",closeLightbox);lightboxPrev.addEventListener("click",showPrevious);lightboxNext.addEventListener("click",showNext);lightbox.addEventListener("click",e=>{if(e.target===lightbox)closeLightbox()});
function openModel(productIndex){const p=products[productIndex];if(!p.model)return;modelModalTitle.textContent=p.title;modelError.hidden=true;modelProgressBar.style.width="0%";productModelViewer.alt=`Model 3D: ${p.title}`;productModelViewer.src=p.model;modelModal.classList.add("open");modelModal.setAttribute("aria-hidden","false");document.body.classList.add("no-scroll")}
function closeModel(){modelModal.classList.remove("open");modelModal.setAttribute("aria-hidden","true");document.body.classList.remove("no-scroll");productModelViewer.removeAttribute("src");modelProgressBar.style.width="0%";modelError.hidden=true}
modelModalClose.addEventListener("click",closeModel);modelModal.addEventListener("click",e=>{if(e.target===modelModal)closeModel()});productModelViewer.addEventListener("progress",e=>{const p=Math.round((e.detail.totalProgress||0)*100);modelProgressBar.style.width=`${p}%`});productModelViewer.addEventListener("load",()=>{modelProgressBar.style.width="100%";setTimeout(()=>modelProgressBar.style.width="0%",450)});productModelViewer.addEventListener("error",e=>{console.error("Błąd model-viewer:",e);modelError.hidden=false});
document.addEventListener("keydown",e=>{if(modelModal.classList.contains("open")){if(e.key==="Escape")closeModel();return}if(!lightbox.classList.contains("open"))return;if(e.key==="Escape")closeLightbox();if(e.key==="ArrowLeft")showPrevious();if(e.key==="ArrowRight")showNext()});
function escapeHtml(v){return String(v).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}
loadGallery();
