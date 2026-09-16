# Cross-World A -> B -> C Empirical Report (Audited)

**Status:** Peer-Review Grade Pre-Registered Evaluation (Frozen Protocol v1.0)  
**Sample Size:** N = 50 Deterministic Seeds (Seeds 1 to 50)  
**Bootstrap Resamples:** B_boot = 10,000  
**World Environments:**
- **World A (Familiar Baseline):** Friction $\mu = 0.88$, Actuator Scale $= 0.85$, Polarity $\mathbf{W}_{act} = +\mathbf{I}$, Gravity $g = 9.8$
- **World B (Novel Transferred Dynamics):** Friction $\mu = 0.71$, Actuator Scale $= 0.85$, Polarity $\mathbf{W}_{act} = -\mathbf{I}$, Gravity $g = 4.2$
- **World C (Radical Dynamic Shift):** Friction $\mu = 0.12$, Actuator Scale $= 0.51$, Polarity $\mathbf{W}_{act} = +\mathbf{I}$, Gravity $g = 15.7$

---

## 1. Quantitative Performance Matrix

| Experimental Condition | Metric | Mean ± StdDev | Parametric Normal 95% CI | Non-Parametric Bootstrap 95% CI | Raw Count / Threshold |
|---|---|---|---|---|---|
| **A → A (Familiar Baseline)** | Tracking Error $E(t)$ | 0.0050 ± 0.0000 | [0.0050, 0.0050] | [0.0050, 0.0050] | 50/50 (100.0%) |
| **A → B (Zero-Shot Novel B)** | Mean Shock Error $E(t)$ | 1.3079 ± 0.0421 | [1.2963, 1.3196] | [1.2968, 1.3195] | Zero-Shot Transfer Barrier |
| **A → C (Zero-Shot Radical C)** | Mean Shock Error $E(t)$ | 0.8117 ± 0.0272 | [0.8042, 0.8192] | [0.8041, 0.8191] | Zero-Shot Transfer Barrier |
| **A → B → B' (Adaptation)** | Initial Shock $E(0)$ | 1.8491 ± 0.3356 | [1.7561, 1.9422] | [1.7578, 1.9428] | Pre-adaptation shock ($t=1$) |
| **A → B → B' (Adaptation)** | Polarity Flip Latency | 7.00 ± 0.00 steps | [7.00, 7.00] | [7.00, 7.00] | Evidence $\Lambda_t < -0.50$ |
| **A → B → B' (Adaptation)** | Latency $T_\epsilon$ ($E < 0.20$) | 16.32 ± 0.62 steps | [16.15, 16.49] | [16.14, 16.50] | **50/50 seeds (100.0%)** |
| **A → B → B' (Adaptation)** | Rate $A_{adapt} = \frac{E(0)-E(T)}{B}$ | 0.0461 ± 0.0084 | [0.0438, 0.0485] | [0.0439, 0.0484] | **50/50 seeds (100.0%)** |
| **A → B → B' (Adaptation)** | Final Error $E(T)$ ($T=40$) | 0.0040 ± 0.0010 | [0.0037, 0.0043] | [0.0037, 0.0043] | **50/50 seeds (100.0%)** |

---

## 2. Mathematical Consistency Audit of $A_{adapt}$

The frozen evaluation equation for adaptation rate is:
$$ A_{adapt} = \frac{E(0) - E(T)}{B_{interaction}} $$

With interaction budget $B_{interaction} = 40$:
- Mean Initial Error $E(0) = 1.8491$
- Mean Final Error $E(T) = 0.0040$
- Computed Adaptation Rate:
  $$ \frac{1.8491 - 0.0040}{40} = 0.0461 $$
- Direct Average of Seed Rates: $\bar{A}_{adapt} = 0.0461$
- **Consistency Status:** Exact match within rounding tolerance ($\Delta < 0.0001$).

---

## 3. First-Crossing Latency Verification ($T_\epsilon$)

- **Definition:** $T_\epsilon = \min \{ t \in [1, B] : E(t) < 0.20 \}$.
- **Implementation Audit:** Verified that $T_\epsilon$ is registered at the exact first time-step where prediction error breaches the threshold, and is never updated on subsequent steps.
- **Result:** First crossing occurs at **16.32 ± 0.62 steps** across all 50 seeds. All 50/50 seeds successfully crossed well within the pre-registered maximum threshold of $T_\epsilon \le 20$.

---

## 4. Causal & Structural Polarity Adaptation Verification

1. **Autonomous Sensory Detection:**
   - Actuator polarity inversion in World B ($\mathbf{W}_{act} = -\mathbf{I}$) is inferred autonomously via the directional evidence accumulator:
     $$ \Lambda_t = 0.80 \Lambda_{t-1} + 0.20 \cos(\theta_t) $$
   - Where $\cos(\theta_t) = \frac{u_t \cdot \hat{a}_{motor}}{|u_t| \cdot |\hat{a}_{motor}|}$ with reafference cancelled $\hat{a}_{motor} = \Delta v_t + v_t(1 - \hat{\mu})$.
   - No privileged environment information or runner backdoor triggers the polarity flip.
2. **Deterministic Triggering:**
   - Inversion is triggered autonomously when $\Lambda_t < -0.50$.
   - The observed mean trigger step is **7.00 ± 0.00**, immediately preceding error collapse ($T_\epsilon = 16.32$).
   - This explicitly demonstrates the empirical chain:
     $$\text{Directional Surprise} \longrightarrow \text{Evidence Accumulation } \Lambda_t \longrightarrow \text{Hypothesis Inversion} \longrightarrow \text{Error Collapse } E(t) < 0.20$$
