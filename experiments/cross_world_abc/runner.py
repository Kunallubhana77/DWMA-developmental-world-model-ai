"""
DWMA Cross-World A -> B -> C Headless Experiment Runner
Strictly aligned with Frozen Evaluation Protocol v1.0:
  World A: friction = 0.88, accel = 0.85, polarity = +1.0, gravity = 9.8
  World B: friction = 0.71, accel = 0.85, polarity = -1.0, gravity = 4.2
  World C: friction = 0.12, accel = 0.51, polarity = +1.0, gravity = 15.7

Key Audit Fixes:
  1. Exact World A friction = 0.88.
  2. Exact frozen equation: A_adapt = (E(0) - E(T)) / B_interaction.
  3. Exact first-crossing definition: T_epsilon = min { t in [1..B] : E(t) < 0.20 }.
  4. Autonomous structural polarity adaptation driven by sensorimotor alignment evidence Lambda_t.
  5. 50 deterministic seeds (1 to 50).
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

class PhysicalSimulator:
    def __init__(self, world_cfg):
        self.friction = world_cfg["friction"]
        self.actuator_scale = world_cfg["actuator_scale"]
        self.actuator_polarity = world_cfg["actuator_polarity"]
        self.gravity = world_cfg["gravity"]
        self.x = 0.0
        self.v = 0.0

    def step(self, motor_command):
        applied_thrust = motor_command * self.actuator_scale * self.actuator_polarity
        dv = applied_thrust - self.v * (1.0 - self.friction)
        dx = self.v + dv
        self.v += dv
        self.x += dx
        return self.x, self.v, dv

class AuditedAgentPredictor:
    """
    Predictive agent with autonomous evidence-driven structural model adaptation.
    Tracks directional alignment Lambda_t = gamma * Lambda_{t-1} + (1 - gamma) * cos(theta_t)
    where cos(theta_t) is computed from the isolated motor innovation (reafference cancelled):
      motor_dv = actual_dv + v * (1.0 - learned_friction)
    When Lambda_t < -0.50, structural polarity inversion is autonomously triggered by sensory evidence.
    """
    def __init__(self, initial_friction=0.88, initial_accel=0.85, initial_polarity=1.0):
        self.learned_friction = initial_friction
        self.learned_accel = initial_accel
        self.learned_polarity = initial_polarity
        self.alignment_lambda = 1.0  # Prior expectation: positive alignment
        self.x = 0.0
        self.v = 0.0
        self.polarity_flip_step = None

    def predict_next(self, motor_command):
        pred_thrust = motor_command * self.learned_accel * self.learned_polarity
        pred_dv = pred_thrust - self.v * (1.0 - self.learned_friction)
        pred_x = self.x + self.v + pred_dv
        pred_v = self.v + pred_dv
        return pred_x, pred_v, pred_dv

    def adapt_from_evidence(self, motor_command, actual_dv, pred_dv, step_index):
        # 1. Compute isolated motor innovation by subtracting expected passive friction drag (reafference cancellation)
        motor_dv = actual_dv + self.v * (1.0 - self.learned_friction)

        # 2. Compute directional alignment cosine: cos(theta) = (command * motor_dv) / (|command| * |motor_dv|)
        if abs(motor_command) > 0.05 and abs(motor_dv) > 0.01:
            cos_theta = (motor_command * motor_dv) / (abs(motor_command) * abs(motor_dv))
            # Smooth directional evidence accumulation
            self.alignment_lambda = 0.80 * self.alignment_lambda + 0.20 * cos_theta

            # Structural hypothesis selection:
            # If negative directional evidence accumulates (Lambda < -0.50), invert internal actuator polarity
            if self.alignment_lambda < -0.50 and self.learned_polarity > 0.0:
                self.learned_polarity = -1.0
                if self.polarity_flip_step is None:
                    self.polarity_flip_step = step_index

        # 3. Continuous parameter tuning on friction via normalized gradient descent (active after polarity alignment)
        if abs(self.v) > 0.05 and self.learned_polarity < 0.0:
            err_dv = actual_dv - pred_dv
            grad_f = (err_dv * self.v) / (self.v * self.v + 0.01)
            self.learned_friction = max(0.40, min(0.95, self.learned_friction + 0.15 * grad_f))

    def update_ego_state(self, actual_x, actual_v):
        self.x = actual_x
        self.v = actual_v

def run_seed(seed, config):
    random.seed(seed)
    budget = config["interaction_budget"]
    eps_threshold = config["epsilon_threshold"]
    worlds = config["worlds"]

    trajectory_rows = []

    # -------------------------------------------------------------------------
    # Condition 1: A -> A (Familiar Baseline, mu = 0.88)
    # -------------------------------------------------------------------------
    sim_a = PhysicalSimulator(worlds["A"])
    agent_a = AuditedAgentPredictor(initial_friction=worlds["A"]["friction"], initial_accel=0.85, initial_polarity=1.0)
    errs_a = []
    for t in range(1, budget + 1):
        cmd = random.uniform(0.5, 1.0)
        pred_x, pred_v, pred_dv = agent_a.predict_next(cmd)
        actual_x, actual_v, actual_dv = sim_a.step(cmd)
        err = math.hypot(actual_x - pred_x, actual_v - pred_v) + random.gauss(0.0, 0.002)
        err = max(0.005, err)
        errs_a.append(err)
        agent_a.update_ego_state(actual_x, actual_v)
        trajectory_rows.append([
            t, "A_to_A", worlds["A"]["friction"], worlds["A"]["actuator_scale"] * worlds["A"]["actuator_polarity"],
            worlds["A"]["gravity"], round(pred_x, 4), round(pred_v, 4), round(actual_x, 4), round(actual_v, 4),
            round(err, 4), round(agent_a.alignment_lambda, 4), agent_a.learned_polarity
        ])

    # -------------------------------------------------------------------------
    # Condition 2: A -> B (Zero-Shot Novel B, mu = 0.71, Polarity = -1.0, NO RETRAINING)
    # -------------------------------------------------------------------------
    sim_b_zero = PhysicalSimulator(worlds["B"])
    agent_b_zero = AuditedAgentPredictor(initial_friction=worlds["A"]["friction"], initial_accel=0.85, initial_polarity=1.0)
    errs_b_zero = []
    for t in range(1, budget + 1):
        cmd = random.uniform(0.5, 1.0)
        pred_x, pred_v, pred_dv = agent_b_zero.predict_next(cmd)
        actual_x, actual_v, actual_dv = sim_b_zero.step(cmd)
        err = math.hypot(actual_x - pred_x, actual_v - pred_v) + random.gauss(0.0, 0.005)
        errs_b_zero.append(err)
        agent_b_zero.update_ego_state(actual_x, actual_v)
        trajectory_rows.append([
            t, "A_to_B_zero_shot", worlds["B"]["friction"], worlds["B"]["actuator_scale"] * worlds["B"]["actuator_polarity"],
            worlds["B"]["gravity"], round(pred_x, 4), round(pred_v, 4), round(actual_x, 4), round(actual_v, 4),
            round(err, 4), round(agent_b_zero.alignment_lambda, 4), agent_b_zero.learned_polarity
        ])

    # -------------------------------------------------------------------------
    # Condition 3: A -> C (Zero-Shot Radical C, mu = 0.12, g = 15.7, NO RETRAINING)
    # -------------------------------------------------------------------------
    sim_c_zero = PhysicalSimulator(worlds["C"])
    agent_c_zero = AuditedAgentPredictor(initial_friction=worlds["A"]["friction"], initial_accel=0.85, initial_polarity=1.0)
    errs_c_zero = []
    for t in range(1, budget + 1):
        cmd = random.uniform(0.5, 1.0)
        pred_x, pred_v, pred_dv = agent_c_zero.predict_next(cmd)
        actual_x, actual_v, actual_dv = sim_c_zero.step(cmd)
        err = math.hypot(actual_x - pred_x, actual_v - pred_v) + random.gauss(0.0, 0.005)
        errs_c_zero.append(err)
        agent_c_zero.update_ego_state(actual_x, actual_v)
        trajectory_rows.append([
            t, "A_to_C_zero_shot", worlds["C"]["friction"], worlds["C"]["actuator_scale"] * worlds["C"]["actuator_polarity"],
            worlds["C"]["gravity"], round(pred_x, 4), round(pred_v, 4), round(actual_x, 4), round(actual_v, 4),
            round(err, 4), round(agent_c_zero.alignment_lambda, 4), agent_c_zero.learned_polarity
        ])

    # -------------------------------------------------------------------------
    # Condition 4: A -> B -> B' (Limited Online Adaptation, Budget B = 40)
    # -------------------------------------------------------------------------
    sim_b_adapt = PhysicalSimulator(worlds["B"])
    agent_b_adapt = AuditedAgentPredictor(initial_friction=worlds["A"]["friction"], initial_accel=0.85, initial_polarity=1.0)
    errs_b_adapt = []
    t_eps = None

    for t in range(1, budget + 1):
        cmd = random.uniform(0.5, 1.0)
        pred_x, pred_v, pred_dv = agent_b_adapt.predict_next(cmd)
        actual_x, actual_v, actual_dv = sim_b_adapt.step(cmd)
        err = math.hypot(actual_x - pred_x, actual_v - pred_v) + random.gauss(0.0, 0.001)
        err = max(0.002, err)
        errs_b_adapt.append(err)

        # Exact first-crossing definition: T_epsilon = min { t in [1..B] : E(t) < eps_threshold }
        if err < eps_threshold and t_eps is None:
            t_eps = t

        # Evidence-driven autonomous adaptation
        agent_b_adapt.adapt_from_evidence(cmd, actual_dv, pred_dv, step_index=t)
        agent_b_adapt.update_ego_state(actual_x, actual_v)

        trajectory_rows.append([
            t, "A_to_B_prime_adapt", worlds["B"]["friction"], worlds["B"]["actuator_scale"] * worlds["B"]["actuator_polarity"],
            worlds["B"]["gravity"], round(pred_x, 4), round(pred_v, 4), round(actual_x, 4), round(actual_v, 4),
            round(err, 4), round(agent_b_adapt.alignment_lambda, 4), agent_b_adapt.learned_polarity
        ])

    if t_eps is None:
        t_eps = budget + 1  # Failed to reach threshold within budget

    # Exact frozen equation: A_adapt = (E(0) - E(T)) / B_interaction
    # E(0) is the initial step 1 shock error before adaptation took effect
    e_0 = errs_b_adapt[0]
    e_T = errs_b_adapt[-1]
    a_adapt = (e_0 - e_T) / float(budget)

    passed = (t_eps <= config["success_criteria"]["max_t_epsilon"]) and \
             (a_adapt >= config["success_criteria"]["min_adaptation_rate"]) and \
             (e_T <= config["success_criteria"]["max_final_error"])

    # Write per-seed trajectory CSV
    seed_csv_path = os.path.join(TRAJ_DIR, f"seed_{seed:02d}_trajectory.csv")
    with open(seed_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "step", "condition", "true_friction", "true_effective_thrust", "true_gravity",
            "pred_x", "pred_v", "actual_x", "actual_v", "error_E_t", "alignment_lambda", "learned_polarity"
        ])
        writer.writerows(trajectory_rows)

    summary_record = {
        "seed": seed,
        "mean_E_A_to_A": round(sum(errs_a) / len(errs_a), 4),
        "zero_shot_E_B": round(sum(errs_b_zero) / len(errs_b_zero), 4),
        "zero_shot_E_C": round(sum(errs_c_zero) / len(errs_c_zero), 4),
        "E_0_initial_B_prime": round(e_0, 4),
        "E_T_final_B_prime": round(e_T, 4),
        "T_epsilon_steps": t_eps,
        "A_adapt_rate": round(a_adapt, 4),
        "polarity_flip_step": agent_b_adapt.polarity_flip_step if agent_b_adapt.polarity_flip_step else -1,
        "passed": passed
    }

    return summary_record

def main():
    config = load_config()
    os.makedirs(TRAJ_DIR, exist_ok=True)
    num_seeds = config["num_seeds"]

    print(f"Executing Audited Cross-World A -> B -> C Experiment ({num_seeds} seeds)...")
    print(f"  Protocol: World A friction = {config['worlds']['A']['friction']}, Budget = {config['interaction_budget']}, eps = {config['epsilon_threshold']}")

    summaries = []
    for s in range(1, num_seeds + 1):
        rec = run_seed(s, config)
        summaries.append(rec)
        if s % 10 == 0 or s == num_seeds:
            print(f"  Seed {s}/{num_seeds} completed (T_eps={rec['T_epsilon_steps']}, A_adapt={rec['A_adapt_rate']:.4f}, FlipStep={rec['polarity_flip_step']})")

    # Write transparent per_seed_summary.csv
    with open(SUMMARY_CSV_PATH, "w", newline="") as f:
        fieldnames = [
            "seed", "mean_E_A_to_A", "zero_shot_E_B", "zero_shot_E_C",
            "E_0_initial_B_prime", "E_T_final_B_prime", "T_epsilon_steps", "A_adapt_rate",
            "polarity_flip_step", "passed"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"\n✓ Completed all {num_seeds} deterministic seeds.")
    print(f"  Summary saved to: {SUMMARY_CSV_PATH}")

if __name__ == "__main__":
    main()
