"""
DWMA Experiment Runner: Simulates a Baby Brain interacting with an unknown world.
Demonstrates:
1. Convergence of self-model (agency discovery)
2. Reduction of predictive error over time (learning physics)
3. Emergence of causal concepts without human language or LLMs.
"""

import math
import random
from dwma_core import DWMABrain

def run_experiment():
    print("=================================================================")
    print("   DWMA: Developmental World-Model AI — Cognitive Benchmark")
    print("   LLM-less, Curiosity-Driven Developmental Learning")
    print("=================================================================\n")
    
    brain = DWMABrain()
    
    # Virtual 2D Physics Environment bounded in [-8, 8]
    agent_state = [0.0, 0.0, 0.0, 0.0]  # [x, y, vx, vy]
    
    entities = {
        'Object_A': {'mass': 100.0, 'pos': [4.0, 2.0], 'displacement': 0.0},
        'Object_B': {'mass': 0.8,   'pos': [-2.0, 3.0], 'displacement': 0.0},
        'Object_C': {'mass': 8.0,   'pos': [1.0, -3.0], 'displacement': 0.0},
    }

    print(f"[*] Initialized Environment with {len(entities)} unknown entities.")
    print("[*] Starting developmental trajectory (300 infant steps)...\n")
    
    candidate_actions = [
        [1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0],
        [0.7, 0.7], [-0.7, 0.7], [0.7, -0.7], [-0.7, -0.7]
    ]
    
    errors_epoch = []
    
    for step in range(1, 301):
        sensors = {
            'pos_x': agent_state[0],
            'pos_y': agent_state[1],
            'vel_x': agent_state[2],
            'vel_y': agent_state[3]
        }
        
        entity_positions = [e['pos'] for e in entities.values()]
        action, meta = brain.step(sensors, candidate_actions, entity_positions)
        
        # Ground Truth Physics Simulation
        true_accel = 0.4
        true_friction = 0.82
        
        next_vx = (agent_state[2] + action[0] * true_accel) * true_friction
        next_vy = (agent_state[3] + action[1] * true_accel) * true_friction
        next_x = agent_state[0] + next_vx
        next_y = agent_state[1] + next_vy
        
        # Bound within arena
        if abs(next_x) > 7.5:
            next_vx *= -0.5
            next_x = 7.5 if next_x > 0 else -7.5
        if abs(next_y) > 7.5:
            next_vy *= -0.5
            next_y = 7.5 if next_y > 0 else -7.5
            
        agent_next = [next_x, next_y, next_vx, next_vy]
        
        # Object collision / interaction
        interacted = None
        for name, ent in entities.items():
            dist = math.dist([next_x, next_y], ent['pos'])
            if dist < 1.8:
                force_mag = math.sqrt(action[0]**2 + action[1]**2)
                disp = min(1.2, (force_mag / ent['mass']) * 0.9)
                ent['pos'][0] += action[0] * (disp / (force_mag + 0.001))
                ent['pos'][1] += action[1] * (disp / (force_mag + 0.001))
                ent['displacement'] += disp
                interacted = {'id': name, 'displacement': disp}
                break
                
        error = brain.observe_consequence(agent_state, action, agent_next, interacted)
        errors_epoch.append(error)
        agent_state = agent_next
        
        if step in [20, 60, 160, 300]:
            recent_err = sum(errors_epoch[-20:]) / 20
            print(f"--- [Development Step {step:3d}] (Stage {meta['stage']}) ---")
            print(f" • Prediction Error (Running Avg): {recent_err:.4f}")
            print(f" • Self-Model Features Discovered: {meta['body_features']}")
            print(f" • Concepts Emerged: {meta['concepts_discovered']}")
            print(f" • Causal Rules Inferred: {len(brain.causal_graph.edges)}\n")

    print("=================================================================")
    print("                     BENCHMARK RESULTS")
    print("=================================================================")
    initial_error = sum(errors_epoch[:20]) / 20
    final_error = sum(errors_epoch[-20:]) / 20
    improvement = ((initial_error - final_error) / initial_error) * 100
    
    print(f"✓ Initial Prediction Error        : {initial_error:.4f}")
    print(f"✓ Final Prediction Error          : {final_error:.4f}")
    print(f"✓ Predictive Accuracy Gain        : +{improvement:.1f}%")
    print(f"✓ Self-Agency Bound Features      : {list(brain.self_model.body_features)}")
    print("\n✓ Emergent Causal Knowledge Base:")
    for edge in brain.causal_graph.edges:
        print(f"   - [{edge['rule']}] -> {edge['effect']} (Confidence: {edge['confidence']*100:.0f}%, Interactions: {edge['count']})")
    print("\n✓ Inferred Physical Concepts:")
    for ent_id, prof in brain.causal_graph.entity_profiles.items():
        print(f"   - {ent_id}: '{prof['inferred_concept']}' (Avg Mobility: {prof['avg_mobility']:.3f})")
    print("=================================================================\n")

if __name__ == "__main__":
    run_experiment()
