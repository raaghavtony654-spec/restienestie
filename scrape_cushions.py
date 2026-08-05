import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://restnest.in/collections/cushions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    products = []
    # Find product cards
    for card in soup.select('.grid__item'):
        title_elem = card.select_one('.card__heading')
        if not title_elem:
            continue
        title = title_elem.text.strip()
        
        img_elem = card.select_one('img')
        imgUrl = img_elem['src'] if img_elem else ''
        if imgUrl and imgUrl.startswith('//'):
            imgUrl = 'https:' + imgUrl
            
        sale_elem = card.select_one('.price-item--sale')
        regular_elem = card.select_one('.price-item--regular')
        
        salePrice = sale_elem.text.strip() if sale_elem else ''
        originalPrice = regular_elem.text.strip() if regular_elem else ''
        
        # In this theme the original price when on sale is sometimes under a different class like s > span
        if not originalPrice:
            s_elem = card.select_one('s.price-item--regular')
            if s_elem:
                originalPrice = s_elem.text.strip()
                
        discount_elem = card.select_one('.badge--bottom-left')
        discount = discount_elem.text.strip() if discount_elem else '-50%' # default if not found but usually exists
        
        products.append({
            'title': title,
            'imgUrl': imgUrl,
            'salePrice': salePrice,
            'originalPrice': originalPrice,
            'discount': discount
        })
        
        if len(products) == 5:
            break

    print(json.dumps(products, indent=2))
except Exception as e:
    print(e)
