import re
import glob

# 1. Update index.html
with open('c:/Users/legion-5pro/Documents/restie/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

buttons_html = """<div class="products-slider" id="products-slider">
    <button class="slider-arrow slider-arrow--prev" id="slider-prev" aria-label="Previous">&larr;</button>
    <button class="slider-arrow slider-arrow--next" id="slider-next" aria-label="Next">&rarr;</button>
    <div class="products-slider__track" id="products-track">"""

html = html.replace('<div class="products-slider" id="products-slider">\n<div class="products-slider__track" id="products-track">', buttons_html)
html = html.replace('<div class="products-slider" id="products-slider">\r\n<div class="products-slider__track" id="products-track">', buttons_html)

with open('c:/Users/legion-5pro/Documents/restie/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update styles.css
css = """
/* ===== SLIDER ARROWS ===== */
.slider-arrow {
    position: absolute;
    top: 40%;
    transform: translateY(-50%);
    z-index: 10;
    background: rgba(255, 255, 255, 0.95);
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: bold;
    color: #4B3621;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: all 0.2s ease;
}
.slider-arrow:hover {
    background: #4B3621;
    color: #fff;
    transform: translateY(-50%) scale(1.1);
}
.slider-arrow--prev {
    left: -22px;
}
.slider-arrow--next {
    right: -22px;
}
@media (max-width: 1024px) {
    .slider-arrow--prev { left: 10px; }
    .slider-arrow--next { right: 10px; }
}
@media (max-width: 900px) {
    .slider-arrow {
        display: none;
    }
}
"""

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'a', encoding='utf-8') as f:
    f.write("\n" + css + "\n")

# 3. Update script.js
with open('c:/Users/legion-5pro/Documents/restie/script.js', 'r', encoding='utf-8') as f:
    script = f.read()

new_js = """function initProductsSlider() {
    const track = document.getElementById('products-track');
    if (!track) return;

    const cards = track.querySelectorAll('.products-slider__card');
    if (!cards.length) return;

    let currentIndex = 0;
    const totalCards = cards.length;
    let visibleCards = 4; // show 4 at a time

    function getCardWidth() {
        const card = cards[0];
        const style = getComputedStyle(track);
        const gap = parseFloat(style.gap) || 0;
        return card.offsetWidth + gap;
    }

    function updateTransform(instant = false) {
        if (window.innerWidth <= 900) visibleCards = 2;
        
        if (instant) {
            track.style.transition = 'none';
        } else {
            track.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        }
        
        const offset = currentIndex * getCardWidth();
        track.style.transform = `translateX(-${offset}px)`;
        
        if (instant) {
            track.offsetHeight;
        }
    }

    function slide() {
        currentIndex++;
        if (currentIndex > totalCards - visibleCards) {
            currentIndex = 0;
            updateTransform(true);
            return;
        }
        updateTransform();
    }

    let slideInterval = setInterval(slide, 2800);
    
    const prevBtn = document.getElementById('slider-prev');
    const nextBtn = document.getElementById('slider-next');
    let pauseTimeout;

    function pauseAutoScroll() {
        clearInterval(slideInterval);
        clearTimeout(pauseTimeout);
        pauseTimeout = setTimeout(() => {
            slideInterval = setInterval(slide, 2800);
        }, 3000);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            pauseAutoScroll();
            currentIndex--;
            if (currentIndex < 0) {
                currentIndex = Math.max(0, totalCards - visibleCards);
            }
            updateTransform(false);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            pauseAutoScroll();
            currentIndex++;
            if (currentIndex > totalCards - visibleCards) {
                currentIndex = 0;
            }
            updateTransform(false);
        });
    }
}"""

script = re.sub(r'function initProductsSlider\(\) \{.*?\n\}\n', new_js + '\n', script, flags=re.DOTALL)

with open('c:/Users/legion-5pro/Documents/restie/script.js', 'w', encoding='utf-8') as f:
    f.write(script)

# 4. Bump versions
html_files = glob.glob('c:/Users/legion-5pro/Documents/restie/**/*.html', recursive=True)
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=13', content)
    new_content = re.sub(r'script\.js\?v=\d+', 'script.js?v=5', new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
