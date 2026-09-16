/**
 * DWMA Predictive World Model
 * Internal physics simulator of the agent's brain.
 * Predicts next state, computes surprise/error, and performs mental rollouts (imagination).
 */
export class PredictiveWorldModel {
  constructor() {
    // Learned intuitive physics parameters
    this.learnedAccel = 0.25;
    this.learnedFriction = 0.85;
    this.learningRate = 0.04;
    this.lastPrediction = null;
    this.lastError = 0.0;
    this.totalSteps = 0;
    this.errorHistory = [];
  }

  predictDelta(state, action) {
    const dvx = action.x * this.learnedAccel - state.vx * (1.0 - this.learnedFriction);
    const dvy = action.y * this.learnedAccel - state.vy * (1.0 - this.learnedFriction);
    const dx = state.vx + dvx;
    const dy = state.vy + dvy;
    return { dx, dy, dvx, dvy };
  }

  predictNextState(state, action) {
    const delta = this.predictDelta(state, action);
    return {
      x: state.x + delta.dx,
      y: state.y + delta.dy,
      vx: state.vx + delta.dvx,
      vy: state.vy + delta.dvy
    };
  }

  /**
   * Mental Rollout / Imagination: Simulates N steps into future
   */
  imagineTrajectory(initialState, actionSequence) {
    const trajectory = [{ ...initialState }];
    let currentState = { ...initialState };

    for (const action of actionSequence) {
      currentState = this.predictNextState(currentState, action);
      trajectory.push({ ...currentState });
    }
    return trajectory;
  }

  update(prevState, action, actualNextState) {
    this.totalSteps++;
    const actualDx = actualNextState.x - prevState.x;
    const actualDy = actualNextState.y - prevState.y;
    const actualDvx = actualNextState.vx - prevState.vx;
    const actualDvy = actualNextState.vy - prevState.vy;

    const predDelta = this.predictDelta(prevState, action);

    const errDx = actualDx - predDelta.dx;
    const errDy = actualDy - predDelta.dy;
    const errDvx = actualDvx - predDelta.dvx;
    const errDvy = actualDvy - predDelta.dvy;

    const totalError = Math.hypot(errDx, errDy, errDvx, errDvy);
    this.lastError = totalError;
    this.errorHistory.push(totalError);
    if (this.errorHistory.length > 200) this.errorHistory.shift();

    // Online adaptive update of internal parameters
    const actionMag = Math.hypot(action.x, action.y);
    if (actionMag > 0.05) {
      const gradAccel = (errDvx * action.x + errDvy * action.y) / (actionMag * actionMag);
      this.learnedAccel += this.learningRate * Math.max(-0.5, Math.min(0.5, gradAccel)) * 0.1;
      this.learnedAccel = Math.max(0.05, Math.min(1.2, this.learnedAccel));
    }

    const speed = Math.hypot(prevState.vx, prevState.vy);
    if (speed > 0.05) {
      const gradFriction = -(errDvx * prevState.vx + errDvy * prevState.vy) / (speed * speed);
      this.learnedFriction += this.learningRate * Math.max(-0.5, Math.min(0.5, gradFriction)) * 0.05;
      this.learnedFriction = Math.max(0.4, Math.min(0.98, this.learnedFriction));
    }

    return totalError;
  }

  getInternalWeights() {
    return {
      learnedFriction: this.learnedFriction,
      learnedAccel: this.learnedAccel,
      learningRate: this.learningRate,
      lastError: this.lastError
    };
  }

  /**
   * Counterfactual Simulation:
   * Predicts hypothetical displacement of an object under force F WITHOUT executing physical intervention.
   */
  predictCounterfactual(mass, appliedForce) {
    const effectiveMass = Math.max(0.1, mass);
    const forceMag = Math.hypot(appliedForce.x, appliedForce.y);
    const impulse = (forceMag / effectiveMass) * this.learnedAccel * 12.0;
    // Estimated displacement based on current learned friction damping
    const expectedDisplacement = impulse / Math.max(0.05, 1.0 - this.learnedFriction);
    return {
      expectedDisplacement,
      impulse,
      appliedForce,
      learnedModelFriction: this.learnedFriction
    };
  }
}
