import os

base_dir = 'c:/Users/legion-5pro/Documents/restie'

html_files = [
    'index.html',
    'pillows/index.html',
    'cushions/index.html',
    'about/index.html',
    'checkout.html',
    'bulk/index.html',
    'mobile/index.html',
    'terms/index.html'
]

clarity_code = """
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "y1ui8xvx9v");
    </script>
"""

for file in html_files:
    path = os.path.join(base_dir, file)
    if not os.path.exists(path):
        print(f"Skipping {file} - not found.")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "clarity.ms/tag" in content:
        print(f"Skipping {file} - already has Clarity code.")
        continue
        
    # Insert right before </head>
    new_content = content.replace("</head>", clarity_code + "</head>")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added Clarity to {file}")
