/* ============================================
   KNOTS RUGS — Landing Page Scripts
   Hero Slider, Scroll Reveal, Interactions
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initHeroSlider();
    initScrollReveal();
    initStickyNav();
    initFeaturesMarquee();
    initProductsSlider();
    initSearchModal();
});


/* ==============================================
   PRODUCTS AUTO-SLIDER (2.8s per card)
   ============================================== */
function initProductsSlider() {
    const track = document.getElementById('products-track');
    if (!track) return;

    const cards = track.querySelectorAll('.products-slider__card');
    if (!cards.length) return;

    let currentIndex = 0;
    const totalCards = cards.length;
    const visibleCards = 4; // show 4 at a time

    function getCardWidth() {
        const card = cards[0];
        const style = getComputedStyle(track);
        const gap = parseFloat(style.gap) || 0;
        return card.offsetWidth + gap;
    }

    function slide() {
        currentIndex++;
        // When we've scrolled past the last visible set, snap back
        if (currentIndex > totalCards - visibleCards) {
            currentIndex = 0;
            // Instant reset (no transition)
            track.style.transition = 'none';
            track.style.transform = `translateX(0)`;
            // Force reflow then re-enable transition
            track.offsetHeight;
            track.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            return;
        }
        const offset = currentIndex * getCardWidth();
        track.style.transform = `translateX(-${offset}px)`;
    }

    setInterval(slide, 2800);
}


/* ==============================================
   FEATURES MARQUEE (seamless loop)
   ============================================== */
function initFeaturesMarquee() {
    const track = document.getElementById('features-track');
    if (!track) return;

    const originalSet = track.querySelector('.features-marquee__set');
    if (!originalSet) return;

    // Dynamically clone enough sets to always cover the full viewport width
    const setWidth = originalSet.offsetWidth;
    const clonesNeeded = Math.ceil(window.innerWidth / setWidth) + 1;

    for (let i = 0; i < clonesNeeded; i++) {
        track.appendChild(originalSet.cloneNode(true));
    }

    let offset = 0;
    const speed = 0.5; // pixels per frame

    function animate() {
        offset -= speed;
        // When the first set has fully scrolled off-screen, reset seamlessly
        if (Math.abs(offset) >= setWidth) {
            offset += setWidth;
        }
        track.style.transform = `translateX(${offset}px)`;
        requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
}


/* ==============================================
   HERO IMAGE SLIDER
   ============================================== */
function initHeroSlider() {
    const track = document.getElementById('hero-track');
    const slides = track ? track.querySelectorAll('.hero__slide') : [];
    const prevBtn = document.getElementById('hero-prev');
    const nextBtn = document.getElementById('hero-next');

    if (!track || slides.length === 0) return;

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;
    let isTransitioning = false;

    function goToSlide(index, direction = 'next') {
        if (isTransitioning) return;
        isTransitioning = true;

        // Remove active class from current slide
        slides[currentIndex].classList.remove('hero__slide--active');

        // Update index
        currentIndex = ((index % totalSlides) + totalSlides) % totalSlides;

        // Move track
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Add active class to new slide after transition
        setTimeout(() => {
            slides[currentIndex].classList.add('hero__slide--active');
            // Re-trigger animations
            restartAnimations(slides[currentIndex]);
            isTransitioning = false;
        }, 800);
    }

    function restartAnimations(slide) {
        const heading = slide.querySelector('.hero__heading');
        const cta = slide.querySelector('.hero__cta');

        if (heading) {
            heading.style.animation = 'none';
            heading.offsetHeight; // Trigger reflow
            heading.style.animation = '';
        }
        if (cta) {
            cta.style.animation = 'none';
            cta.offsetHeight; // Trigger reflow
            cta.style.animation = '';
        }
    }

    function nextSlide() {
        goToSlide(currentIndex + 1, 'next');
    }

    function prevSlide() {
        goToSlide(currentIndex - 1, 'prev');
    }

    // Button click handlers
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            resetAutoSlide();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            resetAutoSlide();
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            nextSlide();
            resetAutoSlide();
        } else if (e.key === 'ArrowLeft') {
            prevSlide();
            resetAutoSlide();
        }
    });

    // Auto-slide
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 6000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Pause on hover
    const hero = document.getElementById('hero');
    if (hero) {
        hero.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
        hero.addEventListener('mouseleave', startAutoSlide);
    }

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    if (track) {
        track.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        track.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
    }

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
            resetAutoSlide();
        }
    }

    // Initialize
    slides[0].classList.add('hero__slide--active');
    startAutoSlide();
}


/* ==============================================
   SCROLL REVEAL ANIMATIONS
   ============================================== */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(
        '.story__feature, .categories__card, .collection__card, ' +
        '.story__label, .story__text, .categories__heading, ' +
        '.collection__heading, .collection__subtitle'
    );

    if (!revealElements.length) return;

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -80px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    revealElements.forEach(el => observer.observe(el));
}


/* ==============================================
   STICKY NAVIGATION (optional enhancement)
   ============================================== */
function initStickyNav() {
    const pillNav = document.getElementById('pill-nav');

    if (!pillNav) return;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 10) {
            pillNav.classList.add('scrolled');
        } else {
            pillNav.classList.remove('scrolled');
        }
    }, { passive: true });
}

/* ==============================================
   SEARCH MODAL
   ============================================== */
function initSearchModal() {
    const searchLinks = document.querySelectorAll('#search-link, .top-bar__link[id="search-link"]');
    const searchModal = document.getElementById('search-modal');
    const searchClose = document.getElementById('search-close');
    const searchOverlay = document.getElementById('search-overlay');

    if (!searchModal) return;

    function openSearch(e) {
        if (e) e.preventDefault();
        searchModal.classList.add('active');
        const input = searchModal.querySelector('input');
        if (input) {
            setTimeout(() => input.focus(), 100);
        }
    }

    function closeSearch() {
        searchModal.classList.remove('active');
    }

    searchLinks.forEach(link => {
        link.addEventListener('click', openSearch);
    });

    if (searchClose) searchClose.addEventListener('click', closeSearch);
    if (searchOverlay) searchOverlay.addEventListener('click', closeSearch);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchModal.classList.contains('active')) {
            closeSearch();
        }
    });
}
