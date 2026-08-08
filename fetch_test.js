const SHOPIFY_DOMAIN = '6770df-a2.myshopify.com';
const STOREFRONT_ACCESS_TOKEN = '23d3e88ed88fd584ae6c33c2cbe768d0';
const GRAPHQL_ENDPOINT = `https://${SHOPIFY_DOMAIN}/api/2025-04/graphql.json`;

const PRODUCTS_QUERY = `
  query {
    products(first: 50) {
      edges {
        node {
          id
          title
          variants(first: 10) {
            edges {
              node {
                id
                price { amount currencyCode }
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

fetch(GRAPHQL_ENDPOINT, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN
  },
  body: JSON.stringify({ query: PRODUCTS_QUERY }),
})
.then(res => res.json())
.then(data => {
  const products = data.data.products.edges;
  console.log(`Found ${products.length} products`);
  const target = products.find(p => p.node.title.includes('Rest Nest 16x16 White Stripe Soft Cushions'));
  if (target) {
    console.log("Target product found:", JSON.stringify(target, null, 2));
  } else {
    console.log("Target product not found. Here are all titles:");
    products.forEach(p => console.log(p.node.title));
  }
})
.catch(err => console.error(err));
