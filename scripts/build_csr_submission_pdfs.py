import os
import subprocess

BASE_DIR = "/Users/kunallubhana/Desktop/dwma"
SUB_DIR = os.path.join(BASE_DIR, "submissions", "cognitive_systems_research")
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def compile_html_to_pdf(html_content, output_pdf_path):
    temp_html = output_pdf_path.replace(".pdf", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_BIN,
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={output_pdf_path}",
        temp_html
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Compiled: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")

def build_title_page():
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    line-height: 1.6;
    padding: 40px 50px;
    max-width: 800px;
    margin: 0 auto;
  }
  h1 {
    font-size: 18pt;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 12px;
    margin-bottom: 24px;
    line-height: 1.35;
  }
  .section-title {
    font-size: 12pt;
    font-weight: bold;
    color: #0369a1;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 24px;
    margin-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
  }
  .author-block {
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 24px;
  }
  .author-name {
    font-size: 14pt;
    font-weight: bold;
    color: #0f172a;
  }
  .author-affil {
    font-size: 11pt;
    color: #475569;
    margin-top: 4px;
  }
  .author-contact {
    font-size: 10pt;
    color: #0284c7;
    margin-top: 6px;
  }
  p {
    font-size: 10pt;
    color: #334155;
    margin-bottom: 12px;
    text-align: justify;
  }
</style>
</head>
<body>

<h1>DWMA: Autonomous Sensorimotor Structure Acquisition, Multi-Schema Retention, and Active Hypothesis Discrimination in an Embodied World Model</h1>

<div class="section-title">Author & Affiliation Information</div>
<div class="author-block">
  <div class="author-name">Kunal Lubhana</div>
  <div class="author-affil">Independent Research, Mumbai, Maharashtra, India</div>
  <div class="author-contact"><strong>Corresponding Author Email:</strong> techqubit77@gmail.com</div>
</div>

<div class="section-title">CRediT Authorship Contribution Statement</div>
<p><strong>Kunal Lubhana:</strong> Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing - Original Draft, Writing - Review &amp; Editing, Visualization, Project administration.</p>

<div class="section-title">Declaration of Competing Interest</div>
<p>The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.</p>

<div class="section-title">Funding Statement</div>
<p>This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. It was conducted as an independent research investigation.</p>

<div class="section-title">Declaration of Generative AI in Scientific Writing</div>
<p>During the preparation of this work, the author utilized generative AI and AI-assisted tools (including deep research assistants and large language models) for drafting, restructuring, editorial refinement, LaTeX formatting, and assistance with Python reproduction scripts under continuous human direction and oversight. Following the use of these tools, the author independently audited, executed, validated, and edited all empirical code, mathematical formulations, figure visualizations, and manuscript text. The author assumes full personal responsibility for the factual validity, scientific integrity, and conclusions presented in this publication.</p>

<div class="section-title">Acknowledgements</div>
<p>The author acknowledges and thanks the open-source scientific computing ecosystem (Python, NumPy, SciPy, Matplotlib) whose open libraries made the simulation and analysis possible.</p>

<div class="section-title">Data and Code Availability</div>
<p>The complete source code, 50-seed deterministic trajectory datasets, configuration files, and turnkey reproduction scripts (<code>reproduce_all.py</code>) associated with this study are openly available in the GitHub repository at <a href="https://github.com/Kunallubhana77/DWMA-developmental-world-model-ai">https://github.com/Kunallubhana77/DWMA-developmental-world-model-ai</a> and permanently preserved with open access in the Zenodo research archive at <a href="https://doi.org/10.5281/zenodo.22796871">https://doi.org/10.5281/zenodo.22796871</a>.</p>

</body>
</html>
"""
    out_pdf = os.path.join(SUB_DIR, "Title_Page_Kunal_Lubhana.pdf")
    compile_html_to_pdf(html, out_pdf)

def build_anonymized_manuscript():
    src_html = os.path.join(BASE_DIR, "archive", "legacy_drafts", "DWMA_Research_Paper_Preprint_v2.1.html")
    with open(src_html, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Anonymize Author Block
    content = content.replace("Kunal Lubhana", "Anonymous Author(s)")
    content = content.replace("Independent Research", "Affiliation Omitted for Double-Blind Review")
    content = content.replace("techqubit77@gmail.com", "[omitted for blind review]")
    content = content.replace("https://github.com/Kunallubhana77/DWMA-developmental-world-model-ai", "https://github.com/[anonymized-project-repo]")
    content = content.replace("10.5281/zenodo.22796871", "[Zenodo DOI reserved]")
    
    # Claim calibrations
    content = content.replace(
        "completely avoiding the catastrophic forgetting of single-model overwriting",
        "effectively mitigating catastrophic forgetting through multi-schema preservation (R = 0.9901 +/- 0.0141 vs R = -72.97)"
    )
    content = content.replace(
        "To substantiate the causal mechanisms underlying DWMA and demonstrate that performance is not an artifact of handcrafted constants, we executed an ablation suite across N = 50 seeds.",
        "To empirically evaluate the functional contributions of individual architectural components and verify operational stability across non-stationary regimes, we executed an ablation suite across N = 50 seeds."
    )
    content = content.replace(
        "To substantiate the causal contributions of DWMA's architectural components",
        "To empirically evaluate the functional contributions of DWMA's architectural components"
    )
    
    # Add Generative AI declaration before References
    ai_decl = """
    <h2>Declaration of Generative AI and AI-Assisted Technologies</h2>
    <p>During the preparation of this work, the author utilized generative AI and AI-assisted tools (including deep research assistants and large language models) for drafting, restructuring, editorial refinement, LaTeX formatting, and assistance with Python reproduction scripts under continuous human direction and oversight. Following the use of these tools, the author independently audited, executed, validated, and edited all empirical code, mathematical formulations, figure visualizations, and manuscript text. The author assumes full personal responsibility for the factual validity, scientific integrity, and conclusions presented in this publication.</p>
    """
    if "<h2>10. References</h2>" in content:
        content = content.replace("<h2>10. References</h2>", ai_decl + "\n<h2>10. References</h2>")
    elif "<h2>References</h2>" in content:
        content = content.replace("<h2>References</h2>", ai_decl + "\n<h2>References</h2>")
    
    out_pdf = os.path.join(SUB_DIR, "DWMA_Manuscript_Anonymized.pdf")
    compile_html_to_pdf(content, out_pdf)

if __name__ == '__main__':
    build_title_page()
    build_anonymized_manuscript()
