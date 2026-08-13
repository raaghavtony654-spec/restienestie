import os
import glob

html_files = glob.glob('**/*.html', recursive=True)

fb_html = """
                <a href="https://m.facebook.com/profile.php?id=61577983328975&name=xhp_nt__fb__action__open_user" target="_blank" aria-label="Facebook" style="margin-left: 1.5rem;">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
                    </svg>
                </a>"""

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "aria-label=\"Facebook\"" not in content:
        # We need to insert fb_html after the closing </a> of the instagram link.
        # Find the instagram block end
        search_str = """                    </svg>
                </a>"""
        
        # Only replace the first occurrence that comes after the instagram link.
        # It's safer to replace the exact instagram block end.
        
        target_str = """                        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                    </svg>
                </a>"""
        
        if target_str in content:
            new_content = content.replace(target_str, target_str + fb_html)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added Facebook link to {file_path}")
