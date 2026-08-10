import os, re

# 1. Update HTML files to remove inline style for .products-grid
for f in ['pillows/index.html', 'cushions/index.html', 'pillows.html']:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove inline style related to products-grid
    content = re.sub(
        r'<div class=\"products-grid\"[^>]*style=\"[^\"]*\"[^>]*>',
        '<div class=\"products-grid\" id=\"products-grid\">',
        content
    )
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

# 2. Append the new CSS rules to styles.css
with open('styles.css', 'a', encoding='utf-8') as file:
    file.write('''

/* ==============================================
   PRODUCTS GRID (PILLOWS & CUSHIONS PAGES)
   ============================================== */
.products-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem;
    max-width: 1200px;
    margin: 0 auto;
}

@media (max-width: 900px) {
    .products-grid {
        gap: 2rem;
    }
}

@media (max-width: 768px) {
    .products-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
}

@media (max-width: 500px) {
    .products-grid {
        /* Keep 2 columns even on very small screens? I'll do 2 columns to match the request */
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }
}
''')
print('Updated styles and HTML')
