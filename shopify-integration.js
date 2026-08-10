/**
 * RestNest — Shopify Storefront API Integration (GraphQL)
 * 
 * Replaces the deprecated JS Buy SDK with direct Storefront API calls.
 * Uses the modern Cart API (not the legacy Checkout object).
 *
 * SETUP:
 * 1. Set SHOPIFY_DOMAIN to your .myshopify.com domain
 * 2. Set STOREFRONT_ACCESS_TOKEN from Shopify Admin → Settings → Apps → Develop apps
 * 3. Run the shopify-product-mapper.js utility to get variant IDs for your products
 * 4. Add data-variant-id attributes to product cards in index.html
 */

const SHOPIFY_DOMAIN = '6770df-a2.myshopify.com';
const STOREFRONT_ACCESS_TOKEN = '23d3e88ed88fd584ae6c33c2cbe768d0';
const GRAPHQL_ENDPOINT = `https://${SHOPIFY_DOMAIN}/api/2026-07/graphql.json`;

// ============================================================
// GraphQL Queries & Mutations
// ============================================================
const CART_CREATE_MUTATION = `
  mutation cartCreate($input: CartInput!) {
    cartCreate(input: $input) {
      cart {
        id
        checkoutUrl
        totalQuantity
        cost {
          totalAmount {
            amount
            currencyCode
          }
        }
        lines(first: 50) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                  product {
                    title
                  }
                  image {
                    url
                  }
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

const CART_LINES_ADD_MUTATION = `
  mutation cartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {
    cartLinesAdd(cartId: $cartId, lines: $lines) {
      cart {
        id
        checkoutUrl
        totalQuantity
        cost {
          totalAmount {
            amount
            currencyCode
          }
        }
        lines(first: 50) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                  product {
                    title
                  }
                  image {
                    url
                  }
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

const CART_LINES_REMOVE_MUTATION = `
  mutation cartLinesRemove($cartId: ID!, $lineIds: [ID!]!) {
    cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
      cart {
        id
        checkoutUrl
        totalQuantity
        cost {
          totalAmount {
            amount
            currencyCode
          }
        }
        lines(first: 50) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                  product {
                    title
                  }
                  image {
                    url
                  }
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

const CART_LINES_UPDATE_MUTATION = `
  mutation cartLinesUpdate($cartId: ID!, $lines: [CartLineUpdateInput!]!) {
    cartLinesUpdate(cartId: $cartId, lines: $lines) {
      cart {
        id
        checkoutUrl
        totalQuantity
        cost {
          totalAmount {
            amount
            currencyCode
          }
        }
        lines(first: 50) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                  product {
                    title
                  }
                  image {
                    url
                  }
                  price {
                    amount
                    currencyCode
                  }
                }
              }
            }
          }
        }
      }
      userErrors {
        field
        message
      }
    }
  }
`;

const CART_QUERY = `
  query cart($cartId: ID!) {
    cart(id: $cartId) {
      id
      checkoutUrl
      totalQuantity
      cost {
        totalAmount {
          amount
          currencyCode
        }
      }
      lines(first: 50) {
        edges {
          node {
            id
            quantity
            merchandise {
              ... on ProductVariant {
                id
                title
                product {
                  title
                }
                image {
                  url
                }
                price {
                  amount
                  currencyCode
                }
              }
            }
          }
        }
      }
    }
  }
`;

const PRODUCTS_QUERY = `
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

// ============================================================
// Helper: Send GraphQL request to Shopify
// ============================================================
async function shopifyFetch(query, variables = {}) {
  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN
    },
    body: JSON.stringify({ query, variables }),
  });

  if (!response.ok) {
    throw new Error(`Shopify API error: ${response.status} ${response.statusText}`);
  }

  const json = await response.json();

  if (json.errors) {
    console.error('Shopify GraphQL errors:', json.errors);
    throw new Error(json.errors.map(e => e.message).join(', '));
  }

  return json.data;
}

// ============================================================
// ShopifyCart — The public API used by script.js
// ============================================================
const ShopifyCart = {
  _cartId: null,
  _cart: null,
  _initialized: false,
  _initializing: null, // Promise to prevent concurrent init calls

  /**
   * Check if Shopify credentials are configured
   */
  isConfigured() { return true; },

  /**
   * Initialize: Load existing cart from localStorage or create a new one.
   * Returns the cart object, or null if Shopify is not configured.
   */
  async init() {
    if (!this.isConfigured()) {
      console.warn(
        '[ShopifyCart] Not configured. Set SHOPIFY_DOMAIN and STOREFRONT_ACCESS_TOKEN in shopify-integration.js'
      );
      return null;
    }

    // Prevent concurrent initialization
    if (this._initializing) {
      return this._initializing;
    }

    if (this._initialized && this._cart) {
      return this._cart;
    }

    this._initializing = this._doInit();
    const result = await this._initializing;
    this._initializing = null;
    return result;
  },

  async _doInit() {
    const savedCartId = localStorage.getItem('shopify_cart_id');

    if (savedCartId) {
      try {
        const data = await shopifyFetch(CART_QUERY, { cartId: savedCartId });
        if (data.cart) {
          this._cartId = data.cart.id;
          this._cart = data.cart;
          this._initialized = true;
          console.log('[ShopifyCart] Restored existing cart:', this._cartId);
          return this._cart;
        }
      } catch (err) {
        console.warn('[ShopifyCart] Could not restore saved cart, creating new one.', err.message);
        localStorage.removeItem('shopify_cart_id');
      }
    }

    // Create a fresh empty cart
    try {
      const data = await shopifyFetch(CART_CREATE_MUTATION, {
        input: { lines: [] },
      });

      if (data.cartCreate.userErrors.length > 0) {
        console.error('[ShopifyCart] Cart creation errors:', data.cartCreate.userErrors);
        return null;
      }

      this._cart = data.cartCreate.cart;
      this._cartId = this._cart.id;
      localStorage.setItem('shopify_cart_id', this._cartId);
      this._initialized = true;
      console.log('[ShopifyCart] Created new cart:', this._cartId);
      return this._cart;
    } catch (err) {
      console.error('[ShopifyCart] Failed to create cart:', err.message);
      return null;
    }
  },

  /**
   * Add an item to the Shopify cart.
   * @param {string} variantId — e.g. "gid://shopify/ProductVariant/123456"
   * @param {number} quantity
   * @returns {object|null} Updated cart object
   */
  async addItem(variantId, quantity = 1) {
    if (!this.isConfigured()) return null;

    // Validate variant ID format
    if (!variantId || !variantId.startsWith('gid://shopify/ProductVariant/')) {
      console.warn('[ShopifyCart] Invalid variant ID:', variantId);
      return null;
    }

    await this.init();
    if (!this._cartId) return null;

    try {
      const data = await shopifyFetch(CART_LINES_ADD_MUTATION, {
        cartId: this._cartId,
        lines: [{ merchandiseId: variantId, quantity }],
      });

      if (data.cartLinesAdd.userErrors.length > 0) {
        console.error('[ShopifyCart] Add item errors:', data.cartLinesAdd.userErrors);
        return null;
      }

      this._cart = data.cartLinesAdd.cart;
      console.log('[ShopifyCart] Added item. Cart now has', this._cart.totalQuantity, 'items');
      return this._cart;
    } catch (err) {
      console.error('[ShopifyCart] Failed to add item:', err.message);
      return null;
    }
  },

  /**
   * Remove a line item from the Shopify cart.
   * @param {string} lineId — The cart line ID (from cart.lines.edges[].node.id)
   * @returns {object|null} Updated cart object
   */
  async removeItem(lineId) {
    if (!this.isConfigured() || !this._cartId) return null;

    try {
      const data = await shopifyFetch(CART_LINES_REMOVE_MUTATION, {
        cartId: this._cartId,
        lineIds: [lineId],
      });

      if (data.cartLinesRemove.userErrors.length > 0) {
        console.error('[ShopifyCart] Remove item errors:', data.cartLinesRemove.userErrors);
        return null;
      }

      this._cart = data.cartLinesRemove.cart;
      console.log('[ShopifyCart] Removed item. Cart now has', this._cart.totalQuantity, 'items');
      return this._cart;
    } catch (err) {
      console.error('[ShopifyCart] Failed to remove item:', err.message);
      return null;
    }
  },

  /**
   * Update quantity of a line item.
   * @param {string} lineId — The cart line ID
   * @param {number} quantity — New quantity
   * @returns {object|null} Updated cart object
   */
  async updateItem(lineId, quantity) {
    if (!this.isConfigured() || !this._cartId) return null;

    try {
      const data = await shopifyFetch(CART_LINES_UPDATE_MUTATION, {
        cartId: this._cartId,
        lines: [{ id: lineId, quantity }],
      });

      if (data.cartLinesUpdate.userErrors.length > 0) {
        console.error('[ShopifyCart] Update item errors:', data.cartLinesUpdate.userErrors);
        return null;
      }

      this._cart = data.cartLinesUpdate.cart;
      return this._cart;
    } catch (err) {
      console.error('[ShopifyCart] Failed to update item:', err.message);
      return null;
    }
  },

  /**
   * Fetch current cart state from Shopify.
   * @returns {object|null} Cart object
   */
  async getCart() {
    if (!this.isConfigured() || !this._cartId) return null;

    try {
      const data = await shopifyFetch(CART_QUERY, { cartId: this._cartId });
      this._cart = data.cart;
      return this._cart;
    } catch (err) {
      console.error('[ShopifyCart] Failed to fetch cart:', err.message);
      return null;
    }
  },

  /**
   * Helper to find a cart line ID by its merchandise variant ID.
   * @param {string} variantId 
   * @returns {string|null} lineId
   */
  findLineIdByVariantId(variantId) {
    if (!this._cart || !this._cart.lines) return null;
    
    for (const edge of this._cart.lines.edges) {
      if (edge.node.merchandise && edge.node.merchandise.id === variantId) {
        return edge.node.id;
      }
    }
    return null;
  },

  /**
   * Get the Shopify hosted checkout URL for the current cart.
   * @returns {string|null} Checkout URL
   */
  getCheckoutUrl() {
    if (this._cart && this._cart.checkoutUrl) {
      return this._cart.checkoutUrl;
    }
    return null;
  },

  /**
   * Redirect the user to Shopify's hosted checkout page.
   */
  async goToCheckout() {
    try {
      // Make sure the cart exists
      await this.init();

      if (!this._cartId) {
        alert('Your cart is empty. Please add a product first.');
        return;
      }

      // Get the latest cart directly from Shopify
      const data = await shopifyFetch(CART_QUERY, {
        cartId: this._cartId
      });

      if (!data || !data.cart) {
        // Old/expired cart — create a fresh one
        localStorage.removeItem('shopify_cart_id');
        this._cartId = null;
        this._cart = null;
        this._initialized = false;

        alert('Your cart expired. Please add the product to your cart again.');
        return;
      }

      this._cart = data.cart;

      // Shopify's hosted checkout URL
      const checkoutUrl = this._cart.checkoutUrl;

      if (!checkoutUrl) {
        console.error('Shopify did not return a checkout URL:', this._cart);
        alert('Unable to open checkout. Please try again.');
        return;
      }

      console.log('[ShopifyCart] Opening checkout:', checkoutUrl);

      window.location.assign(checkoutUrl);

    } catch (error) {
      console.error('[ShopifyCart] Checkout failed:', error);
      alert('Checkout could not be opened. Please try again.');
    }
  },

  /**
   * Fetch all products from the Shopify store.
   * Useful for mapping product titles to variant IDs.
   * @returns {Array} Array of product objects
   */
  async fetchProducts() {
    if (!this.isConfigured()) {
      console.warn('[ShopifyCart] Not configured — cannot fetch products.');
      return [];
    }

    try {
      const data = await shopifyFetch(PRODUCTS_QUERY);
      const products = data.products.edges.map(edge => {
        const node = edge.node;
        return {
          id: node.id,
          title: node.title,
          handle: node.handle,
          image: node.images.edges[0]?.node.url || null,
          variants: node.variants.edges.map(v => ({
            id: v.node.id,
            title: v.node.title,
            price: v.node.price.amount,
            currency: v.node.price.currencyCode,
            available: v.node.availableForSale,
          })),
        };
      });
      return products;
    } catch (err) {
      console.error('[ShopifyCart] Failed to fetch products:', err.message);
      return [];
    }
  },

  /**
   * Find the Shopify line ID for a given variant ID in the current cart.
   * Used to map local cart items to Shopify cart lines for removal/updates.
   * @param {string} variantId
   * @returns {string|null} Line ID
   */
  findLineIdByVariantId(variantId) {
    if (!this._cart || !this._cart.lines) return null;

    const edge = this._cart.lines.edges.find(
      e => e.node.merchandise.id === variantId
    );
    return edge ? edge.node.id : null;
  },

  /**
   * Clear the current cart (by removing the cart ID from localStorage).
   * A new cart will be created on next init().
   */
  clearCart() {
    this._cartId = null;
    this._cart = null;
    this._initialized = false;
    localStorage.removeItem('shopify_cart_id');
    console.log('[ShopifyCart] Cart cleared.');
  },
};

// ============================================================
// Auto-initialize on page load
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  ShopifyCart.init();
});

document.addEventListener('click', function (event) {
  const button = event.target.closest('button, a');

  if (!button) return;

  const text = button.textContent.trim().toLowerCase();

  if (text.includes('checkout')) {
    event.preventDefault();
    event.stopPropagation();

    ShopifyCart.goToCheckout();
  }
});
