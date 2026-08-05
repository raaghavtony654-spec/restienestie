/**
 * RestNest — Shopify Product Mapper Utility
 * 
 * ONE-TIME SETUP SCRIPT — Run this in your browser console to:
 * 1. Fetch all products from your Shopify store
 * 2. Print a mapping of Product Title → Variant ID
 * 3. Auto-fill the data-variant-id attributes in your HTML
 * 
 * HOW TO USE:
 * 1. Set SHOPIFY_DOMAIN and STOREFRONT_ACCESS_TOKEN below (same as shopify-integration.js)
 * 2. Open your RestNest site in a browser
 * 3. Open DevTools Console (F12 → Console tab)
 * 4. Copy-paste this entire file content into the console and press Enter
 * 5. The script will output a table and auto-fill variant IDs
 */

(async function () {
    // ============================================================
    // CONFIGURATION — Same as shopify-integration.js
    // ============================================================
    const ENDPOINT = '/api/shopify';

    // ============================================================
    // Check configuration
    // ============================================================
    

    console.log('🔄 Fetching products from Shopify...');

    // ============================================================
    // Fetch products
    // ============================================================
    const query = `
        query {
            products(first: 50) {
                edges {
                    node {
                        id
                        title
                        handle
                        variants(first: 10) {
                            edges {
                                node {
                                    id
                                    title
                                    price {
                                        amount
                                        currencyCode
                                    }
                                    availableForSale
                                }
                            }
                        }
                        images(first: 1) {
                            edges {
                                node {
                                    url
                                }
                            }
                        }
                    }
                }
            }
        }
    `;

    try {
        const response = await fetch(ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const json = await response.json();

        if (json.errors) {
            console.error('❌ GraphQL errors:', json.errors);
            return;
        }

        const products = json.data.products.edges.map(e => e.node);

        // ============================================================
        // Display product mapping table
        // ============================================================
        console.log(`\n✅ Found ${products.length} products:\n`);

        const tableData = [];
        products.forEach(product => {
            product.variants.edges.forEach(v => {
                const variant = v.node;
                tableData.push({
                    'Product Title': product.title,
                    'Variant Title': variant.title,
                    'Variant ID': variant.id,
                    'Price': `${variant.price.amount} ${variant.price.currencyCode}`,
                    'Available': variant.availableForSale ? '✅' : '❌',
                });
            });
        });

        console.table(tableData);

        // ============================================================
        // Auto-match product cards by title (fuzzy matching)
        // ============================================================
        console.log('\n🔄 Attempting to auto-match product cards in the page...\n');

        const productCards = document.querySelectorAll('.product-card');
        let matchedCount = 0;
        let unmatchedCards = [];

        productCards.forEach(card => {
            const titleEl = card.querySelector('.product-title');
            if (!titleEl) return;

            const cardTitle = titleEl.textContent.trim().toLowerCase();

            // Find matching product by fuzzy title comparison
            const match = products.find(p => {
                const shopifyTitle = p.title.toLowerCase();
                // Check if the card title contains the shopify title or vice versa
                return cardTitle.includes(shopifyTitle) || shopifyTitle.includes(cardTitle);
            });

            if (match) {
                // Use the first available variant
                const firstVariant = match.variants.edges[0]?.node;
                if (firstVariant) {
                    card.setAttribute('data-variant-id', firstVariant.id);
                    matchedCount++;
                    console.log(`  ✅ Matched: "${titleEl.textContent.trim()}" → ${firstVariant.id}`);
                }
            } else {
                unmatchedCards.push(titleEl.textContent.trim());
            }
        });

        console.log(`\n📊 Results: ${matchedCount} cards matched out of ${productCards.length} total.`);

        if (unmatchedCards.length > 0) {
            console.warn(`\n⚠️ ${unmatchedCards.length} cards could not be auto-matched:`);
            unmatchedCards.forEach(title => console.warn(`  - "${title}"`));
            console.warn('\nYou may need to manually set data-variant-id for these cards.');
        }

        // ============================================================
        // Generate copy-paste ready HTML attributes
        // ============================================================
        console.log('\n📋 Copy-paste ready variant ID mapping for index.html:\n');

        products.forEach(product => {
            const firstVariant = product.variants.edges[0]?.node;
            if (firstVariant) {
                console.log(`data-variant-id="${firstVariant.id}"  ← ${product.title}`);
            }
        });

        console.log('\n✅ Done! If auto-matching worked, your "Add to Cart" buttons are now connected to Shopify.');
        console.log('⚠️ Note: These changes are temporary (in-memory only). You need to update your index.html file with the variant IDs shown above.');

    } catch (error) {
        console.error('❌ Failed to fetch products:', error.message);
        console.log('\nTroubleshooting:');
        console.log('1. Check that SHOPIFY_DOMAIN is your .myshopify.com domain');
        console.log('2. Check that STOREFRONT_ACCESS_TOKEN is valid');
        console.log('3. Make sure the Storefront API app has the correct scopes enabled');
    }
})();
