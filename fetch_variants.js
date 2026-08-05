/**
 * Utility: Fetch all Shopify product variant IDs
 * Run with: node fetch_variants.js
 * 
 * This queries the Shopify Storefront API to get all products and their variant IDs,
 * then outputs a JSON mapping of product title -> variant ID.
 */

const SHOPIFY_DOMAIN = '6770df-a2.myshopify.com';
const STOREFRONT_ACCESS_TOKEN = '23d3e88ed88fd584ae6c33c2cbe768d0';
const GRAPHQL_ENDPOINT = `https://${SHOPIFY_DOMAIN}/api/2025-04/graphql.json`;

async function fetchProducts() {
    const query = `
    {
        products(first: 50) {
            edges {
                node {
                    id
                    title
                    handle
                    images(first: 1) {
                        edges {
                            node {
                                url
                            }
                        }
                    }
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
                }
            }
        }
    }`;

    const response = await fetch(GRAPHQL_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN
        },
        body: JSON.stringify({ query }),
    });

    const json = await response.json();
    
    if (json.errors) {
        console.error('GraphQL errors:', json.errors);
        return;
    }

    const products = json.data.products.edges.map(edge => {
        const node = edge.node;
        return {
            title: node.title,
            handle: node.handle,
            shopifyProductId: node.id,
            image: node.images.edges[0]?.node.url || null,
            variants: node.variants.edges.map(v => ({
                variantId: v.node.id,
                variantTitle: v.node.title,
                price: v.node.price.amount,
                currency: v.node.price.currencyCode,
                available: v.node.availableForSale,
            })),
        };
    });

    // Print full product list
    console.log('\n=== ALL SHOPIFY PRODUCTS & VARIANTS ===\n');
    products.forEach(p => {
        console.log(`📦 ${p.title}`);
        console.log(`   Handle: ${p.handle}`);
        console.log(`   Image: ${p.image}`);
        p.variants.forEach(v => {
            console.log(`   → Variant: ${v.variantId} | ${v.variantTitle} | ₹${v.price} | Available: ${v.available}`);
        });
        console.log('');
    });

    // Print as JSON mapping (image URL -> variant ID) for easy use
    console.log('\n=== JSON MAPPING (image -> variantId) ===\n');
    const mapping = {};
    products.forEach(p => {
        // Use the image URL as key for matching
        if (p.image && p.variants.length > 0) {
            mapping[p.image] = {
                title: p.title,
                variantId: p.variants[0].variantId,
                price: p.variants[0].price
            };
        }
        // Also map by title
        if (p.variants.length > 0) {
            mapping[p.title] = p.variants[0].variantId;
        }
    });
    console.log(JSON.stringify(mapping, null, 2));
}

fetchProducts().catch(err => console.error('Error:', err));
