# Scientific Audit & Claim Calibration for Cognitive Systems Research

## Objective
To rigorously align every claim, generalization, and conclusion in the DWMA manuscript with the exact empirical evidence obtained across the 50-seed audited evaluation program. This audit eliminates over-claiming and ensures full defensibility during peer review.

---

## Calibrated Claims Matrix

| Component | Preprint / Draft Wording | Peer-Reviewed Journal Calibrated Wording | Scientific Justification |
| :--- | :--- | :--- | :--- |
| **Ablation Mechanism** | *"substantiates the causal mechanisms of active inference"* | *"empirically characterizes the functional roles of individual architectural components in preventing specific failure modes"* | The ablations measure performance degradation upon removing or altering components; "functional roles" is strictly descriptive of the ablation protocol, avoiding metaphysical overstatement of causal proof. |
| **Continual Retention** | *"guarantees zero catastrophic forgetting"* | *"achieves an empirical retention score of $\mathcal{R} = 0.9901 \pm 0.0141$, demonstrating robust preservation against domain interference compared to monolithic overwriting ($\mathcal{R} = -72.97$)"* | The empirical evidence shows near-complete retention ($\sim 99\%$) across 50 paired seeds in the evaluated task distribution; absolute mathematical guarantees ("zero forgetting") cannot be claimed empirically. |
| **Active Inference Speedup** | *"proves the fundamental superiority of epistemic action selection"* | *"demonstrates a statistically significant acceleration in hypothesis discrimination latency ($2.43\times$ reduction in median steps, log-rank $\chi^2 = 74.98, p < 10^{-17}$)"* | Empirical statistical testing (Kaplan-Meier survival analysis with decoupled RNG) demonstrates hypothesis discrimination acceleration within the simulated domain; phrasing is calibrated to observed statistical significance. |
| **Scope of Generality** | *"universal sensorimotor structure acquisition"* | *"autonomous online sensorimotor structure acquisition within parameterized 2D continuous dynamical environments"* | Accurately bounds the domain of validity to continuous 2D symplectic simulations, explicitly noting 3D physical scaling as future work. |
| **Baseline Comparisons** | *"outperforms all alternative world models"* | *"substantially reduces one-step-ahead forecasting error relative to standard persistence, linear autoregression, and non-adaptive baselines ($8.8\times$ MSE reduction, Cohen's $d = 11.45$)"* | Specifically grounds the comparison to the actual evaluated baseline class in BenchmarkScenarios. |

---

## Architectural Grounding for Cognitive Systems Research

1. **Cognitive Architecture Framing**:
   DWMA is framed not as an ad-hoc ML benchmark or heuristic agent, but as a modular cognitive architecture integrating:
   - **Perceptual Processing**: Reafference cancellation inspired by von Holst & Mittelstaedt (1950).
   - **Forward Modeling**: Recursive state and parameter estimation rooted in predictive processing (Friston, 2010).
   - **Multi-Schema Long-Term Memory**: Discrete schema formation and rapid Bayesian context switching, addressing stability-plasticity dilemmas (Grossberg, 1982).
   - **Epistemic Motivation**: Information-seeking exploratory drives analogous to infant developmental play (Piaget, 1952; Gopnik, 2012).

2. **Statistical Transparency**:
   - $N = 50$ paired deterministic seeds.
   - Non-parametric bootstrap resampling ($B = 10,000$) for 95% confidence intervals.
   - Non-overlapping confidence bounds and effect sizes (Cohen's $d$, Kaplan-Meier median survival latency).
   - Fair decoupled-RNG protocol for Phase 4 active vs. passive hypothesis discrimination.
