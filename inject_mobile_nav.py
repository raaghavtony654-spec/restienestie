import os, re
files = ['pillows.html', 'about/index.html', 'cushions/index.html', 'pillows/index.html', 'product/index.html']
for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Add hamburger button
    if 'id="mobile-menu-toggle"' not in content:
        content = re.sub(
            r'(<div class="pill-nav__inner">)',
            r'\1\n<!-- Mobile Hamburger -->\n<button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Toggle menu" aria-expanded="false">\n<span class="mobile-menu-toggle__bar"></span>\n<span class="mobile-menu-toggle__bar"></span>\n<span class="mobile-menu-toggle__bar"></span>\n</button>',
            content,
            count=1
        )
    
    # 2. Extract paths from existing nav to generate curtain links correctly
    home_match = re.search(r'<a class="main-nav__link" href="([^"]+)" id="nav-home"', content)
    pillow_match = re.search(r'<a class="main-nav__link" href="([^"]+)" id="nav-pillow"', content)
    cushion_match = re.search(r'<a class="main-nav__link" href="([^"]+)" id="nav-cushion"', content)
    about_match = re.search(r'<a class="main-nav__link" href="([^"]+)" id="nav-about-us"', content)
    
    home_path = home_match.group(1) if home_match else '#'
    pillow_path = pillow_match.group(1) if pillow_match else '#'
    cushion_path = cushion_match.group(1) if cushion_match else '#'
    about_path = about_match.group(1) if about_match else '#'
    
    # 3. Add curtain
    if 'id="mobile-nav-curtain"' not in content:
        curtain_html = f'''</nav>
<!-- ===== MOBILE NAV CURTAIN ===== -->
<div class="mobile-nav-curtain" id="mobile-nav-curtain">
<div class="mobile-nav-curtain__inner">
<a class="mobile-nav-curtain__link" href="{home_path}">Home</a>
<a class="mobile-nav-curtain__link" href="{pillow_path}">Pillow</a>
<a class="mobile-nav-curtain__link" href="{cushion_path}">Cushion</a>
<a class="mobile-nav-curtain__link" href="{about_path}">About Us</a>
</div>
</div>'''
        content = re.sub(
            r'</nav>',
            curtain_html,
            content,
            count=1
        )
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Done!")
