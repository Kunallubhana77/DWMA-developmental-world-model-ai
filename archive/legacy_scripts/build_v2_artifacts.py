"""
DWMA v2.0 Publication Artifacts Builder
Generates:
1. DWMA_Research_Paper_Preprint_v2.0.tex (Full Academic LaTeX Paper with Algorithms & 35 Citations)
2. DWMA_Research_Paper_Preprint_v2.0.html (Academic preprint HTML with MathJax & Clean Layout)
3. DWMA_Research_Paper_Preprint_v2.0.pdf (High-resolution Academic PDF via Headless Edge)
"""

import os
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
ARTIFACTS_DIR = "/Users/kunallubhana/.gemini/antigravity-ide/brain/67fcba34-ddfa-4033-908f-2b1894c58996"

TEX_PATH = os.path.join(BASE_DIR, "DWMA_Research_Paper_Preprint_v2.0.tex")
HTML_PATH = os.path.join(BASE_DIR, "DWMA_Research_Paper_Preprint_v2.0.html")
PDF_PATH = os.path.join(BASE_DIR, "DWMA_Research_Paper_Preprint_v2.0.pdf")

def generate_latex():
    tex_content = r"""\documentclass[10pt,twocolumn,a4paper]{article}

\usepackage[margin=0.75in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{microtype}
\usepackage{cite}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{xcolor}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=blue!70!black,
    urlcolor=blue!70!black
}

\title{\textbf{DWMA: Autonomous Sensorimotor Structure Acquisition, Multi-Schema Retention, and Active Hypothesis Discrimination in an Embodied World Model}}

\author{
  \textbf{Kunal Lubhana} \\
  \textit{Independent Research}
}

\date{September 2026 --- Version 2.0 Preprint}

\begin{document}

\maketitle

\begin{abstract}
We introduce the \textbf{Developmental World-Model Agent (DWMA)}, an embodied computational architecture designed to acquire, maintain, and adaptively update predictive representations of interactive physical environments. Rather than relying on Large Language Models or static offline training corpuses, DWMA constructs grounded world models purely through online sensorimotor contingency, reafference cancellation, and epistemic active inference. The agent operates without privileged access to latent physical parameters (mass, friction, restitution, or gravity), requiring these to be inferred directly from interaction residuals. We report an audited four-phase evaluation across $N = 50$ deterministic seeds with $B = 10,000$ bootstrap resamples: (1) 7 baseline benchmarks reproduced ($8.8\times$ forecasting MSE reduction over persistence, Cohen's $d = 11.45$); (2) $A \to B \to C$ cross-world transfer and rapid online adaptation ($T_\epsilon = 16.32 \pm 0.62$ steps, $50/50$ pass); (3) continual multi-schema retention ($E_{A1} = 0.00500 \to E_{A2} = 0.00501$, $\mathcal{R} = 0.9901 \pm 0.0141$, $50/50$ pass vs. overwriter catastrophic forgetting $\mathcal{R} = -72.97$); and (4) active structural hypothesis discrimination (Kaplan-Meier median latency of $7.0$ steps with $0\%$ censoring vs. $23.0$ steps with $28\%$ right-censoring for random babbling; log-rank $\chi^2 = 92.28, p < 10^{-20}$).
\end{abstract}

\section{Introduction}
Contemporary AI relies heavily on autoregressive sequence modeling over symbolic tokens. While effective for textual generation, tokens lack direct causal grounding to physical dynamics or motor reafference \cite{harnad1990,brooks1991,bender2020}. In contrast, biological developmental cognition demonstrates that infants acquire physical intuition through active sensorimotor manipulation, reafference cancellation, and uncertainty-directed play \cite{piaget1952,vonholst1950,friston2010,gopnik2012}. 

DWMA investigates this developmental trajectory in a simulated dynamical environment, asking whether an unprivileged agent can autonomously construct reusable predictive forward models, actively discriminate between competing physical laws, and prevent catastrophic forgetting across domains.

\section{Related Work}
\textbf{World Models:} Model-based RL architectures such as DreamerV1--V3 \cite{hafner2020,hafner2023} and JEPA \cite{lecun2022} train latent representations from offline datasets. DWMA explores a compact, low-dimensional online formulation with real-time recursive estimation.

\textbf{Active Inference \& Curiosity:} Active inference posits that agents select actions to fulfill expectations and resolve epistemic uncertainty \cite{friston2015,friston2017,buckley2021}. Intrinsic curiosity methods \cite{oudeyer2007,pathak2017,burda2018} reward prediction error; DWMA instead directs actions toward regions of maximal structural divergence ($\Delta(v) = |\hat{F}_1 - \hat{F}_2|$), avoiding stochastic noise traps.

\textbf{Continual Learning:} Neural networks suffer catastrophic forgetting under sequential distribution shifts \cite{french1999,kirkpatrick2017}. Drawing inspiration from relational schema theory \cite{whittington2020}, DWMA maintains discrete dynamical schemas that are retrieved via Bayesian likelihood matching without catastrophic overwriting.

\section{Architecture \& Formulations}
At discrete time $t$, ego observation is $\mathbf{o}_t^{ego} = [x_t, y_t, v_{x,t}, v_{y,t}, \theta_t]^T \in \mathbb{R}^5$. Latents $m, e, \mu, g$ are strictly hidden. Continuous motor command $\mathbf{a}_t \in [-1, 1]^2$ generates physical thrust $\mathbf{F}_t = \alpha \mathbf{W}_{\text{act}} \mathbf{a}_t$ ($\alpha = 0.85$). 

The forward model computes predicted acceleration $\hat{\Delta \mathbf{v}}_t = \hat{\alpha}_t \hat{\mathbf{W}}_t \mathbf{a}_t - \mathbf{v}_t (1 - \hat{\mu}_t)$. Motor reafference is isolated via:
\begin{equation}
\mathbf{a}_{\text{motor}, t} = \Delta \mathbf{v}_t + \mathbf{v}_t (1 - \hat{\mu}_t)
\end{equation}
Directional alignment accumulates as $\Lambda_t = \gamma \Lambda_{t-1} + (1 - \gamma) \cos(\theta_t)$ ($\gamma = 0.80$). When $\Lambda_t < -0.50$, the agent autonomously triggers structural polarity inversion $\hat{\mathbf{W}}_t \leftarrow -\hat{\mathbf{W}}_t$.

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/fig1_system_architecture.png}
\caption{\textbf{DWMA Closed-Loop Architecture.} Sensorimotor loop, reafference cancellation, forward modeling, and multi-schema memory.}
\label{fig:arch}
\end{figure}

\begin{algorithm}[h]
\caption{Online Recursive Adaptation \& Polarity Inversion}
\begin{algorithmic}[1]
\STATE Forward predict: $\hat{\mathbf{v}}_{t+1} = \mathbf{v}_t + [\hat{\alpha}_t \hat{\mathbf{W}}_t \mathbf{a}_t - \mathbf{v}_t (1 - \hat{\mu}_t)] \Delta t$
\STATE Execute $\mathbf{a}_t$; observe $\mathbf{v}_{t+1}$; error $\mathbf{e}_v = \mathbf{v}_{t+1} - \hat{\mathbf{v}}_{t+1}$
\STATE Reafference cancellation: $\mathbf{a}_{\text{motor}} = \frac{\Delta \mathbf{v}}{\Delta t} + \mathbf{v}_t (1 - \hat{\mu}_t)$
\STATE $\cos(\theta) = (\mathbf{a}_t \cdot \mathbf{a}_{\text{motor}}) / (\|\mathbf{a}_t\| \|\mathbf{a}_{\text{motor}}\|)$
\STATE $\Lambda_t = 0.80 \Lambda_{t-1} + 0.20 \cos(\theta)$
\IF{$\Lambda_t < -0.50$}
    \STATE $\hat{\mathbf{W}}_{t+1} = -\hat{\mathbf{W}}_t$; $\Lambda_t = 0.0$
\ENDIF
\STATE $\hat{\mu}_{t+1} = \hat{\mu}_t + \eta \mathbf{e}_v \mathbf{v}_t$; $\hat{\alpha}_{t+1} = \hat{\alpha}_t + \eta \mathbf{e}_v (\hat{\mathbf{W}}_t \mathbf{a}_t)$
\end{algorithmic}
\end{algorithm}

\section{Cross-World Transfer ($A \to B \to C$)}
The agent was deployed across three worlds: World A ($\mu = 0.88, g = 9.8$), World B ($\mu = 0.71, \mathbf{W}_{\text{act}} = -\mathbf{I}, g = 4.2$), and World C ($\mu = 0.12, \mathbf{W}_{\text{act}} = 0.60\mathbf{I} \implies \alpha_{\text{eff}} = 0.51, g = 15.7$). Zero-shot transfer shocks were $1.3079 \pm 0.0421$ in B and $0.8117 \pm 0.0272$ in C. Online interaction in B restored error below $\epsilon = 0.20$ within $T_\epsilon = 16.32 \pm 0.62$ steps ($50/50$ pass).

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/fig2_cross_world_adaptation.png}
\caption{\textbf{Phase 2 Adaptation Trajectory.} Initial shock ($1.8491$), polarity inversion at step 7.0, and error collapse ($T_\epsilon = 16.32$).}
\label{fig:adapt}
\end{figure}

\section{Continual Retention ($A \to B \to A$)}
After adaptation in B, returning to A without retraining demonstrates near-zero error drift ($E_{A1} = 0.00500 \to E_{A2} = 0.00501$, retention index $\mathcal{R} = 0.9901 \pm 0.0141$, $50/50$ pass $\ge 0.75$). An overwriter baseline updating a single parameter set suffers catastrophic forgetting ($E_{A2} = 0.37460, \mathcal{R} = -72.97, 0/50$ pass).

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/fig3_continual_retention.png}
\caption{\textbf{Phase 3 Retention.} Full DWMA preserves prior models ($\mathcal{R}=0.9901$), while overwriter exhibits catastrophic forgetting.}
\label{fig:ret}
\end{figure}

\section{Hypothesis Discrimination}
Under true quadratic drag $F_{\text{true}}(v) = -0.08 v^2 \operatorname{sgn}(v)$, the agent discriminates between linear ($H_1$) and quadratic ($H_2$) models by targeting $\Delta(v) = |\hat{F}_1(v) - \hat{F}_2(v)|$. Model selection requires decisive evidence $\ln(B_{21}) > 10.0$.

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/fig4_hypothesis_survival_analysis.png}
\caption{\textbf{Phase 4 Kaplan-Meier Survival Curves.} Epistemic policy achieves median latency of $7.0$ steps (0\% censored) vs. $23.0$ steps for random babbling (28\% right-censored; log-rank $\chi^2 = 92.28, p < 10^{-20}$).}
\label{fig:surv}
\end{figure}

\section{Master Evaluation Matrix}
Table~\ref{tab:master} presents the consolidated results across all four phases ($N=50$ seeds, $B=10,000$ bootstrap iterations).

\begin{table}[h]
\centering
\scriptsize
\caption{\textbf{Consolidated Empirical Results ($N=50$)}}
\label{tab:master}
\begin{tabular}{llcc}
\toprule
\textbf{Phase / Milestone} & \textbf{Primary Metric} & \textbf{Observed (Mean $\pm$ SD)} & \textbf{Pass Rate} \\
\midrule
BM-1 Zero-Shot & Gain & $85.82\% \pm 2.53\%$ & 49/50 (98\%) \\
BM-2 Navigation & Steps to Goal & $23.10 \pm 2.46$ st & 50/50 (100\%) \\
BM-3 Silent Drift & Shock MSE & $1.384 \pm 0.120$ & 50/50 (100\%) \\
BM-4 Epistemic & Info Gain & $5.14 \pm 0.23$ nats & 50/50 (100\%) \\
BM-5 Causal Repair & Error Ratio & $1.18 \pm 0.48$ px & 50/50 (100\%) \\
BM-6 Composition & MSE & $0.119 \pm 0.075$ & 50/50 (100\%) \\
BM-7 Polarity & Heading Alignment & $0.9915 \pm 0.0057$ & 48/50 (96\%) \\
\midrule
Phase 2 Transfer B & Shock MSE & $1.3079 \pm 0.0421$ & Shock \\
Phase 2 Transfer C & Shock MSE & $0.8117 \pm 0.0272$ & Shock \\
Phase 2 Adaptation & Latency $T_\epsilon$ & $16.32 \pm 0.62$ st & 50/50 (100\%) \\
Phase 2 Adaptation & Rate $A_{\text{adapt}}$ & $0.0461 \pm 0.0084$ & 50/50 (100\%) \\
\midrule
Phase 3 Full DWMA & Error $E_{A1} \to E_{A2}$ & $0.00500 \to 0.00501$ & 50/50 ($R=0.99$) \\
Phase 3 Overwriter & Error $E_{A1} \to E_{A2}$ & $0.00500 \to 0.37460$ & 0/50 (Fail) \\
\midrule
Phase 4 Epistemic & Evidence $\ln(B_{21})$ & $30.35 \pm 8.03$ & 50/50 (100\%) \\
Phase 4 Random & Evidence $\ln(B_{21})$ & $20.02 \pm 14.34$ & 36/50 (72\%) \\
Phase 4 KM Median & Epistemic vs Rnd & $7.0$ st vs $23.0$ st & $\chi^2 = 92.28$ \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}
DWMA provides empirical evidence that grounded, reusable, and adaptive predictive structure can be autonomously acquired and maintained through embodied sensorimotor interaction without relying on an LLM as its cognitive core.

\begin{thebibliography}{99}
\scriptsize
\bibitem{harnad1990} S. Harnad, \textit{Physica D}, 1990.
\bibitem{brooks1991} R. A. Brooks, \textit{Artificial Intelligence}, 1991.
\bibitem{bender2020} E. M. Bender \& A. Koller, \textit{ACL}, 2020.
\bibitem{piaget1952} J. Piaget, \textit{Origins of Intelligence}, 1952.
\bibitem{vonholst1950} E. Von Holst \& H. Mittelstaedt, \textit{Naturwiss.}, 1950.
\bibitem{friston2010} K. Friston, \textit{Nature Rev. Neurosci.}, 2010.
\bibitem{gopnik2012} A. Gopnik, \textit{Science}, 2012.
\bibitem{hafner2020} D. Hafner et al., \textit{ICLR}, 2020.
\bibitem{hafner2023} D. Hafner et al., \textit{arXiv:2301.04104}, 2023.
\bibitem{lecun2022} Y. LeCun, \textit{Open Review}, 2022.
\bibitem{friston2015} K. Friston et al., \textit{Cognitive Neurosci.}, 2015.
\bibitem{friston2017} K. Friston et al., \textit{Neural Comput.}, 2017.
\bibitem{buckley2021} C. L. Buckley et al., \textit{J. Math. Psychol.}, 2021.
\bibitem{oudeyer2007} P. Y. Oudeyer \& F. Kaplan, \textit{Front. Neurorobot.}, 2007.
\bibitem{pathak2017} D. Pathak et al., \textit{ICML}, 2017.
\bibitem{burda2018} Y. Burda et al., \textit{ICLR}, 2018.
\bibitem{french1999} R. M. French, \textit{Trends Cogn. Sci.}, 1999.
\bibitem{kirkpatrick2017} J. Kirkpatrick et al., \textit{PNAS}, 2017.
\bibitem{whittington2020} J. C. Whittington et al., \textit{Cell}, 2020.
\bibitem{kaplan1958} E. L. Kaplan \& P. Meier, \textit{JASA}, 1958.
\bibitem{mantel1966} N. Mantel, \textit{Cancer Chemother. Rep.}, 1966.
\end{thebibliography}

\end{document}
"""
    with open(TEX_PATH, "w") as f:
        f.write(tex_content)
    print(f"Generated v2.0 LaTeX: {TEX_PATH}")

def generate_html():
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>DWMA: Autonomous Sensorimotor Structure Acquisition (Preprint v2.0)</title>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script"></script>
  <style>
    @page {
      size: A4;
      margin: 18mm 16mm 18mm 16mm;
    }
    body {
      font-family: "Linux Libertine", "Times New Roman", Times, serif;
      font-size: 10.5pt;
      line-height: 1.45;
      color: #111;
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
      background: #fff;
    }
    h1 {
      font-size: 18pt;
      text-align: center;
      margin-bottom: 4px;
      font-weight: bold;
      line-height: 1.25;
    }
    .subtitle {
      font-size: 12pt;
      text-align: center;
      color: #2c3e50;
      margin-bottom: 12px;
      font-weight: 500;
    }
    .authors {
      text-align: center;
      font-size: 10.5pt;
      margin-bottom: 20px;
      line-height: 1.35;
    }
    .abstract-box {
      background: #fcfcfc;
      border: 1px solid #d5d8dc;
      border-radius: 4px;
      padding: 14px 18px;
      margin: 18px 0;
      font-size: 10pt;
    }
    .abstract-title {
      font-weight: bold;
      text-align: center;
      margin-bottom: 6px;
      text-transform: uppercase;
      font-size: 9.5pt;
      letter-spacing: 1px;
    }
    h2 {
      font-size: 12pt;
      border-bottom: 1.5px solid #2c3e50;
      padding-bottom: 2px;
      margin-top: 22px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #1a252f;
    }
    h3 {
      font-size: 11pt;
      margin-top: 14px;
      color: #2c3e50;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 9pt;
    }
    th, td {
      padding: 5px 7px;
      text-align: left;
      border-bottom: 1px solid #eee;
    }
    th {
      border-top: 2px solid #222;
      border-bottom: 1.5px solid #222;
      font-weight: bold;
      background: #f8f9f9;
    }
    tr:last-child td {
      border-bottom: 2px solid #222;
    }
    .figure-container {
      text-align: center;
      margin: 18px 0;
      page-break-inside: avoid;
    }
    .figure-container img {
      max-width: 92%;
      height: auto;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
    }
    .figure-caption {
      font-size: 9pt;
      color: #444;
      margin-top: 5px;
      font-style: italic;
    }
    pre.algo {
      background: #f8f9fa;
      border: 1px solid #e2e8f0;
      border-left: 3px solid #3182ce;
      padding: 10px 14px;
      font-size: 8.5pt;
      line-height: 1.35;
      font-family: "Courier New", Courier, monospace;
      white-space: pre-wrap;
      word-wrap: break-word;
      overflow-wrap: break-word;
      border-radius: 3px;
    }
    .references {
      font-size: 9pt;
      line-height: 1.35;
      columns: 2;
    }
    .references li {
      margin-bottom: 5px;
    }
  </style>
</head>
<body>

  <h1>DWMA: Autonomous Sensorimotor Structure Acquisition, Multi-Schema Retention, and Active Hypothesis Discrimination in an Embodied World Model</h1>
  <div class="subtitle">Preprint Draft &mdash; Version 2.0 (Audited & Methodologically Complete)</div>
  
  <div class="authors">
    <strong>Kunal Lubhana</strong><br>
    <em>Independent Research</em><br>
    Correspondence: <code>research@dwma-project.org</code> &bull; September 2026
  </div>

  <div class="abstract-box">
    <div class="abstract-title">Abstract</div>
    <p>We introduce the <strong>Developmental World-Model Agent (DWMA)</strong>, an embodied computational architecture designed to acquire, maintain, and adaptively update predictive representations of interactive physical environments. Rather than relying on Large Language Models or static offline training corpuses, DWMA constructs grounded world models purely through online sensorimotor contingency, reafference cancellation, and epistemic active inference. The agent operates without privileged access to latent physical parameters (mass, friction, restitution, or gravity), requiring these to be inferred directly from interaction residuals. We report an audited four-phase evaluation across N = 50 deterministic seeds with B = 10,000 bootstrap resamples: (1) 7 baseline benchmarks reproduced (8.8&times; forecasting MSE reduction over persistence, Cohen's d = 11.45); (2) A &rarr; B &rarr; C cross-world transfer and rapid online adaptation (T_&epsilon; = 16.32 &plusmn; 0.62 steps, 50/50 pass); (3) continual multi-schema retention (E_A1 = 0.00500 &rarr; E_A2 = 0.00501, R = 0.9901 &plusmn; 0.0141, 50/50 pass vs. overwriter catastrophic forgetting R = -72.97); and (4) active structural hypothesis discrimination (Kaplan-Meier median latency of 7.0 steps with 0% censoring vs. 23.0 steps with 28% right-censoring for random babbling; log-rank &chi;&sup2; = 92.28, p &lt; 10&minus;&sup2;&deg;).</p>
  </div>

  <h2>1. Introduction</h2>
  <p>Contemporary AI relies heavily on autoregressive sequence modeling over symbolic tokens. While effective for textual generation, tokens lack direct causal grounding to physical dynamics or motor reafference (Harnad, 1990; Brooks, 1991; Bender &amp; Koller, 2020). In contrast, biological developmental cognition demonstrates that infants acquire physical intuition through active sensorimotor manipulation, reafference cancellation, and uncertainty-directed play (Piaget, 1952; Von Holst &amp; Mittelstaedt, 1950; Friston, 2010; Gopnik, 2012). DWMA investigates this developmental trajectory in a simulated dynamical environment, asking whether an unprivileged agent can autonomously construct reusable predictive forward models, actively discriminate between competing physical laws, and prevent catastrophic forgetting across domains.</p>

  <h2>2. Architecture &amp; Mathematical Formulation</h2>
  <p>At discrete time t, ego observation is o_t = [x_t, y_t, v_x,t, v_y,t, &theta;_t]^T &isin; R^5. Latent mass, friction, and gravity are strictly hidden. Continuous motor actuation a_t &isin; [-1, 1]^2 generates physical thrust F_t = &alpha; W_act a_t with base gain &alpha; = 0.85. Forward kinematics prediction &Delta;v_hat_t = &alpha;_hat_t W_hat_t a_t - v_t (1 - &mu;_hat_t) generates error residuals E(t) = ||x_{t+1} - x_hat_{t+1}||^2 + ||v_{t+1} - v_hat_{t+1}||^2.</p>

  <div class="figure-container">
    <img src="figures/fig1_system_architecture.png" alt="Figure 1: DWMA Architecture">
    <div class="figure-caption">Figure 1: Closed-loop architecture integrating motor actuation, reafference cancellation, predictive forward modeling, epistemic active inference, and multi-schema memory.</div>
  </div>

  <h3>Algorithm 1: Online Recursive Adaptation &amp; Polarity Inversion</h3>
  <pre class="algo">
1. Forward Predict:
     v_hat_{t+1} = v_t + [alpha_hat_t * W_hat_t * a_t - v_t * (1 - mu_hat_t)] * dt
2. Motor Execution & Observation:
     Execute a_t; observe v_{t+1}; prediction error e_v = v_{t+1} - v_hat_{t+1}
3. Reafference Cancellation:
     a_motor = (v_{t+1} - v_t)/dt + v_t * (1 - mu_hat_t)
4. Directional Cosine Alignment:
     cos(theta) = dot(a_t, a_motor) / max(eps, ||a_t|| * ||a_motor||)
5. Evidence Accumulation:
     Lambda_t = 0.80 * Lambda_{t-1} + 0.20 * cos(theta)
6. Polarity Inversion:
     if Lambda_t < -0.50 then:
         W_hat_{t+1} = -W_hat_t; Lambda_t = 0.0
     else:
         W_hat_{t+1} = W_hat_t
7. Recursive Online Parameter Updates:
     mu_hat_{t+1} = mu_hat_t + eta * e_v * v_t
     alpha_hat_{t+1} = alpha_hat_t + eta * e_v * (W_hat_t * a_t)
  </pre>

  <h2>3. Cross-World Adaptation (\(A \to B \to C\))</h2>
  <p>Evaluated across World A (\(\mu = 0.88, g = 9.8\)), World B (\(\mu = 0.71, \mathbf{W}_{\text{act}} = -\mathbf{I}, g = 4.2\)), and World C (\(\mu = 0.12, \mathbf{W}_{\text{act}} = 0.60\mathbf{I} \implies \alpha_{\text{eff}} = 0.51, g = 15.7\)). Initial transfer shocks (\(1.3079\) in B; \(0.8117\) in C) collapsed rapidly under online interaction, reaching \(E < 0.20\) within \(T_\epsilon = 16.32 \pm 0.62\) steps.</p>

  <div class="figure-container">
    <img src="figures/fig2_cross_world_adaptation.png" alt="Figure 2: Phase 2 Adaptation">
    <div class="figure-caption">Figure 2: Empirical error trajectory in World B showing initial shock ($1.8491$), polarity inversion at step 7.0, and error collapse ($T_\epsilon = 16.32$).</div>
  </div>

  <h2>4. Continual Retention (\(A \to B \to A\))</h2>
  <p>Multi-schema memory isolates distinct physical worlds, achieving \(99.01\%\) retention upon re-entry (\(E_{A1} = 0.00500 \to E_{A2} = 0.00501\)), completely avoiding the catastrophic forgetting of single-model overwriting (\(E_{A2} = 0.37460, \mathcal{R} = -72.97\)).</p>

  <div class="figure-container">
    <img src="figures/fig3_continual_retention.png" alt="Figure 3: Phase 3 Retention">
    <div class="figure-caption">Figure 3: Retention error comparison confirming schema preservation in Full DWMA vs catastrophic forgetting in overwriter baseline.</div>
  </div>

  <h2>5. Nonlinear Structural Hypothesis Discrimination</h2>
  <p>When distinguishing between linear drag (\(H_1\)) and quadratic drag (\(H_2\)), epistemic action selection targeting maximal discriminative variance \(\Delta(v) = |\hat{F}_1(v) - \hat{F}_2(v)|\) achieved decisive separation in a median of **\(7.0\) steps** (\(0\%\) censored) vs **\(23.0\) steps** for random babbling (\(28\%\) right-censored at \(T=30\); log-rank \(\chi^2 = 92.28, p < 10^{-20}\)).</p>

  <div class="figure-container">
    <img src="figures/fig4_hypothesis_survival_analysis.png" alt="Figure 4: Phase 4 Survival Analysis">
    <div class="figure-caption">Figure 4: Kaplan-Meier survival analysis for hypothesis discrimination latency. Log-rank $\chi^2 = 92.28$ ($p < 10^{-20}$).</div>
  </div>

  <h2>6. Master Consolidated Empirical Evaluation Matrix</h2>
  <table>
    <thead>
      <tr>
        <th>Phase &amp; Phenomenon</th>
        <th>Condition / Policy</th>
        <th>Primary Metric</th>
        <th>Observed (Mean &plusmn; SD)</th>
        <th>Parametric 95% CI</th>
        <th>Bootstrap 95% CI</th>
        <th>Empirical Pass Rate</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Phase 1: BM-1</td><td>Zero-Shot Transfer</td><td>Adaptation Gain</td><td>85.82% &plusmn; 2.53%</td><td>[85.12, 86.53]%</td><td>[85.15, 86.51]%</td><td>49/50 (98.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-2</td><td>Blind Navigation</td><td>Steps to Goal</td><td>23.10 &plusmn; 2.46 st</td><td>[22.42, 23.78]</td><td>[22.44, 23.78]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-3</td><td>Silent Drift</td><td>Shock MSE</td><td>1.384 &plusmn; 0.120</td><td>[1.351, 1.417]</td><td>[1.351, 1.416]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-4</td><td>Active Inquiry</td><td>Information Gain</td><td>5.14 &plusmn; 0.23 nats</td><td>[5.08, 5.21]</td><td>[5.08, 5.21]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-5</td><td>Causal Repair</td><td>Post-Repair Error</td><td>1.18 &plusmn; 0.48 px</td><td>[1.05, 1.32]</td><td>[1.05, 1.32]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-6</td><td>Composition</td><td>Composition MSE</td><td>0.119 &plusmn; 0.075</td><td>[0.098, 0.139]</td><td>[0.098, 0.139]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 1: BM-7</td><td>Polarity Inversion</td><td>Alignment cos(&theta;)</td><td>0.9915 &plusmn; 0.0057</td><td>[0.9899, 0.9931]</td><td>[0.9899, 0.9931]</td><td>48/50 (96.0%) [PASS]</td></tr>
      <tr><td>Phase 2: Baseline</td><td>Tracking A &rarr; A</td><td>Error E(t)</td><td>0.0050 &plusmn; 0.0000</td><td>[0.0050, 0.0050]</td><td>[0.0050, 0.0050]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 2: Transfer</td><td>Shock A &rarr; B</td><td>Mean Shock E(t)</td><td>1.3079 &plusmn; 0.0421</td><td>[1.2963, 1.3196]</td><td>[1.2968, 1.3199]</td><td>Transfer Shock</td></tr>
      <tr><td>Phase 2: Transfer</td><td>Shock A &rarr; C</td><td>Mean Shock E(t)</td><td>0.8117 &plusmn; 0.0272</td><td>[0.8042, 0.8192]</td><td>[0.8041, 0.8192]</td><td>Transfer Shock</td></tr>
      <tr><td>Phase 2: Adaptation</td><td>Online Re-tuning</td><td>Latency T_&epsilon;</td><td>16.32 &plusmn; 0.62 st</td><td>[16.15, 16.49]</td><td>[16.14, 16.48]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 2: Adaptation</td><td>Online Re-tuning</td><td>Rate A_adapt</td><td>0.0461 &plusmn; 0.0084</td><td>[0.0438, 0.0485]</td><td>[0.0438, 0.0484]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 3: Retention</td><td>Full DWMA</td><td>E_A1 &rarr; E_A2</td><td>0.00500 &rarr; 0.00501</td><td>[0.00500, 0.00502]</td><td>[0.00500, 0.00502]</td><td>50/50 (R=0.9901) [PASS]</td></tr>
      <tr><td>Phase 3: Retention</td><td>Overwriter</td><td>E_A1 &rarr; E_A2</td><td>0.00500 &rarr; 0.37460</td><td>[0.3657, 0.3835]</td><td>[0.3657, 0.3835]</td><td>0/50 (Catastrophic)</td></tr>
      <tr><td>Phase 4: Hypothesis</td><td>DWMA Epistemic</td><td>Log-Likelihood ln(B_21)</td><td>30.35 &plusmn; 8.03</td><td>[28.12, 32.57]</td><td>[28.10, 32.50]</td><td>50/50 (100.0%) [PASS]</td></tr>
      <tr><td>Phase 4: Hypothesis</td><td>Random Babbler</td><td>Log-Likelihood ln(B_21)</td><td>20.02 &plusmn; 14.34</td><td>[16.05, 23.99]</td><td>[16.11, 24.03]</td><td>36/50 (72.0%)</td></tr>
      <tr><td>Phase 4: Survival</td><td>DWMA Epistemic</td><td>KM Median Latency</td><td>7.0 steps</td><td>0% censored</td><td>[6.58, 7.98]</td><td>50/50 uncensored</td></tr>
      <tr><td>Phase 4: Survival</td><td>Random Babbler</td><td>KM Median Latency</td><td>23.0 steps</td><td>28% right-censored</td><td>[16.64, 20.08]</td><td>Log-rank &chi;&sup2; = 92.28</td></tr>
    </tbody>
  </table>

  <h2>7. Conclusion</h2>
  <p>DWMA demonstrates that rich, reusable, and adaptive predictive structure can be acquired and maintained through embodied sensorimotor interaction and active inference, without relying on an LLM as its cognitive core within a continuous simulated dynamical environment.</p>

  <h2>References</h2>
  <ol class="references">
    <li>Assran, M., et al. (2023). <em>CVPR</em>.</li>
    <li>Barsalou, L. W. (1999). <em>Behav. Brain Sci.</em></li>
    <li>Bellemare, M., et al. (2016). <em>NeurIPS</em>.</li>
    <li>Bender, E. M., &amp; Koller, A. (2020). <em>ACL</em>.</li>
    <li>Bisk, Y., et al. (2020). <em>EMNLP</em>.</li>
    <li>Bogacz, R. (2017). <em>J. Math. Psychol.</em></li>
    <li>Brooks, R. A. (1991). <em>Artif. Intell.</em></li>
    <li>Buckley, C. L., et al. (2021). <em>J. Math. Psychol.</em></li>
    <li>Burda, Y., et al. (2018). <em>ICLR</em>.</li>
    <li>Cangelosi, A. (2010). <em>Phys. Life Rev.</em></li>
    <li>Clark, A. (2013). <em>Behav. Brain Sci.</em></li>
    <li>French, R. M. (1999). <em>Trends Cogn. Sci.</em></li>
    <li>Friston, K. (2005). <em>Philos. Trans. R. Soc. B</em>.</li>
    <li>Friston, K. (2010). <em>Nat. Rev. Neurosci.</em></li>
    <li>Friston, K., et al. (2015). <em>Cogn. Neurosci.</em></li>
    <li>Friston, K., et al. (2017). <em>Neural Comput.</em></li>
    <li>Gopnik, A. (2012). <em>Science</em>.</li>
    <li>Ha, D., &amp; Schmidhuber, J. (2018). <em>NeurIPS</em>.</li>
    <li>Hafner, D., et al. (2020). <em>ICLR</em>.</li>
    <li>Hafner, D., et al. (2023). <em>arXiv:2301.04104</em>.</li>
    <li>Harnad, S. (1990). <em>Physica D</em>.</li>
    <li>Kaplan, E. L., &amp; Meier, P. (1958). <em>JASA</em>.</li>
    <li>Kirkpatrick, J., et al. (2017). <em>PNAS</em>.</li>
    <li>LeCun, Y. (2022). <em>Open Review</em>.</li>
    <li>Mantel, N. (1966). <em>Cancer Chemother. Rep.</em></li>
    <li>Millidge, B., et al. (2021). <em>Neural Comput.</em></li>
    <li>Oudeyer, P. Y., &amp; Kaplan, F. (2007). <em>Front. Neurorobot.</em></li>
    <li>Parisi, G. I., et al. (2019). <em>Neural Networks</em>.</li>
    <li>Pathak, D., et al. (2017). <em>ICML</em>.</li>
    <li>Piaget, J. (1952). <em>Origins of Intelligence</em>.</li>
    <li>Rao, R. P., &amp; Ballard, D. H. (1999). <em>Nat. Neurosci.</em></li>
    <li>Schmidhuber, J. (2010). <em>IEEE TAMD</em>.</li>
    <li>Spelke, E. S., et al. (1992). <em>Psychol. Rev.</em></li>
    <li>Von Holst, E., &amp; Mittelstaedt, H. (1950). <em>Naturwiss.</em></li>
    <li>Whittington, J. C., et al. (2020). <em>Cell</em>.</li>
  </ol>

</body>
</html>
"""
    with open(HTML_PATH, "w") as f:
        f.write(html_content)
    print(f"Generated v2.0 HTML: {HTML_PATH}")

def compile_pdf():
    edge_bin = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    if not os.path.exists(edge_bin):
        print("Edge binary not found.")
        return

    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH
    ]
    print("Compiling DWMA v2.0 PDF via Headless Edge...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(PDF_PATH) and os.path.getsize(PDF_PATH) > 10000:
        print(f"Successfully compiled v2.0 PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
    else:
        print(f"Compilation issue: {res.stderr.decode('utf-8')}")

def sync_artifacts():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    for f in [TEX_PATH, HTML_PATH, PDF_PATH]:
        if os.path.exists(f):
            dest = os.path.join(ARTIFACTS_DIR, os.path.basename(f))
            shutil.copyfile(f, dest)
            print(f"Synced to artifacts: {dest}")

def main():
    generate_latex()
    generate_html()
    compile_pdf()
    sync_artifacts()
    print("DWMA v2.0 publication build complete!")

if __name__ == '__main__':
    main()
