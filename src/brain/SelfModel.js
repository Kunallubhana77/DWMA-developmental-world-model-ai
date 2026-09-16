/**
 * DWMA Self-Model & Agency Tracker
 * Detects contingency between internal motor commands and sensory changes.
 * Differentiates the 'Ego' (Body) from the 'Allo' (Environment).
 */
export class SelfModel {
  constructor() {
    this.contingencies = {
      velocityActuator: 0.5,
      positionProprioception: 0.5,
      headingOrientation: 0.5
    };
    this.bodyFeatures = new Set();
    this.agencyConfidence = 0.5;
  }

  update(action, stateDelta) {
    const actionMag = Math.hypot(action.x, action.y);
    const velMag = Math.hypot(stateDelta.vx, stateDelta.vy);
    const posMag = Math.hypot(stateDelta.dx, stateDelta.dy);

    if (actionMag > 0.05) {
      // Correlation score between action intention and resulting movement
      const velMatch = Math.max(0, 1.0 - Math.abs(actionMag * 0.5 - velMag) / (actionMag * 0.5 + 0.1));
      const posMatch = Math.max(0, 1.0 - Math.abs(actionMag * 0.35 - posMag) / (actionMag * 0.35 + 0.1));

      this.contingencies.velocityActuator = 0.88 * this.contingencies.velocityActuator + 0.12 * velMatch;
      this.contingencies.positionProprioception = 0.88 * this.contingencies.positionProprioception + 0.12 * posMatch;
    }

    if (this.contingencies.velocityActuator > 0.72) {
      this.bodyFeatures.add('Motor Thruster (Self)');
    }
    if (this.contingencies.positionProprioception > 0.72) {
      this.bodyFeatures.add('Proprioceptive Position (Self)');
    }

    this.agencyConfidence = (this.contingencies.velocityActuator + this.contingencies.positionProprioception) / 2;
  }

  isSelf(featureId) {
    return this.bodyFeatures.has(featureId);
  }
}
