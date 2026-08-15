import os
import glob

html_files = glob.glob('**/*.html', recursive=True)

loader_html = """
    <!-- Simple Page Loader -->
    <style>
        .page-loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #FAF9F6; z-index: 99999;
            display: flex; justify-content: center; align-items: center;
            opacity: 0; visibility: hidden; pointer-events: none;
            transition: opacity 0.4s ease, visibility 0.4s ease;
        }
        .page-loader-overlay.active {
            opacity: 1; visibility: visible; pointer-events: all;
        }
        .loader-spinner {
            width: 40px; height: 40px;
            border: 4px solid rgba(75, 54, 33, 0.1);
            border-left-color: #4B3621;
            border-radius: 50%;
            animation: loader-spin 1s linear infinite;
        }
        @keyframes loader-spin { 100% { transform: rotate(360deg); } }
    </style>
    <div id="page-loader" class="page-loader-overlay">
        <div class="loader-spinner"></div>
    </div>
    <script>
        (function() {
            var loaderTimeout = setTimeout(function() {
                var loader = document.getElementById('page-loader');
                if (loader) loader.classList.add('active');
            }, 500); // Show loader only if page takes > 500ms to load

            window.addEventListener('load', function() {
                clearTimeout(loaderTimeout);
                var loader = document.getElementById('page-loader');
                if (loader) loader.classList.remove('active');
            });
        })();
    </script>
"""

for file_path in html_files:
    if 'admin-app' in file_path or 'server' in file_path:
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'page-loader-overlay' in content:
        continue
        
    # Find body tag. Some might have classes.
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + loader_html)
    elif '<body class="page-account">' in content:
        content = content.replace('<body class="page-account">', '<body class="page-account">\n' + loader_html)
    else:
        # Fallback to replacing <head> or something else if needed, but we assume <body> is there.
        import re
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + loader_html, content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print(f"Processed files.")
