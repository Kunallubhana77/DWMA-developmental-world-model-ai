"""
DWMA Nonlinear Hypothesis Discrimination Experiment (H1: kv vs H2: kv^2)
Strictly aligned with Frozen Evaluation Protocol v1.0 (Section 7.2):
  Ground Truth: F_true(v) = -k_true * v^2 * sgn(v), where k_true = 0.08
  Competing Hypotheses:
    H1: F_1(v) = -k_1 * v (Linear Viscous Drag)
    H2: F_2(v) = -k_2 * v^2 * sgn(v) (Quadratic Aerodynamic Drag)

Discriminative Metric:
  Delta(v) = |F_1(v) - F_2(v)|

Bayesian Model Selection Criterion:
  ln(B_21) = (SSE_1 - SSE_2) / (2 * sigma^2) > 10.0 (Decisive Evidence)

Fair Comparison:
  DWMA Epistemic Policy vs Random Babbler Baseline
  Same seeds (1 to 50), same environment, same budget (30 steps).
"""

import os
import json
import math
import random
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DATA_DIR = os.path.join(BASE_DIR, "data")
TRAJ_DIR = os.path.join(DATA_DIR, "raw_trajectories")
SUMMARY_CSV_PATH = os.path.join(DATA_DIR, "per_seed_summary.csv")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

class DragSimulator:
    def __init__(self, k_true, sigma, v_bounds, rng=None):
        self.k_true = k_true
        self.sigma = sigma
        self.v_min, self.v_max = v_bounds
        self.v = 0.0
        self.rng = rng if rng is not None else random.Random()

    def step(self, u):
        sgn = 1.0 if self.v >= 0.0 else -1.0
        f_drag = -self.k_true * (self.v ** 2) * sgn
        noise = self.rng.gauss(0.0, self.sigma)
        dv = u + f_drag + noise
        v_next = max(self.v_min, min(self.v_max, self.v + dv))
        obs_drag = dv - u
        v_curr = self.v
        self.v = v_next
        return v_curr, obs_drag, v_next

def run_agent_trial(is_epistemic, seed, config):
    env_rng = random.Random(seed)
    agent_rng = random.Random(seed + 1000)
    env_cfg = config["environment"]
    budget = config["interaction_budget"]
    k_true = env_cfg["k_true"]
    sigma = env_cfg["observation_noise_sigma"]
    candidate_actions = env_cfg["candidate_actions"]
    v_bounds = env_cfg["velocity_bounds"]

    sim = DragSimulator(k_true, sigma, v_bounds, rng=env_rng)

    v_history = []
    f_obs_history = []
    delta_history = []
    log_b21_history = []

    k1_hat = 0.08
    k2_hat = 0.08

    first_crossing_step = None
    step_rows = []

    for t in range(1, budget + 1):
        curr_v = sim.v

        # 1. Action selection policy
        if is_epistemic:
            # Targeted epistemic exploration: select action maximizing Delta(v_next)
            def eval_discriminative_value(act):
                v_cand = curr_v + act
                sgn_cand = 1.0 if v_cand >= 0.0 else -1.0
                f1_cand = -k1_hat * v_cand
                f2_cand = -k2_hat * (v_cand ** 2) * sgn_cand
                return abs(f1_cand - f2_cand)
            action = max(candidate_actions, key=eval_discriminative_value)
        else:
            # Uniform random babbler baseline (isolated RNG)
            action = agent_rng.choice(candidate_actions)

        # 2. Environment step (Ground Truth: Quadratic Drag)
        v_at_step, obs_drag, next_v = sim.step(action)

        v_history.append(v_at_step)
        f_obs_history.append(obs_drag)

        # Informative discrepancy at current step
        sgn_curr = 1.0 if v_at_step >= 0.0 else -1.0
        f1_pred = -k1_hat * v_at_step
        f2_pred = -k2_hat * (v_at_step ** 2) * sgn_curr
        delta_v = abs(f1_pred - f2_pred)
        delta_history.append(delta_v)

        # 3. Running online fit of both competing hypotheses
        # H1: F = -k1 * v
        sum_v2 = sum(x ** 2 for x in v_history)
        if sum_v2 > 1e-4:
            k1_hat = sum(-f * x for f, x in zip(f_obs_history, v_history)) / sum_v2

        # H2: F = -k2 * v^2 * sgn(v)
        sum_v4 = sum(x ** 4 for x in v_history)
        if sum_v4 > 1e-4:
            k2_hat = sum(-f * (x ** 2) * (1.0 if x >= 0.0 else -1.0) for f, x in zip(f_obs_history, v_history)) / sum_v4

        # 4. Running log Bayes factor ln(B21)
        sse_1 = sum((f - (-k1_hat * x)) ** 2 for f, x in zip(f_obs_history, v_history))
        sse_2 = sum((f - (-k2_hat * (x ** 2) * (1.0 if x >= 0.0 else -1.0))) ** 2 for f, x in zip(f_obs_history, v_history))

        # Precision-weighted log Bayes factor
        log_b21 = (sse_1 - sse_2) / (2.0 * (sigma ** 2))
        log_b21_history.append(log_b21)

        if log_b21 > config["bayes_factor_threshold"] and first_crossing_step is None:
            first_crossing_step = t

        step_rows.append([
            t, "Epistemic" if is_epistemic else "RandomBabbler",
            round(action, 2), round(v_at_step, 4), round(obs_drag, 4),
            round(delta_v, 4), round(k1_hat, 4), round(k2_hat, 4), round(log_b21, 4)
        ])

    passed = (first_crossing_step is not None)
    latency = first_crossing_step if first_crossing_step is not None else (budget + 1)
    rmse_1 = math.sqrt(sse_1 / budget)
    rmse_2 = math.sqrt(sse_2 / budget)
    mean_delta = sum(delta_history) / len(delta_history)
    peak_v = max(abs(x) for x in v_history)

    result = {
        "is_epistemic": is_epistemic,
        "log_b21_final": round(log_b21, 4),
        "passed": passed,
        "discrimination_latency": latency,
        "mean_delta_v": round(mean_delta, 4),
        "peak_velocity": round(peak_v, 4),
        "k1_hat": round(k1_hat, 4),
        "k2_hat": round(k2_hat, 4),
        "rmse_H1": round(rmse_1, 5),
        "rmse_H2": round(rmse_2, 5),
        "step_rows": step_rows
    }
    return result

def run_seed(seed, config):
    # Paired run on identical seed
    res_epistemic = run_agent_trial(True, seed, config)
    res_random = run_agent_trial(False, seed, config)

    # Save detailed trajectory for this seed
    seed_csv_path = os.path.join(TRAJ_DIR, f"seed_{seed:02d}_discrimination_trajectory.csv")
    with open(seed_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "policy", "action", "velocity", "observed_drag", "delta_v", "k1_hat", "k2_hat", "log_b21"])
        writer.writerows(res_epistemic["step_rows"])
        writer.writerows(res_random["step_rows"])

    summary_record = {
        "seed": seed,
        "epistemic_log_b21": res_epistemic["log_b21_final"],
        "epistemic_latency": res_epistemic["discrimination_latency"],
        "epistemic_passed": res_epistemic["passed"],
        "epistemic_delta_v": res_epistemic["mean_delta_v"],
        "epistemic_peak_v": res_epistemic["peak_velocity"],
        "epistemic_rmse_H1": res_epistemic["rmse_H1"],
        "epistemic_rmse_H2": res_epistemic["rmse_H2"],
        "random_log_b21": res_random["log_b21_final"],
        "random_latency": res_random["discrimination_latency"],
        "random_passed": res_random["passed"],
        "random_delta_v": res_random["mean_delta_v"],
        "random_peak_v": res_random["peak_velocity"],
        "random_rmse_H1": res_random["rmse_H1"],
        "random_rmse_H2": res_random["rmse_H2"]
    }
    return summary_record

def main():
    config = load_config()
    os.makedirs(TRAJ_DIR, exist_ok=True)
    num_seeds = config["num_seeds"]

    print(f"Executing Phase 4: Nonlinear Hypothesis Discrimination ({num_seeds} seeds)...")
    print(f"  Ground Truth: F(v) = -{config['environment']['k_true']} * v^2 * sgn(v)")
    print(f"  Threshold: ln(B_21) > {config['bayes_factor_threshold']} within {config['interaction_budget']} steps")

    summaries = []
    for s in range(1, num_seeds + 1):
        rec = run_seed(s, config)
        summaries.append(rec)
        if s % 10 == 0 or s == num_seeds:
            print(f"  Seed {s:02d}/{num_seeds} complete | Epistemic: ln(B)={rec['epistemic_log_b21']:.2f}, Latency={rec['epistemic_latency']} st | Random: ln(B)={rec['random_log_b21']:.2f}, Latency={rec['random_latency']} st")

    # Save summary CSV
    with open(SUMMARY_CSV_PATH, "w", newline="") as f:
        fieldnames = [
            "seed",
            "epistemic_log_b21", "epistemic_latency", "epistemic_passed", "epistemic_delta_v", "epistemic_peak_v", "epistemic_rmse_H1", "epistemic_rmse_H2",
            "random_log_b21", "random_latency", "random_passed", "random_delta_v", "random_peak_v", "random_rmse_H1", "random_rmse_H2"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"\n✓ Completed all {num_seeds} paired seeds.")
    print(f"  Summary saved to: {SUMMARY_CSV_PATH}")

if __name__ == "__main__":
    main()
