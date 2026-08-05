with open('cushions/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('"styles.css"', '"../styles.css"')
html = html.replace('"assets/', '"../assets/')
html = html.replace('"index.html"', '"../index.html"')
html = html.replace('"script.js"', '"../script.js"')

with open('cushions/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
