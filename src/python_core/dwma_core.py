"""
DWMA: Developmental World-Model AI Core
A foundational, LLM-less cognitive engine inspired by infant brain development.
Core Loop: Perception -> Prediction -> Action -> Consequence -> Error -> Memory -> Causal Update
"""

import math
import random
from typing import Dict, List, Tuple, Any

class SelfModel:
    """
    Agency Tracker: Discovers what is 'Self' vs 'Environment'
    Uses contingency detection (correlation between motor intention and sensory shift).
    """
    def __init__(self):
        self.contingencies = {'pos_shift': 0.5, 'vel_shift': 0.5}
        self.body_features = set()

    def update_contingency(self, action: List[float], state_delta: List[float]):
        action_mag = math.sqrt(action[0]**2 + action[1]**2)
        vel_mag = math.sqrt(state_delta[2]**2 + state_delta[3]**2)
        pos_mag = math.sqrt(state_delta[0]**2 + state_delta[1]**2)
        
        if action_mag > 0.05:
            # How closely does the movement delta match the motor command?
            match_vel = 1.0 - min(1.0, abs(action_mag * 0.5 - vel_mag) / (action_mag * 0.5 + 0.1))
            match_pos = 1.0 - min(1.0, abs(action_mag * 0.3 - pos_mag) / (action_mag * 0.3 + 0.1))
            
            self.contingencies['vel_shift'] = 0.88 * self.contingencies['vel_shift'] + 0.12 * match_vel
            self.contingencies['pos_shift'] = 0.88 * self.contingencies['pos_shift'] + 0.12 * match_pos
            
        if self.contingencies['vel_shift'] > 0.75:
            self.body_features.add("EgoVelocityActuator")
        if self.contingencies['pos_shift'] > 0.75:
            self.body_features.add("EgoPositionProprioception")

    def is_self(self, feature_name: str) -> bool:
        return feature_name in self.body_features

class PredictiveWorldModel:
    """
    Forward Dynamics Model: Predicts DELTA state (change in velocity and position).
    DeltaState_hat = W_action * action + W_friction * current_velocity
    Normalized adaptive estimation for high numerical stability.
    """
    def __init__(self):
        # Learned physical parameters:
        # acceleration_factor: how much 1 unit of force accelerates body
        self.accel_x = 0.1
        self.accel_y = 0.1
        self.friction_x = 0.5
        self.friction_y = 0.5
        self.learning_rate = 0.05
        self.prediction_history = []
        self.error_history = []

    def predict_delta(self, state: List[float], action: List[float]) -> List[float]:
        # state: [x, y, vx, vy]
        # action: [fx, fy]
        pred_dvx = (action[0] * self.accel_x) - (state[2] * (1.0 - self.friction_x))
        pred_dvy = (action[1] * self.accel_y) - (state[3] * (1.0 - self.friction_y))
        pred_dx = state[2] + pred_dvx
        pred_dy = state[3] + pred_dvy
        return [pred_dx, pred_dy, pred_dvx, pred_dvy]

    def predict(self, state: List[float], action: List[float]) -> List[float]:
        delta = self.predict_delta(state, action)
        return [
            state[0] + delta[0],
            state[1] + delta[1],
            state[2] + delta[2],
            state[3] + delta[3]
        ]

    def update(self, state: List[float], action: List[float], actual_next_state: List[float]) -> float:
        actual_delta = [
            actual_next_state[0] - state[0],
            actual_next_state[1] - state[1],
            actual_next_state[2] - state[2],
            actual_next_state[3] - state[3]
        ]
        pred_delta = self.predict_delta(state, action)
        
        err_dx = actual_delta[0] - pred_delta[0]
        err_dy = actual_delta[1] - pred_delta[1]
        err_dvx = actual_delta[2] - pred_delta[2]
        err_dvy = actual_delta[3] - pred_delta[3]
        
        total_error = math.sqrt(err_dx**2 + err_dy**2 + err_dvx**2 + err_dvy**2)
        
        # Adaptive learning for acceleration and friction constants
        if abs(action[0]) > 0.1:
            self.accel_x += self.learning_rate * (err_dvx / action[0]) * 0.1
            self.accel_x = max(0.01, min(2.0, self.accel_x))
        if abs(action[1]) > 0.1:
            self.accel_y += self.learning_rate * (err_dvy / action[1]) * 0.1
            self.accel_y = max(0.01, min(2.0, self.accel_y))
            
        if abs(state[2]) > 0.1:
            self.friction_x -= self.learning_rate * (err_dvx / state[2]) * 0.05
            self.friction_x = max(0.1, min(0.99, self.friction_x))
        if abs(state[3]) > 0.1:
            self.friction_y -= self.learning_rate * (err_dvy / state[3]) * 0.05
            self.friction_y = max(0.1, min(0.99, self.friction_y))
            
        self.error_history.append(total_error)
        return total_error

class CuriosityEngine:
    """
    Epistemic Curiosity:
    Selects actions that navigate towards unvisited or high-uncertainty regions.
    """
    def __init__(self):
        self.surprise_history = []
        self.visited_sectors = {}  # (grid_x, grid_y) -> visit count

    def compute_intrinsic_reward(self, prediction_error: float) -> float:
        intrinsic_reward = math.tanh(prediction_error * 2.0)
        self.surprise_history.append(prediction_error)
        return intrinsic_reward

    def select_curious_action(self, candidate_actions: List[List[float]], current_pos: List[float], entity_positions: List[List[float]]) -> List[float]:
        """
        Directs the agent toward the closest object that hasn't been thoroughly explored.
        """
        best_action = candidate_actions[0]
        max_attraction = -999.0
        
        for action in candidate_actions:
            next_x = current_pos[0] + action[0]
            next_y = current_pos[1] + action[1]
            
            # Attraction to objects (natural infant urge to grasp / touch)
            score = 0.0
            for obj_pos in entity_positions:
                dist = math.dist([next_x, next_y], obj_pos)
                score += 1.0 / (dist + 0.5)
                
            # Random exploratory jitter
            score += random.uniform(-0.1, 0.1)
            
            if score > max_attraction:
                max_attraction = score
                best_action = action
                
        return best_action

class CausalGraph:
    """
    Autonomous Concept & Causal Relationship Formation.
    Induces rules: [Condition / Entity Properties] + [Action] -> [Outcome / State Delta]
    Without any human language labels.
    """
    def __init__(self):
        self.edges = []
        self.entity_profiles = {}

    def record_interaction(self, entity_id: str, action_type: str, displacement: float, force: float):
        if entity_id not in self.entity_profiles:
            self.entity_profiles[entity_id] = {
                'interactions': 0,
                'total_displacement': 0.0,
                'avg_mobility': 0.0,
                'inferred_concept': 'Unexplored Entity'
            }
        
        p = self.entity_profiles[entity_id]
        p['interactions'] += 1
        p['total_displacement'] += displacement
        p['avg_mobility'] = p['total_displacement'] / max(1, p['interactions'])
        
        # Concept induction based on physical dynamics
        if p['interactions'] >= 3:
            if p['avg_mobility'] < 0.05:
                p['inferred_concept'] = 'Immovable Static Barrier'
            elif p['avg_mobility'] > 0.4:
                p['inferred_concept'] = 'Lightweight Dynamic Object'
            else:
                p['inferred_concept'] = 'Heavy Resistive Object'
                
        rule_key = f"Push_{entity_id}"
        found = False
        for edge in self.edges:
            if edge['rule'] == rule_key:
                edge['count'] += 1
                edge['confidence'] = min(0.99, edge['confidence'] + 0.05)
                edge['effect'] = f"Displacement ~ {p['avg_mobility']:.2f}"
                found = True
                break
        if not found:
            self.edges.append({
                'rule': rule_key,
                'entity': entity_id,
                'action': action_type,
                'effect': f"Displacement ~ {displacement:.2f}",
                'confidence': 0.5,
                'count': 1
            })

class DWMABrain:
    """
    Unified Developmental World-Model AI Brain.
    Orchestrates the infant-learning cycle.
    """
    def __init__(self):
        self.self_model = SelfModel()
        self.world_model = PredictiveWorldModel()
        self.curiosity = CuriosityEngine()
        self.causal_graph = CausalGraph()
        self.development_age_steps = 0
        self.current_stage = 0

    def step(self, raw_sensors: Dict[str, Any], candidate_actions: List[List[float]], entity_positions: List[List[float]]) -> Tuple[List[float], Dict[str, Any]]:
        self.development_age_steps += 1
        state_vec = [
            raw_sensors.get('pos_x', 0.0),
            raw_sensors.get('pos_y', 0.0),
            raw_sensors.get('vel_x', 0.0),
            raw_sensors.get('vel_y', 0.0)
        ]
        
        # Stage progression
        if self.development_age_steps < 60:
            self.current_stage = 0  # Motor babbling & Self-discovery
        elif self.development_age_steps < 160:
            self.current_stage = 1  # Physical object interaction
        elif self.development_age_steps < 300:
            self.current_stage = 2  # Active curiosity
        else:
            self.current_stage = 3  # Causal planning

        # Action Selection
        if self.current_stage == 0:
            action = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
        elif self.current_stage == 1:
            action = [random.gauss(0.0, 0.8), random.gauss(0.0, 0.8)]
        else:
            action = self.curiosity.select_curious_action(candidate_actions, [state_vec[0], state_vec[1]], entity_positions)

        meta = {
            'stage': self.current_stage,
            'step': self.development_age_steps,
            'body_features': list(self.self_model.body_features),
            'concepts_discovered': {k: v['inferred_concept'] for k, v in self.causal_graph.entity_profiles.items()}
        }
        return action, meta

    def observe_consequence(self, prev_state: List[float], action: List[float], actual_next_state: List[float], interacted_entity: Dict[str, Any] = None) -> float:
        error = self.world_model.update(prev_state, action, actual_next_state)
        self.curiosity.compute_intrinsic_reward(error)

        deltas = [
            actual_next_state[0] - prev_state[0],
            actual_next_state[1] - prev_state[1],
            actual_next_state[2] - prev_state[2],
            actual_next_state[3] - prev_state[3]
        ]
        self.self_model.update_contingency(action, deltas)

        if interacted_entity:
            self.causal_graph.record_interaction(
                entity_id=interacted_entity['id'],
                action_type='push',
                displacement=interacted_entity.get('displacement', 0.0),
                force=math.sqrt(action[0]**2 + action[1]**2)
            )

        return error
