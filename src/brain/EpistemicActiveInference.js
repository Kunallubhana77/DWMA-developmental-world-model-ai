/**
 * DWMA Epistemic Active Inference Engine
 * Replaces heuristic jitter with formal uncertainty reduction (Information Gain).
 * G(a) = argmax_i [ Var(Belief_i) - Var(Belief_i | Action) ]
 */
export class EpistemicActiveInference {
  constructor() {
    this.entityUncertainties = new Map(); // entityId -> variance (float)
    this.activeHypothesis = null;
    this.totalInformationGain = 0.0;
  }

  registerEntity(entity) {
    if (!this.entityUncertainties.has(entity.id)) {
      // Prior epistemic entropy is high for newly sighted entities
      this.entityUncertainties.set(entity.id, {
        id: entity.id,
        name: entity.name,
        initialVariance: 25.0,
        variance: 25.0, // High initial variance
        probes: 0,
        estimatedMass: 1.0
      });
    }
  }

  selectMostInformativeEntity(entities) {
    for (const ent of entities) {
      this.registerEntity(ent);
    }

    // Pick entity with the MAXIMUM unresolved variance
    let maxVar = -1;
    let mostUncertain = null;

    for (const ent of entities) {
      const u = this.entityUncertainties.get(ent.id);
      if (u && u.variance > maxVar) {
        maxVar = u.variance;
        mostUncertain = ent;
      }
    }

    return mostUncertain;
  }

  recordProbeResult(entity, force, displacement) {
    const u = this.entityUncertainties.get(entity.id);
    if (!u) return 0;

    const oldVariance = u.variance;
    u.probes++;

    // Compute empirical SNR and collapse variance
    const inferredMass = force / Math.max(0.01, displacement);
    u.estimatedMass = 0.7 * u.estimatedMass + 0.3 * inferredMass;

    const snr = Math.min(10.0, displacement / Math.max(0.1, force));
    u.variance = u.variance / (1.0 + snr * 0.8);

    // Differential Gaussian entropy change for this single intervention:
    // Delta H = 0.5 * ln(sigma^2_prior / sigma^2_post) in nats
    const infoGain = 0.5 * Math.max(0, Math.log(oldVariance / Math.max(0.001, u.variance)));

    // Recompute total bounded system information gain across all registered entities:
    // I_total = sum_i [ 0.5 * ln(sigma^2_{i, 0} / sigma^2_{i, current}) ]
    let systemInfoGain = 0.0;
    for (const entry of this.entityUncertainties.values()) {
      const initialVar = entry.initialVariance || 25.0;
      systemInfoGain += 0.5 * Math.max(0, Math.log(initialVar / Math.max(0.001, entry.variance)));
    }
    this.totalInformationGain = systemInfoGain;

    return {
      infoGain,
      oldVariance,
      newVariance: u.variance,
      estimatedMass: u.estimatedMass,
      totalSystemInfoGain: this.totalInformationGain
    };
  }
}
