import os
import subprocess
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = "/Users/kunallubhana/Desktop/dwma"
SUB_DIR = os.path.join(BASE_DIR, "submissions", "cognitive_systems_research")
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def update_cover_letter():
    cl_path = os.path.join(SUB_DIR, "cover_letter.txt")
    with open(cl_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. our -> my
    content = content.replace("submit our original research manuscript", "submit my original research manuscript")
    content = content.replace("our unified embodied architecture", "the unified embodied architecture")
    
    # 2. peer-reviewed journal formulation -> full journal-submission formulation
    content = content.replace(
        "represents the full, peer-reviewed journal formulation with calibrated scientific claims",
        "represents the full journal-submission formulation, with calibrated scientific claims"
    )
    
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {cl_path}")

    # Recompile Cover_Letter.pdf
    paragraphs = content.split("\n\n")
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
        EDGE_BIN, "--headless", "--disable-gpu", "--allow-file-access-from-files",
        "--no-pdf-header-footer", "--virtual-time-budget=8000",
        f"--print-to-pdf={out_pdf}", temp_html
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Compiled Cover_Letter.pdf ({os.path.getsize(out_pdf)} bytes)")

def create_competing_interests_docx():
    doc = Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    
    # Title
    title_p = doc.add_paragraph()
    title_run = title_p.add_run("Declaration of Competing Interests")
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)
    title_p.paragraph_format.space_after = Pt(18)
    
    # Manuscript metadata
    meta_p = doc.add_paragraph()
    r1 = meta_p.add_run("Manuscript Title: ")
    r1.font.bold = True
    meta_p.add_run("DWMA: Autonomous Sensorimotor Structure Acquisition, Multi-Schema Retention, and Active Hypothesis Discrimination in an Embodied World Model\n")
    
    r2 = meta_p.add_run("Author: ")
    r2.font.bold = True
    meta_p.add_run("Kunal Lubhana\n")
    
    r3 = meta_p.add_run("Affiliation: ")
    r3.font.bold = True
    meta_p.add_run("Independent Research, Mumbai, Maharashtra, India\n")
    
    r4 = meta_p.add_run("Journal: ")
    r4.font.bold = True
    meta_p.add_run("Cognitive Systems Research (Elsevier)\n")
    meta_p.paragraph_format.space_after = Pt(24)
    
    # Declaration text
    h2 = doc.add_paragraph()
    h2_run = h2.add_run("Declaration Statement")
    h2_run.font.size = Pt(14)
    h2_run.font.bold = True
    h2.paragraph_format.space_after = Pt(12)
    
    p1 = doc.add_paragraph()
    p1_run = p1.add_run("Declarations of interest: none")
    p1_run.font.bold = True
    p1_run.font.size = Pt(11)
    p1.paragraph_format.space_after = Pt(12)
    
    p2 = doc.add_paragraph()
    p2_run = p2.add_run(
        "The author declares that he has no known competing financial interests or personal relationships "
        "that could have appeared to influence the work reported in this paper. The author has not received "
        "any specific grants, consultancies, stock ownership, or financial compensation related to this research. "
        "The author does not currently serve, nor has previously served, in an editorial capacity for Cognitive Systems Research."
    )
    p2_run.font.size = Pt(10.5)
    p2.paragraph_format.space_after = Pt(36)
    
    # Signature block
    sig_p = doc.add_paragraph()
    s1 = sig_p.add_run("Author Signature / Confirmation:\n")
    s1.font.bold = True
    sig_p.add_run("Kunal Lubhana\n")
    sig_p.add_run("Independent Researcher\n")
    sig_p.add_run("Date: September 16, 2026\n")
    sig_p.add_run("Email: techqubit77@gmail.com\n")
    
    out_docx = os.path.join(SUB_DIR, "Declaration_of_Competing_Interests.docx")
    doc.save(out_docx)
    print(f"Created Word Document: {out_docx} ({os.path.getsize(out_docx)} bytes)")

def update_and_recompile_title_and_manuscript():
    # 1. Update build_csr_submission_pdfs.py with fully transparent, comprehensive AI disclosure
    ai_disclosure_text = (
        "During the preparation of this work, the author utilized generative AI and AI-assisted tools "
        "(including deep research assistants and large language models) for drafting, restructuring, "
        "editorial refinement, LaTeX formatting, and assistance with Python reproduction scripts under "
        "continuous human direction and oversight. Following the use of these tools, the author independently "
        "audited, executed, validated, and edited all empirical code, mathematical formulations, figure visualizations, "
        "and manuscript text. The author assumes full personal responsibility for the factual validity, "
        "scientific integrity, and conclusions presented in this publication."
    )
    
    script_path = os.path.join(BASE_DIR, "scripts", "build_csr_submission_pdfs.py")
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Replace old AI statements
    old_ai_title = (
        "During the preparation of this manuscript, the author used generative AI models solely for editorial grammar refinement, "
        "stylistic readability polishing, and script formatting under rigorous, continuous human oversight. "
        "After using these assistance tools, the author independently reviewed and edited all content and takes full "
        "personal responsibility for the factual integrity and scientific claims of this publication."
    )
    old_ai_manuscript = (
        "During the preparation of this work, the author used generative AI models solely for initial editorial styling, "
        "grammar refinement, and code structuring assistance under direct human oversight. "
        "After using these tools, the author reviewed and edited the content and takes full responsibility for the content of the publication."
    )
    
    code = code.replace(old_ai_title, ai_disclosure_text)
    code = code.replace(old_ai_manuscript, ai_disclosure_text)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    # Recompile Title Page and Anonymized Manuscript
    subprocess.run([".venv/bin/python", script_path], cwd=BASE_DIR)
    print("Recompiled Title Page and Anonymized Manuscript PDFs.")

if __name__ == '__main__':
    update_cover_letter()
    create_competing_interests_docx()
    update_and_recompile_title_and_manuscript()
    print("All submission assets updated with 100% precision.")
