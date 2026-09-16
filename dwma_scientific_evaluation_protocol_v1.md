# DWMA Scientific Evaluation Protocol v1.0
**Document Version:** 1.0.0 (Frozen Specification)  
**System:** Developmental World-Model Agent (DWMA)  
**Cognitive Core:** Embodied Predictive-Coding & Active-Inference (Zero LLM Dependency)  
**Status:** Protocol Frozen for Empirical Benchmarking  

---

## 1. Executive Research Scope & Epistemological Boundaries
This document formalizes the experimental protocol for DWMA v1.0. All empirical claims are strictly bounded to the simulated continuous dynamical environment. No claims of general intelligence, metaphysical causality, or conscious experience are made or implied. 

The primary scientific objective of this protocol is to test:
> *Can an ungrounded computational agent autonomously build a predictive forward model, bind orthogonal sensorimotor concepts without privileged access, detect structural violations (drift and vector inversion), and execute online model repair solely via sensory contingency and epistemic active inference?*

---

## 2. Formal MDP & Cognitive Parameterization

### 2.1 State Space $\mathcal{S}$ & Observation Space $\mathcal{O}$
At each discrete time step $t \in \mathbb{N}$:
- **Ego Sensory Vector:** $\mathbf{o}_t^{ego} = [x_t, y_t, v_{x, t}, v_{y, t}, \theta_t] \in \mathbb{R}^5$
- **Entity Observation Array:** $\mathbf{o}_t^{env} = \{ (\mathbf{p}_i, \mathbf{v}_i, r_i, c_i, s_i) \}_{i=1}^{K}$
  - $\mathbf{p}_i \in \mathbb{R}^2$: Centroid coordinates in world reference frame
  - $\mathbf{v}_i \in \mathbb{R}^2$: Observed velocity
  - $r_i \in \mathbb{R}^+$: Bounding radius
  - $c_i \in \text{RGB}$: Visual spectral signature
  - $s_i \in \{\text{circle}, \text{box}, \text{diamond}, \text{polygon}, \text{pillar}\}$: Geometric silhouette
- **Non-Privileged Constraint:** The agent has **ZERO** direct access to latent physical constants:
  $$\text{mass } m_i \notin \mathcal{O}, \quad \text{restitution } e_i \notin \mathcal{O}, \quad \text{ground friction } \mu \notin \mathcal{O}$$
  All latent parameters must be inferred strictly via interaction residuals.

### 2.2 Action Space $\mathcal{A}$
Continuous motor actuation vector:
$$\mathbf{a}_t = [u_x, u_y] \in [-1.0, 1.0]^2 \subset \mathbb{R}^2$$
Actuator dynamics transform command $\mathbf{a}_t$ into applied thrust:
$$\mathbf{F}_t = \mathbf{W}_{actuator} \mathbf{a}_t \cdot \alpha$$
where $\mathbf{W}_{actuator} \in \mathbb{R}^{2 \times 2}$ (initially identity $\mathbf{I}_2$) and $\alpha = 0.85$.

### 2.3 Internal Model & Hyperparameters
- **Learning Rate:** $\eta = 0.04$
- **Initial Learned Acceleration:** $a_0 = 0.25$
- **Initial Learned Friction Damping:** $f_0 = 0.85$
- **Prior Epistemic Variance:** $\sigma_0^2 = 25.0$
- **Sensorimotor Smoothing Factor:** $\gamma = 0.90$
- **Agency Decision Threshold:** $\theta_{agency} = 0.50$

---

## 3. Standardized External Observer Protocol
To eliminate evaluation bias (apples-to-oranges ablation errors):
1. Prior to state transition execution, the **External Observer** presents current state $(\mathbf{x}_t, \mathbf{v}_t)$ and planned actuation $\mathbf{a}_t$.
2. Every agent variant must generate a state forecast:
   $$\hat{\mathbf{s}}_{t+1} = [\hat{\mathbf{x}}_{t+1}, \hat{\mathbf{v}}_{t+1}]$$
   - *Active Predictive Models:* $\hat{\mathbf{s}}_{t+1} = \mathcal{M}(\mathbf{s}_t, \mathbf{a}_t)$
   - *Ablated (No Predictive Model):* Defaults strictly to persistence identity $\hat{\mathbf{s}}_{t+1} = \mathbf{s}_t$.
3. The environment executes $\mathbf{s}_{t+1} \sim \mathcal{P}(\cdot \mid \mathbf{s}_t, \mathbf{a}_t)$.
4. Standardized Prediction MSE:
   $$\mathcal{L}_{MSE} = \|\hat{\mathbf{x}}_{t+1} - \mathbf{x}_{t+1}\|_2^2 + \|\hat{\mathbf{v}}_{t+1} - \mathbf{v}_{t+1}\|_2^2$$

---

## 4. Benchmark Specifications (BM-1 to BM-7)

| Benchmark ID | Scientific Phenomenon | Perturbation Protocol | Success Metric & Threshold |
|---|---|---|---|
| **BM-1** | Zero-Shot Transfer | Transfer from World A ($\mu=0.88$) to Alien Nebula B ($\mu=0.65$, novel silhouettes) with zero memory reset. | Transfer Adaptation Gain $> 50\%$; Re-settled Error $< 0.15$. |
| **BM-2** | Blind Goal Navigation | Impenetrable central barrier placed between start $(80, 440)$ and goal $(720, 80)$. Zero map provided. | Goal attained via autonomous detours in $\le 35$ steps without collision trapping. |
| **BM-3** | Silent Concept Drift | Unannounced friction shift $\mu: 0.88 \to 0.35$ (viscous mud) at $t = 80$. | Shock spike $> 3\times$ pre-drift baseline; online recalibration error $< 0.20$ within 40 steps. |
| **BM-4** | Epistemic Active Inference | 3 high-uncertainty entities ($\sigma_0^2 = 20.0$). Compare random vs. info-gain probes. | Total Bounded Information Gain $\ge 1.5$ nats; all final entity variances $\sigma_i^2 < 10.0$. |
| **BM-5** | Counterfactual Causal Repair | Query unexecuted prediction $\hat{\Delta x}_1(F) \to$ Intervene $\to$ Silent drift $\to$ Detect mismatch $\to$ Repair model $\to$ Query $\hat{\Delta x}_2(F)$. | Post-repair counterfactual error $\epsilon_2 < 0.15 \times \epsilon_{shock}$. |
| **BM-6** | Non-Privileged Composition | Novel entity combining orthogonal features (Heavy Mass + High Elasticity + Novel Polygon). Pre-touch prediction vs Categorical Baseline. | Compositional MSE $< 0.30 \times$ Categorical Nearest-Prototype MSE. |
| **BM-7** | Causal Vector Inversion | Actuator directional polarity inverted ($\mathbf{F} \to -\Delta \mathbf{x}$). | Pre-shock $\cos(\theta) > 0.98 \to$ Shock $\cos(\theta) \le -0.99 \to$ Post-repair $\cos(\theta) \ge 0.98$. |

---

## 5. Statistical Rigor: Multi-Seed & Bootstrap Protocol

To prevent distribution assumption artifacts on bounded metrics (success rates, cosines):
1. **Sample Size:** $N = 50$ deterministically generated seeds ($seed \in [1, 50]$).
2. **Parametric Reporting:** Sample Mean $\mu$, Sample Standard Deviation $\sigma$, and 95% Normal CI:
   $$CI_{norm} = \left[\mu - 1.96 \frac{\sigma}{\sqrt{N}}, \, \mu + 1.96 \frac{\sigma}{\sqrt{N}}\right]$$
3. **Non-Parametric Bootstrap Reporting ($B = 10,000$ iterations):**
   - For empirical success rates and bounded parameters, compute percentile bootstrap confidence intervals:
     $$CI_{boot} = \left[ \theta^*_{\alpha/2}, \, \theta^*_{1 - \alpha/2} \right] \quad \text{where } \alpha = 0.05$$
4. **Effect Size Attribution (Ablation Contrasts):**
   $$d = \frac{\mu_{Full} - \mu_{Ablated}}{\sigma_{pooled}}, \quad \sigma_{pooled} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

---

## 6. Codebase Freeze Declaration
As of protocol version 1.0.0, the core cognitive modules in `src/brain/` and benchmark specifications in `src/environment/` are declared **FROZEN**. All further runs must execute headlessly through deterministic harness scripts without ad-hoc parameter tuning.

---

## 7. Pre-Registered Falsification Protocol: Reusable Structure vs. Local Heuristics

### 7.1 Cross-World Trajectory Separation ($A \to B \to C$)
- **Condition $A \to A$:** Baseline familiar dynamics trajectory $E(t)$.
- **Condition $A \to B$:** Zero-shot novel dynamics ($\mu=0.71, g=4.2, \mathbf{W}_{act}=-\mathbf{I}$), zero retraining.
- **Condition $A \to C$:** Zero-shot novel dynamics ($\mu=0.12, g=15.7, \mathbf{W}_{act}=0.60\mathbf{I} \implies \text{effective simulator force multiplier } \alpha \mathbf{W}_{act} = 0.85 \times 0.60 = 0.51$), zero retraining.
- **Condition $A \to B \to B'$:** Limited online adaptation.
- **Key Metrics:**
  - Adaptation Latency: $T_\epsilon = \min \{ t : E(t) < 0.20 \}$
  - Adaptation Rate: $A_{\text{adapt}} = \frac{E(0) - E(T)}{B_{\text{interaction}}}$

### 7.2 Pre-Registered Nonlinear Hypothesis Discrimination
- **Environment Ground Truth:** Nonlinear Quadratic Drag $F(v) = k v^2$.
- **Competing Hypotheses:** $H_1: \hat{F} = k_1 v$ vs. $H_2: \hat{F} = k_2 v^2$.
- **Epistemic Selection:** Probing actions must target velocities maximizing discriminative variance $\Delta(v) = |k_1 v - k_2 v^2|$.
- **Bayes Factor Criterion:** Log-likelihood ratio $\ln(B_{21}) > 10.0$ required for structural model selection.

### 7.3 Continual Learning & Catastrophic Interference
- Tests whether adaptation to World B induces catastrophic destruction of World A latent representations:
  $$\mathcal{R} = 1.0 - \max\left(0, \frac{E_{A, 2} - E_{A, 1}}{E_{A, 1}}\right)$$
- Threshold: Knowledge retention $\mathcal{R} \ge 75\%$ required without explicit retraining.

---

## 8. Defensible Scientific Definition
> **Official Characterization:**  
> *"DWMA is an embodied developmental sensorimotor architecture that experimentally investigates predictive world modeling, active information acquisition, online structural adaptation, compositional generalization, and self-modeling without an LLM as its cognitive core."*
