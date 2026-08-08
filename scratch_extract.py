import re
html = open('restnest_html.txt', encoding='utf-8').read()
res = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>.*?<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*alt=[\'"]collectionTitle[\'"]', html, re.DOTALL)
for a, img in res:
    print(a, img)
