import os

css = """
/* ===== FOOTER ===== */
.site-footer {
    background: #4B3621;
    color: #fff;
    padding: 3rem 1.5rem;
    font-family: 'Inter', sans-serif;
    text-align: center;
}
.site-footer__inner {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}
.site-footer__links {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    justify-content: center;
}
.site-footer__links a {
    color: #fff;
    text-decoration: none;
    font-size: 1rem;
    font-weight: 500;
    transition: opacity 0.2s;
}
.site-footer__links a:hover {
    opacity: 0.8;
}
.site-footer__social {
    margin-top: 0.5rem;
}
.site-footer__social a {
    color: #fff;
    display: inline-block;
    transition: transform 0.2s;
}
.site-footer__social a:hover {
    transform: scale(1.1);
}
.site-footer__copyright {
    margin-top: 2rem;
    font-size: 0.8rem;
    opacity: 0.6;
}
"""

with open('c:/Users/legion-5pro/Documents/restie/styles.css', 'a', encoding='utf-8') as f:
    f.write("\n" + css + "\n")

footer_template = """
    <!-- ===== FOOTER ===== -->
    <footer class="site-footer">
        <div class="site-footer__inner">
            <div class="site-footer__links">
                <a href="{prefix}pillows/">Pillows collection</a>
                <a href="{prefix}cushions/">Cushion collection</a>
            </div>
            <div class="site-footer__social">
                <a href="https://instagram.com" target="_blank" aria-label="Instagram">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                        <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                    </svg>
                </a>
            </div>
        </div>
        <div class="site-footer__copyright">
            &copy; 2026 RestNest. All rights reserved.
        </div>
    </footer>
"""

base_dir = 'c:/Users/legion-5pro/Documents/restie'
files_to_modify = [
    'index.html',
    'about/index.html',
    'pillows/index.html',
    'cushions/index.html',
    'checkout.html',
    'product/index.html',
    'mobile/index.html'
]

for file_path in files_to_modify:
    full_path = os.path.join(base_dir, file_path)
    if not os.path.exists(full_path):
        continue
    
    depth = file_path.count('/')
    prefix = '../' * depth if depth > 0 else ''
    
    footer_html = footer_template.format(prefix=prefix)
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<footer class="site-footer">' not in content:
        content = content.replace('</body>', footer_html + '\n</body>')
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
