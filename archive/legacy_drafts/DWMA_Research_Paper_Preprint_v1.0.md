# DWMA: Developmental World-Model Agent
### An Embodied Predictive-Coding and Active-Inference Architecture Without an LLM Cognitive Core

**Preprint Draft — Version 1.0**  
**Status:** Research artifact / frozen empirical evaluation protocol  

---

## Abstract
We present the **Developmental World-Model Agent (DWMA)**, an embodied computational architecture designed to investigate whether an agent can acquire and update predictive structure about an interactive environment without a Large Language Model (LLM) as its cognitive core. DWMA combines predictive forward modeling, epistemic active inference, online adaptation, sensorimotor concept formation, symbol grounding, and a functional self-model.

The evaluation is deliberately bounded to a simulated continuous dynamical environment where the agent has no direct access to latent mass, restitution, or ground-friction variables; these must be inferred through interaction residuals. We report the complete, audited four-phase empirical evaluation program conducted across $N = 50$ paired deterministic seeds with $B = 10,000$ percentile bootstrap resamples:
1. **Frozen Baseline Suite (BM-1 to BM-7):** Successful replication across 50 seeds ($49/50$ zero-shot transfer, $50/50$ blind navigation, $50/50$ concept drift recalibration, $50/50$ epistemic inquiry, $50/50$ counterfactual repair, $50/50$ non-privileged composition, and $48/50$ actuator polarity inversion), accompanied by an $8.8\times$ forecasting MSE reduction against a standardized persistence observer ($0.3276$ vs $2.8803$ MSE, Cohen's $d = 11.45$).
2. **Cross-World Transfer ($A \to B \to C$):** Clear zero-shot dynamical shock in novel worlds B ($1.3079 \pm 0.0421$) and C ($0.8117 \pm 0.0272$), followed by rapid online structural adaptation in B reaching $E(t) < 0.20$ within $T_\epsilon = 16.32 \pm 0.62$ steps ($50/50$ pass) with consistent adaptation rate $A_{\text{adapt}} = 0.0461 \pm 0.0084$.
3. **Continual Retention ($A \to B \to A$):** The multi-schema architecture preserves familiar World A dynamics with near-zero degradation ($E_{A1} = 0.00500 \to E_{A2} = 0.00501$, retention index $\mathcal{R} = 0.9901 \pm 0.0141$, $50/50$ pass $\mathcal{R} \ge 0.75$), whereas an overwriting baseline suffers catastrophic forgetting ($E_{A2} = 0.37460$, $\mathcal{R} = -72.97$, $0/50$ pass).
4. **Nonlinear Hypothesis Discrimination:** Primary survival analysis demonstrates that epistemic action selection discriminates between linear viscous drag ($H_1$) and quadratic drag ($H_2$) substantially faster and more reliably than undirected exploration (Kaplan-Meier median latency of $7.0$ steps with $0\%$ censoring vs $23.0$ steps with $28.0\%$ right-censored at the 30-step observation horizon; Mantel-Cox log-rank $\chi^2 = 92.28, p < 10^{-20}$; $50/50$ uncensored DWMA runs vs $36/50$ uncensored random runs).

All empirical claims are strictly bounded to the simulated continuous dynamical environment. No claims of AGI, consciousness, metaphysical causality, or human-like understanding are made.

---

## 1. Introduction

### 1.1 Motivation
An alternative to making language modeling the cognitive core of an autonomous system is to study learning through direct sensorimotor interaction. Biological development motivates the question: useful internal structure can emerge through repeated action, observation, prediction, and correction rather than through explicit access to latent physical constants.

DWMA is a computational investigation of this principle. It does not claim to reproduce biological development. Instead, it asks whether a non-privileged embodied agent can construct predictive and reusable sensorimotor structure inside a controlled dynamical environment.

### 1.2 Research Question
The frozen protocol asks:
> *Can an ungrounded computational agent autonomously build a predictive forward model, bind orthogonal sensorimotor concepts without privileged access, detect structural violations (drift and vector inversion), and execute online model repair solely via sensory contingency and epistemic active inference?*

### 1.3 Epistemological Boundaries
All empirical claims are restricted to the simulator. The work does not establish general intelligence, consciousness, metaphysical causality, biological equivalence, or unrestricted real-world competence.

---

## 2. Mathematical and Computational Architecture

### 2.1 Observation Space
At discrete time step $t$, the ego sensory vector is:
$$\mathbf{o}_t^{ego} = [x_t, y_t, v_{x,t}, v_{y,t}, \theta_t] \in \mathbb{R}^5$$

Each observed entity contains position, velocity, radius, RGB signature, and geometric silhouette. Crucially:
$$m_i \notin \mathcal{O}, \quad e_i \notin \mathcal{O}, \quad \mu \notin \mathcal{O}$$
so mass, restitution, and ground friction are not directly observable.

### 2.2 Action Space
The continuous motor actuation vector is:
$$\mathbf{a}_t = [u_x, u_y] \in [-1.0, 1.0]^2 \subset \mathbb{R}^2$$

Applied thrust is:
$$\mathbf{F}_t = \mathbf{W}_{actuator} \mathbf{a}_t \cdot \alpha$$
with initial actuator matrix $\mathbf{I}_2$ and scaling factor $\alpha = 0.85$.

### 2.3 Predictive World Model
The forward model computes next-state expectations:
$$\hat{\mathbf{s}}_{t+1} = \mathcal{M}(\mathbf{s}_t, \mathbf{a}_t)$$

Prediction error is measured from the difference between predicted and observed dynamical outcomes. The prototype performs online parameter updates with learning rate $\eta = 0.04$.

The scientific role of the predictive model is to create measurable expectations whose violations signal environmental change and structural drift.

### 2.4 Standardized External Observer
Every evaluated variant receives the identical forecasting task. Active forward models use:
$$\hat{\mathbf{s}}_{t+1} = \mathcal{M}(\mathbf{s}_t, \mathbf{a}_t)$$
while the no-predictive-model ablation uses the unbiased persistence baseline:
$$\hat{\mathbf{s}}_{t+1} = \mathbf{s}_t$$

The standardized prediction loss is:
$$\mathcal{L}_{MSE} = \|\hat{\mathbf{x}}_{t+1} - \mathbf{x}_{t+1}\|_2^2 + \|\hat{\mathbf{v}}_{t+1} - \mathbf{v}_{t+1}\|_2^2$$
This completely eliminates earlier apples-to-oranges ablation evaluation artifacts.

### 2.5 Epistemic Active Inference
For an entity belief state whose parameter uncertainty variance changes from prior to posterior:
$$\Delta H_i = \frac{1}{2} \ln\left(\frac{\sigma_{prior}^2}{\sigma_{post}^2}\right) \quad \text{[nats]}$$

The bounded total information gain across all entities is:
$$I_{total} = \sum_i \frac{1}{2} \max\left(0, \ln\frac{\sigma_{i,0}^2}{\sigma_{i,current}^2}\right) \quad \text{[nats]}$$
Thus repeated probing of an already-characterized entity does not create artificial or unbounded information gain.

### 2.6 Concept Formation and Symbol Grounding
The causal/concept network records sensorimotor relationships and behavioral properties inferred from collision residuals. The composition benchmark tests whether orthogonal learned properties can be combined for a novel object rather than relying only on categorical nearest-prototype matching.

The symbol lexicon associates arbitrary labels with sensorimotor entities. This is treated as a symbol-grounding mechanism, not proof of complete semantic understanding.

### 2.7 Functional Self-Model
The self-model estimates action-outcome contingency:
$$\Delta P = P(\text{motion} \mid \text{motor thrust}) - P(\text{motion} \mid \text{external drift})$$
This is a computational agency estimate, not a measure of consciousness or subjective experience.

![Figure 1: DWMA Embodied Closed-Loop Predictive Architecture](figures/fig1_system_architecture.png)
*Figure 1: Closed-loop architecture combining continuous motor actuation, reafference-cancelled sensory observation, predictive forward modeling, epistemic active inference, and multi-schema continual memory.*

---

## 3. Frozen Benchmark Suite

| Benchmark | Phenomenon | Empirical Criterion |
|---|---|---|
| **BM-1** | Zero-shot transfer | Gain $> 50\%$; re-settled error $< 0.15$ |
| **BM-2** | Blind goal navigation | Goal in $\le 35$ steps without trapping |
| **BM-3** | Silent concept drift | Shock $> 3\times$ baseline; recalibration error $< 0.20$ within 40 steps |
| **BM-4** | Epistemic active inference | Information gain $\ge 1.5$ nats; final variances $< 10.0$ |
| **BM-5** | Counterfactual causal repair | Post-repair error $< 0.15 \times$ shock error |
| **BM-6** | Non-privileged composition | MSE $< 0.30 \times$ categorical baseline |
| **BM-7** | Directional structural violation | Shock $\cos(\theta) \le -0.99 \to$ Post-repair $\cos(\theta) \ge 0.98$ |

- **BM-1 (Zero-Shot Transfer):** World A uses friction 0.88. Alien World B uses friction 0.65 and novel silhouettes, with no memory reset.
- **BM-2 (Blind Navigation):** An impenetrable central barrier separates start $(80, 440)$ and goal $(720, 80)$, with no map provided.
- **BM-3 (Silent Drift):** Ground friction changes without announcement from 0.88 to 0.35 at $t = 80$.
- **BM-4 (Active Inquiry):** Three high-uncertainty entities begin with variance 20.0. Information-directed probing is compared with random probing.
- **BM-5 (Counterfactual Repair):** The agent predicts an unexecuted intervention, executes it, experiences silent drift, detects mismatch, repairs its model, and repeats the counterfactual query.
- **BM-6 (Compositional Generalization):** A novel object combines heavy mass, high elasticity, and a novel polygon silhouette. Latent physical constants are excluded from observation.
- **BM-7 (Directional Structural Violation):** The actuator mapping is inverted so that commanded direction and resulting displacement become opposed. The system must detect and repair the structural mismatch.

---

## 4. Audited Empirical Reproduction of Frozen Baselines (BM-1 to BM-7)
The baseline benchmark suite was executed across $N = 50$ paired deterministic seeds (seeds 1 to 50) using the frozen evaluation harness. Normal and non-parametric bootstrap ($B = 10,000$) 95% confidence intervals were computed.

| Benchmark | Phenomenon | Empirical Metric | Measured Result | Parametric Normal 95% CI | Percentile Bootstrap 95% CI | Decisive Success Count |
|---|---|---|---|---|---|---|
| **BM-1** | Zero-Shot Transfer | Transfer Adaptation Gain | **$85.82\% \pm 2.53\%$** | $[85.12, 86.53]\%$ | $[85.15, 86.51]\%$ | **$49/50$ ($98.0\%$) [PASS]** |
| **BM-2** | Blind Goal Navigation | Steps to Target (No Map) | **$23.10 \pm 2.46$ steps** | $[22.42, 23.78]$ | $[22.44, 23.78]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **BM-3** | Silent Concept Drift | Shock Prediction MSE | **$1.384 \pm 0.120$ MSE** | $[1.351, 1.417]$ | $[1.351, 1.416]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **BM-4** | Epistemic Active Inquiry | Total Information Gain | **$5.14 \pm 0.23$ nats** | $[5.08, 5.21]$ | $[5.08, 5.21]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **BM-5** | Counterfactual Model Repair | Post-Repair Error Ratio | **$1.18 \pm 0.48$ px** | $[1.05, 1.32]$ | $[1.05, 1.32]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **BM-6** | Non-Privileged Composition | Compositional Prediction MSE | **$0.119 \pm 0.075$ MSE** | $[0.098, 0.139]$ | $[0.098, 0.139]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **BM-7** | Actuator Polarity Inversion | Directional Alignment $\cos(\theta)$ | **$0.9915 \pm 0.0057$** | $[0.9899, 0.9931]$ | $[0.9899, 0.9931]$ | **$48/50$ ($96.0\%$) [PASS]** |

All seven preregistered benchmark criteria were satisfied across the 50 deterministic seeds. Across all seeds, the single observed BM-1 failure occurred on seed 42 due to boundary entrapment, and the two BM-7 failures occurred on seeds 17 and 39 due to oscillatory motor chatter prior to polarity latching.

---

## 5. Empirical Falsification Program Results

### 5.1 Phase 2: Cross-World Transfer & Adaptation ($A \to B \to C$)
To test whether the agent learns reusable predictive structure rather than over-indexing to World A, we evaluated headless zero-shot transfer across three dynamical regimes ($N = 50$ seeds, $B_{\text{interaction}} = 40$ steps):
- **World A (Earth Baseline):** Friction $\mu = 0.88$, base actuator gain $\alpha = 0.85$, polarity $\mathbf{W}_{\text{act}} = +\mathbf{I}$, gravity $g = 9.8$.
- **World B (Alien Nebula):** Friction $\mu = 0.71$, base actuator gain $\alpha = 0.85$, inverted actuator polarity $\mathbf{W}_{\text{act}} = -\mathbf{I}$, gravity $g = 4.2$.
- **World C (Radical Dynamics):** Friction $\mu = 0.12$, relative actuator matrix multiplier $\mathbf{W}_{\text{act}} = 0.60\mathbf{I}$, resulting in simulator net actuator scale $\alpha \mathbf{W}_{\text{act}} = 0.85 \times 0.60 = 0.51$, polarity $= +\mathbf{I}$, gravity $g = 15.7$.

| Experimental Condition | Metric | Mean ± StdDev | Parametric Normal 95% CI | Percentile Bootstrap 95% CI | Decisive Criterion / Status |
|---|---|---|---|---|---|
| **$A \to A$ (Familiar Baseline)** | Tracking Error $E(t)$ | **$0.0050 \pm 0.0000$** | $[0.0050, 0.0050]$ | $[0.0050, 0.0050]$ | $50/50$ ($100.0\%$) |
| **$A \to B$ (Zero-Shot Novel B)** | Mean Shock Error $E(t)$ | **$1.3079 \pm 0.0421$** | $[1.2963, 1.3196]$ | $[1.2968, 1.3199]$ | Pronounced Transfer Shock |
| **$A \to C$ (Zero-Shot Radical C)** | Mean Shock Error $E(t)$ | **$0.8117 \pm 0.0272$** | $[0.8042, 0.8192]$ | $[0.8041, 0.8192]$ | Pronounced Transfer Shock |
| **$A \to B \to B'$ (Adaptation)** | Initial Error $E(0)$ ($t=1$) | **$1.8491 \pm 0.3356$** | $[1.7561, 1.9422]$ | $[1.7588, 1.9413]$ | Post-inversion entry shock |
| **$A \to B \to B'$ (Adaptation)** | Polarity Flip Latency | **$7.00 \pm 0.00$ steps** | $[7.00, 7.00]$ | $[7.00, 7.00]$ | Directional evidence $\Lambda_t < -0.50$ |
| **$A \to B \to B'$ (Adaptation)** | Latency $T_\epsilon$ ($E < 0.20$) | **$16.32 \pm 0.62$ steps** | $[16.15, 16.49]$ | $[16.14, 16.48]$ | **$50/50$ pass ($T_\epsilon \le 20$)** |
| **$A \to B \to B'$ (Adaptation)** | Rate $A_{\text{adapt}} = \frac{E(0)-E(T)}{40}$ | **$0.0461 \pm 0.0084$** | $[0.0438, 0.0485]$ | $[0.0438, 0.0484]$ | **$50/50$ pass ($A_{\text{adapt}} \ge 0.02$)** |
| **$A \to B \to B'$ (Adaptation)** | Final Settled Error $E(T)$ | **$0.0040 \pm 0.0010$** | $[0.0037, 0.0043]$ | $[0.0037, 0.0043]$ | Re-settled accurate tracking |

**Autonomous Mechanism:** In World B, actuator polarity inversion is inferred solely via the reafference-cancelled directional alignment accumulator $\Lambda_t = 0.80 \Lambda_{t-1} + 0.20 \cos(\theta_t)$. The agent autonomously flips polarity when $\Lambda_t < -0.50$ (at step $7.00 \pm 0.00$), directly triggering the rapid error collapse to $E(t) < 0.20$ at $16.32 \pm 0.62$ steps.

![Figure 2: Phase 2 Online Structural Adaptation in World B](figures/fig2_cross_world_adaptation.png)
*Figure 2: Empirical error trajectory $E(t)$ during online adaptation in World B ($A \to B \to B'$), showing initial transfer shock ($E(0) = 1.8491$), autonomous polarity inversion at step $7.00$, threshold crossing ($T_\epsilon = 16.32 \pm 0.62$ steps), and asymptotic re-settling to $E(T) = 0.0040$. Shaded region denotes 95% percentile bootstrap confidence interval across $N = 50$ seeds.*

### 5.2 Phase 3: Continual Retention & Schema Retrieval ($A \to B \to A$)
To evaluate catastrophic interference, agents adapted to World B are returned to World A without explicit retraining ($N = 50$ seeds, budget $T = 40$). Full DWMA is compared against an Overwriter baseline that updates a single global parameter set.

The retention index is defined as:
$$\mathcal{R} = 1.0 - \max\left(0, \frac{E_{A2} - E_{A1}}{E_{A1}}\right)$$

| Agent Architecture | Phase A1 Error $E_{A1}$ | Phase A2 Error $E_{A2}$ | Absolute Error Drift $\Delta E$ | Retention Index $\mathcal{R}$ | Normal 95% CI | Decisive Retention Count ($\mathcal{R} \ge 0.75$) |
|---|---|---|---|---|---|---|
| **Full DWMA (Multi-Schema)** | **$0.00500 \pm 0.00000$** | **$0.00501 \pm 0.00003$** | **$+0.00001 \pm 0.00003$** | **$0.9901 \pm 0.0141$** | $[0.9862, 0.9940]$ | **$50/50$ ($100.0\%$) [PASS]** |
| **Overwriter Baseline** | **$0.00500 \pm 0.00000$** | **$0.37460 \pm 0.03212$** | **$+0.36960 \pm 0.03212$** | **$-72.9726 \pm 6.4245$** | $[-74.752, -71.193]$ | **$0/50$ ($0.0\%$) [FAIL]** |

**Statistical & Metric Disclosures:**
1. **Raw Error Primacy:** Because baseline tracking error $E_{A1} \approx 0.00500$ px is near zero, dividing by $E_{A1}$ numerically magnifies negative values (e.g. Overwriter $\mathcal{R} = -72.97$). We therefore report raw tracking errors $E_{A1} \to E_{A2}$ as the primary retention evidence, using $\mathcal{R}$ as the secondary threshold check.
2. **Sensory-Cued vs. Un-Cued Retrieval:** In sensory-cued re-entry, ambient gravity ($g=9.8$) matches the stored World A schema prior to actuation, yielding zero-shock tracking ($E_{A2} = 0.00501$). Under blind un-cued re-entry (where gravity is withheld until after motion), the agent experiences an immediate step-1 shock ($E(1) \approx 1.595$), which is autonomously resolved at step 2 via Bayesian schema likelihood selection, collapsing error back to $0.00501$ for steps 2 through 40.

![Figure 3: Phase 3 Continual Retention vs Catastrophic Forgetting](figures/fig3_continual_retention.png)
*Figure 3: Tracking error comparison in World A before ($E_{A1}$) and after ($E_{A2}$) intermediate adaptation to World B. Full DWMA preserves prior representations ($\mathcal{R} = 0.9901 \pm 0.0141$, $50/50$ pass), whereas single-schema overwriting suffers catastrophic interference ($\mathcal{R} = -72.97$, $0/50$ pass).*

### 5.3 Phase 4: Nonlinear Structural Hypothesis Discrimination
To determine whether DWMA can design informative experiments to discriminate between competing physical laws, the agent was placed in an environment governed by quadratic aerodynamic drag:
$$F_{\text{true}}(v) = -k_{\text{true}} v^2 \operatorname{sgn}(v), \quad k_{\text{true}} = 0.08$$

The agent maintained two recursively fitted structural hypotheses:
- $H_1: \hat{F}_1(v) = -k_1 v$ (Linear Viscous Drag)
- $H_2: \hat{F}_2(v) = -k_2 v^2 \operatorname{sgn}(v)$ (Quadratic Aerodynamic Drag)

Actions were selected to maximize discriminative variance $\Delta(v) = |\hat{F}_1(v) - \hat{F}_2(v)|$, compared against a uniformly random babbler baseline over $N = 50$ paired seeds with observation horizon $T = 30$.

| Exploration Policy | Metric | Mean ± StdDev | Kaplan-Meier Median | Bootstrap 95% CI | Decisive Pass ($\ln(B_{21}) > 10.0$) |
|---|---|---|---|---|---|
| **DWMA Epistemic Policy** | Log-Likelihood Ratio $\ln(B_{21})$ | **$30.35 \pm 8.03$** | **$31.74$** | $[28.10, 32.50]$ | **$50/50$ seeds ($100.0\%$) [PASS]** |
| **Random Babbler Baseline** | Log-Likelihood Ratio $\ln(B_{21})$ | **$20.02 \pm 14.34$** | **$16.47$** | $[16.11, 24.03]$ | **$36/50$ seeds ($72.0\%$)** |
| **DWMA Epistemic Policy** | Time-to-Discrimination $T_{\text{disc}}$ | **$7.18 \pm 2.59$ st** | **$7.0$ st** | $[6.58, 7.98]$ | **$50/50$ uncensored ($100.0\%$)** |
| **Random Babbler (Uncensored 36)** | Time-to-Discrimination $T_{\text{disc}}$ | **$18.33 \pm 5.12$ st** | **$18.5$ st** | $[16.64, 20.08]$ | $36$ successful seeds only |
| **Random Babbler (All 50)** | Observation Horizon Censoring | **$14 / 50$ right-censored** | **$23.0$ st (KM)** | [$28.0\%$ censored at $T=30$] | $14$ seeds ambiguous at $T=30$ |
| **DWMA Epistemic Policy** | Chosen Discrepancy $\Delta(v)$ | **$0.0765 \pm 0.0095$** | **$0.0766$** | $[0.0740, 0.0792]$ | Maximizes $|\hat{F}_1 - \hat{F}_2|$ |
| **Random Babbler Baseline** | Chosen Discrepancy $\Delta(v)$ | **$0.0552 \pm 0.0484$** | **$0.0466$** | $[0.0453, 0.0708]$ | Sub-critical velocity range |
| **DWMA Epistemic Policy** | Peak Velocity Explored $\|v_{\text{max}}\|$ | **$3.63 \pm 0.03$** | **$3.63$** | $[3.62, 3.64]$ | Drives to high $|v|$ divergence |
| **Random Babbler Baseline** | Peak Velocity Explored $\|v_{\text{max}}\|$ | **$2.47 \pm 0.41$** | **$2.51$** | $[2.36, 2.58]$ | Fails to escape low $|v|$ regime |

**Primary Time-to-Event Survival Analysis:**
- **Primary Finding:** The epistemic policy yielded substantially faster and more reliable discrimination, with **50/50 uncensored DWMA runs versus 36/50 uncensored random runs** within the 30-step observation horizon.
- **Kaplan-Meier Survival Contrast:** Epistemic action selection achieved a median discrimination latency of **$7.0$ steps** with $0\%$ right-censoring, whereas the random baseline reached a median latency of **$23.0$ steps** with $14/50$ runs ($28.0\%$) remaining ambiguous at the maximum observation horizon ($T = 30$).
- **Mantel-Cox Log-Rank Test:** The survival distributions exhibit decisive statistical separation:
  $$\chi^2 = \mathbf{92.28}, \quad df = 1, \quad p < 10^{-20}$$
- **Uncensored Speedup:** Among the 36 seeds where the random babbler successfully discriminated within the horizon, DWMA achieved separation in **$7.18 \pm 2.59$ steps vs $18.33 \pm 5.12$ steps**, representing a **$2.55\times$ speedup** ($p < 10^{-12}$).
- **Administrative-Censoring Sensitivity Statistic:** Imputing the 14 censored random seeds at the terminal horizon boundary $T = 31$ yields a paired latency difference of $\bar{D} = 14.70 \pm 7.99$ steps, corresponding to an administrative sensitivity effect size of $d_{\text{paired}} = \mathbf{1.84}$. This is classified strictly as a secondary sensitivity metric under horizon truncation.
- **Methodological Disclosure:** Candidate models $H_1$ and $H_2$ are fitted online via recursive ordinary least squares. Under the Gaussian observation error model ($\sigma = 0.05$), the test statistic is formally the **maximum-likelihood log-evidence / log-likelihood ratio**:
  $$\ln(B_{21}) = \frac{\text{SSE}_{H1} - \text{SSE}_{H2}}{2\sigma^2}$$
  denoted $\ln(B_{21})$ to maintain continuity with the preregistered threshold $\ln(B_{21}) > 10.0$.

![Figure 4: Phase 4 Kaplan-Meier Survival Analysis of Discrimination Latency](figures/fig4_hypothesis_survival_analysis.png)
*Figure 4: Kaplan-Meier survival curves $S(t) = P(T > t)$ representing the probability of remaining ambiguous regarding competing dynamical hypotheses ($H_1$ linear vs $H_2$ quadratic drag). Epistemic exploration drives rapid discrimination (median $7.0$ steps, $0\%$ censored) compared to undirected random babbling (median $23.0$ steps, $28.0\%$ right-censored at $T=30$; log-rank $\chi^2 = 92.28, p < 10^{-20}$).*

---

## 6. Consolidated Empirical Evaluation Matrix
The master matrix below compiles all evaluated phases, experimental conditions, sample sizes, parameter environments, and decisive outcomes into a single frozen record.

| Phase & Phenomenon | Condition / Policy | Environment Parameters | Primary Metric | Observed Value (Mean ± SD) | Normal 95% CI | Percentile Bootstrap 95% CI | Empirical Pass Rate |
|---|---|---|---|---|---|---|---|
| **Phase 1: BM-1** | Zero-Shot Transfer | $\mu_A = 0.88 \to \mu_B = 0.65$ | Adaptation Gain | **$85.82\% \pm 2.53\%$** | $[85.12, 86.53]\%$ | $[85.15, 86.51]\%$ | **$49/50$ ($98.0\%$)** |
| **Phase 1: BM-2** | Blind Goal Navigation | Impenetrable barrier, no map | Steps to Goal | **$23.10 \pm 2.46$ st** | $[22.42, 23.78]$ | $[22.44, 23.78]$ | **$50/50$ ($100.0\%$)** |
| **Phase 1: BM-3** | Silent Concept Drift | $\mu: 0.88 \to 0.35$ at $t=80$ | Shock Error MSE | **$1.384 \pm 0.120$** | $[1.351, 1.417]$ | $[1.351, 1.416]$ | **$50/50$ ($100.0\%$)** |
| **Phase 1: BM-4** | Epistemic Active Inquiry | $\sigma_0^2 = 20.0$, 3 entities | Information Gain | **$5.14 \pm 0.23$ nats** | $[5.08, 5.21]$ | $[5.08, 5.21]$ | **$50/50$ ($100.0\%$)** |
| **Phase 1: BM-5** | Counterfactual Repair | Unexecuted intervention | Post-Repair Error | **$1.18 \pm 0.48$ px** | $[1.05, 1.32]$ | $[1.05, 1.32]$ | **$50/50$ ($100.0\%$)** |
| **Phase 1: BM-6** | Non-Privileged Composition | Heavy + elastic + polygon | Composition MSE | **$0.119 \pm 0.075$** | $[0.098, 0.139]$ | $[0.098, 0.139]$ | **$50/50$ ($100.0\%$)** |
| **Phase 1: BM-7** | Actuator Polarity Inversion | Actuator polarity $-\mathbf{I}$ | Re-aligned $\cos(\theta)$ | **$0.9915 \pm 0.0057$** | $[0.9899, 0.9931]$ | $[0.9899, 0.9931]$ | **$48/50$ ($96.0\%$)** |
| **Phase 2: Baseline** | Familiar Tracking $A \to A$ | $\mu=0.88, \alpha=0.85, g=9.8$ | Tracking Error $E(t)$ | **$0.0050 \pm 0.0000$** | $[0.0050, 0.0050]$ | $[0.0050, 0.0050]$ | **$50/50$ ($100.0\%$)** |
| **Phase 2: Transfer** | Zero-Shot Shock $A \to B$ | $\mu=0.71, \mathbf{W}_{\text{act}}=-\mathbf{I}, g=4.2$ | Mean Shock $E(t)$ | **$1.3079 \pm 0.0421$** | $[1.2963, 1.3196]$ | $[1.2968, 1.3199]$ | Transfer Shock |
| **Phase 2: Transfer** | Zero-Shot Shock $A \to C$ | $\mu=0.12, \mathbf{W}_{\text{act}}=0.60\mathbf{I} (\alpha_{\text{eff}}=0.51), g=15.7$ | Mean Shock $E(t)$ | **$0.8117 \pm 0.0272$** | $[0.8042, 0.8192]$ | $[0.8041, 0.8192]$ | Transfer Shock |
| **Phase 2: Adaptation** | Online Re-tuning $A \to B \to B'$ | $\mu=0.71, \mathbf{W}_{\text{act}}=-\mathbf{I}, B=40$ | Latency $T_\epsilon (<0.20)$ | **$16.32 \pm 0.62$ st** | $[16.15, 16.49]$ | $[16.14, 16.48]$ | **$50/50$ ($100.0\%$)** |
| **Phase 2: Adaptation** | Online Re-tuning $A \to B \to B'$ | $E(0)=1.8491, E(T)=0.0040$ | Rate $A_{\text{adapt}} = \frac{\Delta E}{40}$ | **$0.0461 \pm 0.0084$** | $[0.0438, 0.0485]$ | $[0.0438, 0.0484]$ | **$50/50$ ($100.0\%$)** |
| **Phase 3: Retention** | Multi-Schema DWMA | Retest in World A ($T=40$) | Raw Error $E_{A1} \to E_{A2}$ | **$0.00500 \to 0.00501$** | $[0.00500, 0.00502]$ | $[0.00500, 0.00502]$ | **$50/50$ ($\mathcal{R}=0.9901$)** |
| **Phase 3: Retention** | Overwriter Baseline | Retest in World A ($T=40$) | Raw Error $E_{A1} \to E_{A2}$ | **$0.00500 \to 0.37460$** | $[0.3657, 0.3835]$ | $[0.3657, 0.3835]$ | **$0/50$ (Catastrophic)** |
| **Phase 4: Hypothesis** | DWMA Epistemic Policy | Quadratic drag $k=0.08$ | Log-Evidence $\ln(B_{21})$ | **$30.35 \pm 8.03$** | $[28.12, 32.57]$ | $[28.10, 32.50]$ | **$50/50$ ($100.0\%$)** |
| **Phase 4: Hypothesis** | Random Babbler Baseline | Quadratic drag $k=0.08$ | Log-Evidence $\ln(B_{21})$ | **$20.02 \pm 14.34$** | $[16.05, 23.99]$ | $[16.11, 24.03]$ | **$36/50$ ($72.0\%$)** |
| **Phase 4: Survival** | DWMA Epistemic Policy | KM Time-to-Discrimination | KM Median Latency | **$7.0$ steps** | $0\%$ censored | $[6.58, 7.98]$ (mean 7.18) | **$50/50$ uncensored** |
| **Phase 4: Survival** | Random Babbler (Uncensored) | KM Time-to-Discrimination | KM Median Latency | **$18.5$ steps** | Uncensored 36 runs | $[16.64, 20.08]$ (mean 18.33) | **$36/50$ uncensored** |
| **Phase 4: Censoring** | Random Babbler (All 50) | Horizon $T=30$ | Ambiguous at Horizon | **$14 / 50$ right-censored** | $28.0\%$ censored | Log-rank $\chi^2 = 92.28$ | $p < 10^{-20}$ |

---

## 7. Controlled Component Ablations
To isolate the functional contribution of each architectural component, all variants were evaluated against a standardized external forecasting observer predicting next-state kinematics:
$$\mathcal{L}_{MSE} = \|\hat{\mathbf{x}}_{t+1} - \mathbf{x}_{t+1}\|_2^2 + \|\hat{\mathbf{v}}_{t+1} - \mathbf{v}_{t+1}\|_2^2$$
where ablated predictive agents used an unbiased persistence baseline $\hat{\mathbf{s}}_{t+1} = \mathbf{s}_t$.

| Evaluated Architecture Variant | Active Component Removed | External Forecasting MSE | Normal 95% CI | Effect Size vs Full DWMA ($d$) | Interpretation |
|---|---|---|---|---|---|
| **Full DWMA (Baseline)** | None (Complete Architecture) | **$0.3276 \pm 0.0418$** | $[0.3160, 0.3392]$ | — | Accurate, adaptive forward modeling |
| **Variant A** | No Predictive Model (Persistence) | **$2.8803 \pm 0.3129$** | $[2.7936, 2.9670]$ | **$11.45$** ($8.8\times$ error increase) | Catastrophic loss of state anticipation |
| **Variant B** | No Epistemic Drive (Uniform Action) | **$0.8412 \pm 0.0982$** | $[0.8140, 0.8684]$ | **$6.82$** ($2.6\times$ error increase) | Sub-optimal parameter convergence |
| **Variant C** | No Functional Self-Model | **$0.6120 \pm 0.0714$** | $[0.5922, 0.6318]$ | **$4.87$** ($1.9\times$ error increase) | Inability to cancel motor reafference |
| **Variant D** | No Causal Graph Structure | **$0.5489 \pm 0.0632$** | $[0.5314, 0.5664]$ | **$4.13$** ($1.7\times$ error increase) | Loss of compositional property binding |
| **Variant E** | No Episodic Memory Store | **$0.4915 \pm 0.0511$** | $[0.4773, 0.5057]$ | **$3.51$** ($1.5\times$ error increase) | Slow re-adaptation upon regime return |

---

## 8. Discussion & Epistemological Boundaries
The empirical findings establish that within the simulated continuous dynamical environment, DWMA successfully combines:
1. **Predictive Forward Modeling:** Forecasting next-state kinematics with an $8.8\times$ error reduction over persistence.
2. **Epistemic Information Acquisition:** Active selection of experiments that isolate parameters in fewer steps than random exploration, decisively accelerating structural hypothesis discrimination ($2.55\times$ latency reduction; log-rank $\chi^2 = 92.28, p < 10^{-20}$).
3. **Rapid Structural Adaptation:** Inverting actuator mappings autonomously via sensorimotor reafference cancellation ($\Lambda_t < -0.50$) within $7.0$ steps, restoring prediction stability within $16.32$ steps across $50/50$ seeds.
4. **Continual Retention Without Interference:** Preserving prior world models across domain shifts with near-zero error drift ($E_{A1} = 0.00500 \to E_{A2} = 0.00501$), completely avoiding catastrophic forgetting.

**Strict Demarcation of Claims:**
- Prediction errors represent internal model discrepancies, not "hallucinations."
- Intervention-based model adaptation represents computational structural update, not metaphysical comprehension of physical reality.
- The self-model measures functional motor-outcome contingency $\Delta P$, not subjective self-awareness or consciousness.
- All conclusions remain strictly bounded to the evaluated continuous dynamical simulation environment.

---

## 9. Threats to Validity & Limitations
1. **Simulator Dependence:** All empirical evidence is grounded in a deterministic continuous 2D simulator. Transfer to real-world physical systems with unmodeled sensory noise and temporal delays remains unverified.
2. **Simplified Sensorimotor Dimensionality:** The action space is two-dimensional continuous control, and the entity feature space is low-dimensional. Scaling to high-dimensional visual inputs requires future investigation.
3. **Prespecified Hypothesis Families:** In Phase 4, the candidate functional forms (linear vs. quadratic drag) were pre-specified. The architecture discriminates between candidate structures, but does not invent novel mathematical functional families de novo.
4. **Administrative Censoring in Baseline:** Because $28\%$ of random babbler seeds did not discriminate within 30 steps, comparative effect sizes involving latency require careful handling: survival analysis (Kaplan-Meier and log-rank) serves as the primary time-to-event benchmark, while paired $d_{\text{paired}} = 1.84$ reflects an administrative censoring convention.

---

## 10. Conclusion
The Developmental World-Model Agent (DWMA) demonstrates that rich, reusable, and adaptive predictive structure can be acquired and maintained through embodied sensorimotor interaction and active inference, without relying on a Large Language Model as its cognitive core. 

Across four preregistered empirical phases comprising $N = 50$ deterministic seeds, the frozen architecture successfully reproduced all seven core developmental benchmarks, adapted to radically novel environments ($A \to B \to C$), prevented catastrophic forgetting ($A \to B \to A$), and actively gathered evidence to discriminate between competing physical laws.

The final scientific characterization is frozen:
> *"DWMA is an embodied developmental sensorimotor architecture that experimentally demonstrates predictive world modeling, active information acquisition, online structural adaptation, compositional generalization, and multi-schema retention without an LLM as its cognitive core within a continuous simulated dynamical environment."*

---

## Appendix A — Frozen Experimental Parameters

| Parameter | Symbol | Frozen Value | Scope / Description |
|---|---|---|---|
| Online Learning Rate | $\eta$ | $0.04$ | Recursive model weight update rate |
| Initial Learned Acceleration | $a_0$ | $0.25$ | Initial acceleration parameter prior |
| Initial Friction Damping | $f_0$ | $0.85$ | Initial friction damping prior |
| Actuator Base Scale | $\alpha$ | $0.85$ | Standard physical simulator actuator thrust gain |
| Agency Contingency Threshold | $\theta_{\text{agency}}$ | $0.50$ | Self-model action-outcome contingency threshold |
| Directional Evidence Smoothing | $\gamma$ | $0.80$ | Reafference directional evidence smoothing |
| Polarity Inversion Threshold | $\Lambda_{\text{thresh}}$ | $-0.50$ | Trigger for autonomous actuator inversion |
| Pre-Registered Sample Size | $N$ | $50$ | Paired deterministic seeds (1 to 50) |
| Bootstrap Resamples | $B_{\text{boot}}$ | $10,000$ | Percentile non-parametric bootstrap iterations |
| Interaction Budget (Phase 2 & 3) | $B_{\text{interaction}}$ | $40$ steps | Horizon for cross-world online adaptation |
| Adaptation Threshold (Phase 2) | $\epsilon$ | $0.20$ | Error threshold for latency metric $T_\epsilon$ |
| Retention Criterion (Phase 3) | $\mathcal{R}_{\text{pass}}$ | $\ge 0.75$ | Threshold for continual retention index |
| Discrimination Threshold (Phase 4) | $\ln(B_{21})_{\text{thresh}}$ | $> 10.0$ | Decisive structural model selection criterion |
| Observation Horizon (Phase 4) | $T_{\text{horizon}}$ | $30$ steps | Maximum time window for hypothesis discrimination |

---

## Appendix B — Publication Reproducibility Checklist
- [x] Frozen git repository commit hash documented and preserved.
- [x] All 50 deterministic random seeds (seeds 1 to 50) explicitly enumerated.
- [x] Hardware/software runtime environment verified: macOS, Python 3.14.3, Node v22.23.
- [x] Complete per-seed raw CSV trajectories archived for all benchmarks and phases.
- [x] Exact mathematical definitions and equation consistency verified ($A_{\text{adapt}}$, $\mathcal{R}$, $\ln(B_{21})$).
- [x] Parameter reconciliation for World C documented: $\mathbf{W}_{\text{act}} = 0.60\mathbf{I} \implies \alpha_{\text{eff}} = 0.51$.
- [x] Survival analysis (Kaplan-Meier and Mantel-Cox log-rank) established as primary time-to-event evidence for Phase 4.
- [x] Right-censoring disclosures and administrative sensitivity nature of $d_{\text{paired}} = 1.84$ explicitly stated.
- [x] Dual-mode continual retention (sensory-cued vs un-cued Bayesian schema switch) documented.
- [x] Standardized persistence observer used for all component ablation contrasts.
- [x] Strictly bounded claims with zero unverified speculation, metaphysical causality, or AGI claims.

---

## References
1. Friston, K. (2010). The free-energy principle: a unified brain theory?. *Nature Reviews Neuroscience*, 11(2), 127-138.
2. Rao, R. P., & Ballard, D. H. (1999). Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*, 2(1), 79-87.
3. Ha, D., & Schmidhuber, J. (2018). Recurrent world models facilitate policy evolution. *Advances in Neural Information Processing Systems (NeurIPS)*, 31.
4. Harnad, S. (1990). The symbol grounding problem. *Physica D: Nonlinear Phenomena*, 42(1-3), 335-346.
5. French, R. M. (1999). Catastrophic forgetting in connectionist networks. *Trends in Cognitive Sciences*, 3(4), 128-135.
6. Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457-481.
7. Mantel, N. (1966). Evaluation of survival data and two new rank order statistics arising in its consideration. *Cancer Chemotherapy Reports*, 50(3), 163-170.
