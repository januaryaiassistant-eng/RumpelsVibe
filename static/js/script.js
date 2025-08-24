// =======================
// Elements
// =======================
const menuToggle = document.getElementById('menu-toggle');
const menuClose  = document.getElementById('menu-close');
const sidebar    = document.getElementById('sidebar');
const backdrop   = document.getElementById('backdrop');

// =======================
// Toggle helpers
// =======================
function openMenu() {
  sidebar.classList.add('open');
  backdrop.classList.add('show');
  menuToggle.classList.add('active');
  sidebar.setAttribute('aria-hidden', 'false');
  menuToggle.setAttribute('aria-expanded', 'true');
}

function closeMenu() {
  sidebar.classList.remove('open');
  backdrop.classList.remove('show');
  menuToggle.classList.remove('active');
  sidebar.setAttribute('aria-hidden', 'true');
  menuToggle.setAttribute('aria-expanded', 'false');
}

// Menu events
menuToggle.addEventListener('click', () => {
  const isOpen = sidebar.classList.contains('open');
  isOpen ? closeMenu() : openMenu();
});
menuClose.addEventListener('click', closeMenu);
backdrop.addEventListener('click', closeMenu);
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

// =======================
// Booking placeholder
// =======================
const reqBtn = document.getElementById('request-slot');
if (reqBtn) {
  reqBtn.addEventListener('click', () => {
    alert("Request sent! We'll email you shortly.");
  });
}

// =======================
// Footer year
// =======================
const yearEl = document.getElementById('year');
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

// =======================
// Hover Video Previews (Play on hover, pause on leave)
// =======================
document.querySelectorAll('.card').forEach(card => {
  const videoSrc = card.dataset.video; // from HTML data attribute
  const thumb = card.querySelector('.thumb');

  // Create video element once (not autoplay)
  const videoEl = document.createElement('video');
  videoEl.src = videoSrc;
  videoEl.muted = true;
  videoEl.loop = true;
  videoEl.playsInline = true;
  videoEl.preload = 'metadata'; // lighter preload
  videoEl.classList.add('card-video');
  videoEl.style.opacity = '0';
  videoEl.style.transition = 'opacity 0.3s ease';
  thumb.appendChild(videoEl);

  card.addEventListener('mouseenter', () => {
    videoEl.style.opacity = '1';
    videoEl.play(); // Start playing on hover
  });

  card.addEventListener('mouseleave', () => {
    videoEl.style.opacity = '0';
    videoEl.pause(); // Stop playing when not hovered
    videoEl.currentTime = 0; // Reset to start for consistency
  });
});
