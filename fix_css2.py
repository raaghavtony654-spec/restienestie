import sys

file_path = r"c:\Users\legion-5pro\Documents\restie\styles.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the end of the .qty-btn section and reconstruct the rest of the file cleanly
target_str = ".qty-btn {\n    width: 28px;\n    height: 28px;"
start_idx = content.find(target_str)

if start_idx == -1:
    print("Could not find .qty-btn block")
    sys.exit(1)

clean_end_content = """
.qty-btn {
    width: 28px;
    height: 28px;
    border: 1px solid rgba(75, 54, 33, 0.3);
    background: transparent;
    color: #4B3621;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    line-height: 1;
}

.qty-btn:hover {
    background: #4B3621;
    color: #FAF9F6;
    border-color: #4B3621;
}

.qty-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #4B3621;
    min-width: 20px;
    text-align: center;
}

/* ==============================================
   CART STYLES
   ============================================== */
.cart-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 9999999;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease;
}

.cart-overlay.active {
    opacity: 1;
    visibility: visible;
}

.cart-dropdown {
    position: fixed;
    top: 0;
    right: -450px;
    width: 100%;
    max-width: 400px;
    height: 100vh;
    background: #FAF9F6;
    border-left: 1px solid rgba(75, 54, 33, 0.1);
    z-index: 9999999;
    display: flex;
    flex-direction: column;
    transition: right 0.4s cubic-bezier(0.77, 0, 0.175, 1);
    box-shadow: -5px 0 30px rgba(0, 0, 0, 0.1);
    font-family: var(--font-sans);
}

.cart-dropdown.active {
    right: 0;
}

.cart-header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(75, 54, 33, 0.1);
}

.cart-header h2 {
    font-size: 1.5rem;
    color: #4B3621;
    font-family: var(--font-serif);
    margin: 0;
}

.cart-close-btn {
    background: none;
    border: none;
    color: #4B3621;
    font-size: 2rem;
    cursor: pointer;
    line-height: 1;
}

.cart-close-btn:hover {
    opacity: 0.7;
}

.cart-items {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.cart-empty {
    text-align: center;
    color: #4B3621;
    opacity: 0.7;
    margin-top: 50px;
}

.cart-item {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(75, 54, 33, 0.1);
}

.cart-item img {
    width: 70px;
    height: 70px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid rgba(75, 54, 33, 0.1);
}

.cart-item-details {
    flex: 1;
}

.cart-item-details h4 {
    font-size: 0.95rem;
    margin-bottom: 5px;
    color: #4B3621;
}

.cart-item-price {
    color: #4B3621;
    font-weight: 500;
    margin-bottom: 3px;
}

.cart-item-remove {
    background: none;
    border: none;
    color: #ff4d4d;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 5px;
    transition: transform 0.2s;
}

.cart-item-remove:hover {
    transform: scale(1.2);
}

.cart-footer {
    padding: 20px;
    border-top: 1px solid rgba(75, 54, 33, 0.1);
    background: rgba(75, 54, 33, 0.02);
}

.cart-total {
    display: flex;
    justify-content: space-between;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 15px;
    color: #4B3621;
}

.checkout-btn {
    width: 100%;
    padding: 15px;
    background: #4B3621;
    color: #FAF9F6;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.3s;
}

.checkout-btn:hover {
    opacity: 0.9;
}

.cart-item-qty-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 6px;
}

/* ==============================================
   SHOWCASE PLACEHOLDERS
   ============================================== */
.showcase {
    background-color: var(--color-bg);
}
.showcase__placeholders {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    padding: 4rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}
.showcase__placeholder {
    height: 450px;
    background-color: #e8e6e1;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    overflow: hidden;
}
.showcase__placeholder img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

@media (max-width: 900px) {
    .showcase__placeholders {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 500px) {
    .showcase__placeholders {
        grid-template-columns: 1fr;
    }
}
"""

new_content = content[:start_idx] + clean_end_content.strip() + "\n"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("styles.css fixed successfully")
