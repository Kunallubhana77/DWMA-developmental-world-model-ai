import os
import subprocess

BASE_DIR = "/Users/kunallubhana/Desktop/dwma"
SUB_DIR = os.path.join(BASE_DIR, "submissions", "cognitive_systems_research")
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def build_cover_letter_pdf():
    cl_txt_path = os.path.join(SUB_DIR, "cover_letter.txt")
    with open(cl_txt_path, "r", encoding="utf-8") as f:
        txt = f.read()
    
    paragraphs = txt.split("\n\n")
    body_html = "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    line-height: 1.55;
    padding: 40px 50px;
    max-width: 800px;
    margin: 0 auto;
    font-size: 10pt;
  }}
  h2 {{
    color: #0284c7;
    font-size: 14pt;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 6px;
    margin-bottom: 16px;
  }}
  p {{
    margin-bottom: 12px;
    text-align: justify;
  }}
</style>
</head>
<body>
<h2>Cover Letter — Cognitive Systems Research</h2>
{body_html}
</body>
</html>
"""
    out_pdf = os.path.join(SUB_DIR, "Cover_Letter.pdf")
    temp_html = out_pdf.replace(".pdf", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)
    
    cmd = [
        EDGE_BIN,
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={out_pdf}",
        temp_html
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Compiled: {out_pdf} ({os.path.getsize(out_pdf)} bytes)")

if __name__ == '__main__':
    build_cover_letter_pdf()
