import re
import glob

html_files = glob.glob('**/*.html', recursive=True)

new_loader = """
    <!-- Simple Page Loader -->
    <style>
        .page-loader-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #FAF9F6; z-index: 99999;
            display: flex; justify-content: center; align-items: center;
            opacity: 0; visibility: hidden; pointer-events: none;
            transition: opacity 0.4s ease, visibility 0.4s ease;
            overflow: hidden;
        }
        .page-loader-overlay.active {
            opacity: 1; visibility: visible; pointer-events: all;
        }
        
        .loader-scene {
            position: relative;
            width: 200px;
            height: 200px;
        }

        /* 3D Hole setup */
        .loader-hole-back {
            position: absolute;
            width: 70px;
            height: 18px;
            background: #2A1D11;
            border-radius: 50%;
            top: 155px;
            left: 120px;
            z-index: 5;
            clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%);
        }
        .loader-hole-front {
            position: absolute;
            width: 70px;
            height: 18px;
            background: #2A1D11;
            border-radius: 50%;
            top: 155px;
            left: 120px;
            z-index: 15;
            clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%);
        }
        .loader-floor-mask {
            position: absolute;
            width: 100%;
            height: 400px;
            background: #FAF9F6;
            top: 164px; /* exact vertical center of the hole */
            left: 0;
            z-index: 14;
        }

        /* Bed */
        .loader-bed {
            position: absolute;
            width: 100px;
            height: 22px;
            background: #4B3621;
            border-radius: 4px;
            top: 120px;
            left: 20px;
            z-index: 8;
            box-shadow: 0 4px 10px rgba(75, 54, 33, 0.2);
        }
        /* Bed Legs */
        .loader-bed::before, .loader-bed::after {
            content: '';
            position: absolute;
            width: 8px;
            height: 16px;
            background: #3a2818;
            top: 22px;
            border-radius: 2px;
        }
        .loader-bed::before { left: 10px; }
        .loader-bed::after { right: 10px; }
        
        /* Headboard */
        .loader-bed-headboard {
            position: absolute;
            width: 12px;
            height: 40px;
            background: #4B3621;
            top: 102px;
            left: 14px;
            z-index: 7;
            border-radius: 4px 4px 0 0;
        }

        /* Mattress */
        .loader-mattress {
            position: absolute;
            width: 90px;
            height: 18px;
            background: #E8E2DA;
            border: 2px solid #c4a173;
            border-radius: 6px;
            top: 100px;
            left: 25px;
            z-index: 10;
            box-sizing: border-box;
            box-shadow: inset 0 -3px 0 rgba(139, 115, 85, 0.2);
        }

        .mattress-1 {
            animation: mattress-cycle 2.4s infinite cubic-bezier(0.4, 0, 0.2, 1);
        }
        .mattress-2 {
            animation: mattress-cycle 2.4s infinite cubic-bezier(0.4, 0, 0.2, 1) -1.2s;
        }

        @keyframes mattress-cycle {
            0%, 10% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 1;
            }
            20% {
                transform: translate(30px, -40px) rotate(50deg);
                opacity: 1;
            }
            30% {
                /* Hover perfectly vertical over the hole */
                transform: translate(85px, -10px) rotate(90deg);
                opacity: 1;
            }
            40% {
                /* Drop straight down into the hole */
                transform: translate(85px, 150px) rotate(90deg);
                opacity: 1;
            }
            41%, 50% {
                transform: translate(0, -200px) rotate(0deg);
                opacity: 0;
            }
            51%, 65% {
                transform: translate(0, -200px) rotate(0deg);
                opacity: 1;
            }
            85% {
                transform: translate(0, 0) rotate(0deg);
            }
            90% {
                transform: translate(0, 4px) scaleY(0.8) scaleX(1.05);
            }
            95%, 100% {
                transform: translate(0, 0) scaleY(1) scaleX(1);
            }
        }
    </style>
    <div id="page-loader" class="page-loader-overlay">
        <div class="loader-scene">
            <div class="loader-hole-back"></div>
            <div class="loader-floor-mask"></div>
            <div class="loader-hole-front"></div>
            <div class="loader-bed-headboard"></div>
            <div class="loader-bed"></div>
            <div class="loader-mattress mattress-1"></div>
            <div class="loader-mattress mattress-2"></div>
        </div>
    </div>
    <script>
        (function() {
            var loaderTimeout = setTimeout(function() {
                var loader = document.getElementById('page-loader');
                if (loader) loader.classList.add('active');
            }, 500); // 500ms threshold for fast connections

            window.addEventListener('load', function() {
                clearTimeout(loaderTimeout);
                var loader = document.getElementById('page-loader');
                if (loader) loader.classList.remove('active');
            });
        })();
    </script>"""

pattern = re.compile(r'<!-- Simple Page Loader -->.*?</script>', re.DOTALL)

for file_path in html_files:
    if 'admin-app' in file_path or 'server' in file_path:
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- Simple Page Loader -->' in content:
        new_content = pattern.sub(new_loader, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

print("Done updating loaders.")
