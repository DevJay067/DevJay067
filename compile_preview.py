# -*- coding: utf-8 -*-
"""
README Preview Compiler
Reads README.md, encodes it as base64, and compiles it into the HTML template to bypass CORS.
"""
import base64
import os

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Profile README Preview</title>
    <!-- GitHub Markdown CSS Dark Mode -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
    <style>
        body {
            background-color: #040d1a;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .preview-header {
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .preview-title {
            font-size: 16px;
            font-weight: 600;
            color: #58a6ff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .preview-status {
            font-size: 12px;
            color: #8b949e;
            background-color: #21262d;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid #30363d;
        }
        .markdown-body {
            box-sizing: border-box;
            width: 100%;
            padding: 45px;
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        @media (max-width: 767px) {
            .markdown-body {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="preview-header">
            <div class="preview-title">
                <span>📁 dev-jay / README.md</span>
            </div>
            <div class="preview-status">🟢 Live Local Preview</div>
        </div>
        <article class="markdown-body" id="content">
            <p style="text-align: center; color: #8b949e;">Loading preview...</p>
        </article>
    </div>

    <!-- Marked.js to parse markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        marked.setOptions({
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        });

        function b64DecodeUnicode(str) {
            return decodeURIComponent(atob(str).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
        }

        const b64Data = "BASE64_PLACEHOLDER";

        function loadPreview() {
            try {
                if (b64Data === "BASE64_PLACEHOLDER") {
                    throw new Error("Preview content not compiled yet.");
                }
                const markdownText = b64DecodeUnicode(b64Data);
                document.getElementById('content').innerHTML = marked.parse(markdownText);
            } catch (err) {
                document.getElementById('content').innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #ff7b72;">
                        <h3>Error Loading README.md</h3>
                        <p>${err.message}</p>
                    </div>
                `;
            }
        }

        loadPreview();
    </script>
</body>
</html>
"""

def compile_preview():
    readme_path = "README.md"
    preview_path = "preview.html"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
        
    # base64 encode the markdown content
    encoded = base64.b64encode(readme_content.encode("utf-8")).decode("utf-8")
    
    # inject into template
    output_html = TEMPLATE.replace("BASE64_PLACEHOLDER", encoded)
    
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"Successfully compiled preview to: {os.path.abspath(preview_path)}")

if __name__ == "__main__":
    compile_preview()
