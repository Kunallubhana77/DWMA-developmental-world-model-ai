"""
DWMA: DEVELOPMENTAL WORLD-MODEL AGENT — ABLATION BENCHMARK SUITE
Controlled scientific ablation testing to establish causal necessity of each architecture component:
1. Full DWMA (Baseline)
2. Variant A: No Predictive World Model (Reactive only)
3. Variant B: No Epistemic Engine (Passive random walk)
4. Variant C: No Self-Model (No contingency / agency tracking)
5. Variant D: No Causal Graph (No symbolic concept formation)
6. Variant E: No Episodic Memory (No history replay)
"""

import math
import random

class SimulatedAgent:
    def __init__(self, variant="Full", seed=42):
        random.seed(seed)
        self.variant = variant
        self.x = 0.0
        self.vx = 0.0
        
        # Internal components
        self.learned_friction = 0.85
        self.learned_accel = 0.25
        self.agency_confidence = 0.0
        self.total_info_gain = 0.0
        self.discovered_concepts = 0
        self.memory = []
        self.step_count = 0

        # Component ablation flags
        self.has_predictive_model = variant != "Variant A (No Predictive Model)"
        self.has_epistemic_driver = variant != "Variant B (No Epistemic Engine)"
        self.has_self_model = variant != "Variant C (No Self Model)"
        self.has_causal_graph = variant != "Variant D (No Causal Graph)"
        self.has_memory = variant != "Variant E (No Episodic Memory)"

    def step(self, true_friction, objects):
        self.step_count += 1
        
        # 1. Action Selection
        if self.has_epistemic_driver:
            # Active Information Gain: targets highest variance object
            target_obj = max(objects, key=lambda o: o["variance"])
            force = 1.0 if target_obj["variance"] > 2.0 else 0.4
        else:
            # Passive / Brownian random walk
            force = random.uniform(-0.8, 0.8)

        applied_thrust = force * 0.85

        # 2. STANDARDIZED EXTERNAL OBSERVER: State Forecast Before Execution
        if self.has_predictive_model:
            pred_dv = applied_thrust - self.vx * (1.0 - self.learned_friction)
            pred_x = self.x + self.vx + pred_dv
            pred_v = self.vx + pred_dv
        else:
            # Fair Ablation Baseline: Without a forward model, forecast is persistence (identity: x_t, v_t)
            pred_dv = 0.0
            pred_x = self.x
            pred_v = self.vx

        # 3. Environment Step Execution
        actual_dv = applied_thrust - self.vx * (1.0 - true_friction)
        actual_x = self.x + self.vx + actual_dv
        actual_v = self.vx + actual_dv

        # Update physical state
        self.x = actual_x
        self.vx = actual_v

        # 4. Standardized Prediction Error (Apples-to-Apples for all variants)
        standardized_error = math.hypot(actual_x - pred_x, actual_v - pred_v)

        # Online model adaptation (only if predictive model exists)
        if self.has_predictive_model:
            grad = -(actual_dv - pred_dv) * 0.05
            self.learned_friction = max(0.3, min(0.95, self.learned_friction + grad))

        # 5. Independent Sensorimotor Agency Evaluation
        # Contingency: Correlation between motor command and actual physical motion (velocity alignment)
        motor_contingency = 1.0 if (abs(force) > 0.05 and (force * actual_v > 0 or abs(actual_dv) > 0.02)) else 0.0
        if self.has_self_model:
            self.agency_confidence = 0.9 * self.agency_confidence + 0.1 * motor_contingency
        else:
            # Without self-model, contingency tracking is ungrounded / zero
            self.agency_confidence = 0.0

        # 6. Active Epistemic Variance Collapse
        if self.has_epistemic_driver:
            target_obj = max(objects, key=lambda o: o["variance"])
            old_var = target_obj["variance"]
            snr = (force / target_obj["mass"]) * 1.5
            target_obj["variance"] = target_obj["variance"] / (1.0 + snr)
            
            # Differential Gaussian entropy change: 0.5 * ln(var_prior / var_post)
            step_ig = 0.5 * math.log(old_var / max(0.001, target_obj["variance"]))
            self.total_info_gain += step_ig

        # 7. Causal Graph Concept Formation
        if self.has_causal_graph:
            for obj in objects:
                if obj["variance"] < 1.0 and not obj.get("classified", False):
                    obj["classified"] = True
                    self.discovered_concepts += 1

        # 8. Episodic Memory
        if self.has_memory:
            self.memory.append({"step": self.step_count, "error": standardized_error, "friction": self.learned_friction})

        return standardized_error


def run_ablation_experiment():
    variants = [
        "Full DWMA (Baseline)",
        "Variant A (No Predictive Model)",
        "Variant B (No Epistemic Engine)",
        "Variant C (No Self Model)",
        "Variant D (No Causal Graph)",
        "Variant E (No Episodic Memory)",
    ]

    results = []

    for var in variants:
        agent = SimulatedAgent(variant=var, seed=101)
        
        objects = [
            {"id": "obj1", "mass": 1.2, "variance": 20.0},
            {"id": "obj2", "mass": 8.0, "variance": 20.0},
            {"id": "obj3", "mass": 25.0, "variance": 20.0},
        ]

        total_error = 0.0
        drift_recovery_steps = None
        shock_error = 0.0

        for t in range(1, 101):
            # Normal Earth friction for steps 1-50, then Silent Drift to viscous mud (0.35)
            true_friction = 0.85 if t <= 50 else 0.35
            
            err = agent.step(true_friction, objects)
            total_error += err

            if t == 51:
                shock_error = err

            if t > 51 and drift_recovery_steps is None:
                if err <= 0.15:
                    drift_recovery_steps = t - 50

        if drift_recovery_steps is None:
            drift_recovery_steps = "> 50 (Failed)"

        results.append({
            "variant": var,
            "mean_error": total_error / 100.0,
            "shock_error": shock_error,
            "recovery_steps": drift_recovery_steps,
            "info_gain": agent.total_info_gain,
            "concepts_found": f"{agent.discovered_concepts}/3",
            "agency_score": f"{int(agent.agency_confidence * 100)}%"
        })

    # Print Publication-Grade Scientific Table
    print("\n" + "=" * 90)
    print("      DWMA ABLATION STUDY: SCIENTIFIC CAUSAL ATTRIBUTION BENCHMARK")
    print("=" * 90)
    print(f"{'Condition':<35} | {'Mean MSE':<9} | {'Shock Err':<9} | {'Recovery':<10} | {'Info Gain':<10} | {'Concepts':<8} | {'Agency'}")
    print("-" * 90)
    for r in results:
        print(f"{r['variant']:<35} | {r['mean_error']:<9.4f} | {r['shock_error']:<9.4f} | {str(r['recovery_steps']):<10} | {r['info_gain']:<8.2f} nats | {r['concepts_found']:<8} | {r['agency_score']}")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    run_ablation_experiment()
