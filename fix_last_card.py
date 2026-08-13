import re

with open('c:/Users/legion-5pro/Documents/restie/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """<div class="products-slider__card">
  <a href="product/?id=white-amp-gold-glace-cotton-pillows-pack-of-2">
  <span class="products-slider__badge">-41%</span>
  <div class="products-slider__img-wrap">
  <img alt="White Gold Glace Cotton Pillows" src="assets/product-img-4.jpg"/>
  </div>
  <h3 class="products-slider__name">Rest Nest White &amp; Gold Glace Cotton Pillows - Pack of 2</h3>
  <div class="products-slider__price">
  <span class="products-slider__sale">Rs. 1,110.00</span>
  <span class="products-slider__original">Rs. 1,897.00</span>
  </div>
  </a>
  </div>"""

new_html = """<div class="products-slider__card">
  <div style="; text-decoration: none; color: inherit; cursor: default;">
  <span class="products-slider__badge">-41%</span>
  <div class="products-slider__img-wrap">
  <img alt="White Gold Glace Cotton Pillows" src="assets/product-img-4.jpg"/>
  </div>
  <h3 class="products-slider__name">Rest Nest White &amp; Gold Glace Cotton Pillows - Pack of 2</h3>
  <div class="products-slider__price">
  <span class="products-slider__sale">Rs. 1,110.00</span>
  <span class="products-slider__original">Rs. 1,897.00</span>
  </div>
  </div>
  <button class="btn--primary" disabled="" style="margin-top: 1rem; width: 100%; padding: 0.75rem; background: #4B3621; color: #FAF9F6; border: none; font-weight: bold; cursor: not-allowed; opacity: 0.5;">Out of Stock</button>
  </div>"""

html = html.replace(old_html, new_html)

# Also check for \r\n
old_html_rn = old_html.replace('\n', '\r\n')
new_html_rn = new_html.replace('\n', '\r\n')
html = html.replace(old_html_rn, new_html_rn)

with open('c:/Users/legion-5pro/Documents/restie/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
