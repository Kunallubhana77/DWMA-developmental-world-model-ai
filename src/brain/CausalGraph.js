/**
 * DWMA Causal Graph & Emergent Concept Induction
 * Maps physical observations into causal rules and proto-concepts.
 * Neuro-symbolic abstraction without Large Language Models.
 */
export class CausalGraph {
  constructor() {
    this.entityProfiles = new Map(); // entityId -> { interactions, totalDisp, avgMobility, elasticity, concept, symbol }
    this.causalEdges = []; // { id, rule, source, target, confidence, count, effectDescription }
    this.conceptRegistry = new Map(); // conceptName -> count
    this.cognitiveLogs = [];
  }

  logThought(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    this.cognitiveLogs.unshift({ timestamp, message, type });
    if (this.cognitiveLogs.length > 50) this.cognitiveLogs.pop();
  }

  recordInteraction(entity, action, displacement, force) {
    const entityId = entity.id;
    if (!this.entityProfiles.has(entityId)) {
      this.entityProfiles.set(entityId, {
        id: entityId,
        name: entity.name || `Entity_${entityId}`,
        color: entity.color,
        interactions: 0,
        totalDisp: 0,
        avgMobility: 0,
        concept: 'Undiscovered Entity',
        symbol: '?',
        elasticity: entity.elasticity || 0.5
      });
      this.logThought(`Discovered new physical entity: [${entity.name || entityId}]. Sensor registration complete.`, 'discovery');
    }

    const p = this.entityProfiles.get(entityId);
    p.interactions++;
    p.totalDisp += displacement;
    p.avgMobility = p.totalDisp / p.interactions;

    // Emergent Concept Induction (Unsupervised physical classification)
    let previousConcept = p.concept;
    if (p.interactions >= 2) {
      if (p.avgMobility < 0.1) {
        p.concept = 'Immovable Static Barrier';
        p.symbol = '🧱';
      } else if (p.avgMobility > 10.0) {
        p.concept = 'Ultra-Lightweight Body';
        p.symbol = '🪶';
      } else if (p.avgMobility > 3.0) {
        p.concept = 'Movable Dynamic Object';
        p.symbol = '📦';
      } else {
        p.concept = 'Heavy Resistive Mass';
        p.symbol = '🪨';
      }

      if (previousConcept !== p.concept) {
        this.logThought(`Hypothesis updated: ${p.name} categorized as "${p.concept}" based on mobility ~ ${p.avgMobility.toFixed(2)}px`, 'concept');
      }
    }

    // Causal Rule Generation
    const ruleId = `Push_${entityId}`;
    let edge = this.causalEdges.find(e => e.id === ruleId);
    if (!edge) {
      edge = {
        id: ruleId,
        source: 'Motor Thruster (Self)',
        target: p.concept,
        action: 'Push / Impinge',
        effectDescription: `Displacement ~ ${displacement.toFixed(1)}px`,
        confidence: 0.55,
        count: 1
      };
      this.causalEdges.push(edge);
      this.logThought(`Formed causal link: [Self Action] -> [${p.concept}] results in physical displacement`, 'causal');
    } else {
      edge.count++;
      edge.target = p.concept;
      edge.confidence = Math.min(0.99, edge.confidence + 0.05);
      edge.effectDescription = `Displacement ~ ${p.avgMobility.toFixed(1)}px`;
    }

    return p;
  }

  recordObjectToObjectCollision(sourceEnt, targetEnt, impulse) {
    const srcProfile = this.entityProfiles.get(sourceEnt.id);
    const tgtProfile = this.entityProfiles.get(targetEnt.id);

    if (srcProfile && srcProfile.interactions > 0) {
      srcProfile.concept = 'Dynamic Tool / Projectile';
      srcProfile.symbol = '🔨';
    }

    const ruleId = `Tool_${sourceEnt.id}_hits_${targetEnt.id}`;
    let edge = this.causalEdges.find(e => e.id === ruleId);

    if (!edge) {
      edge = {
        id: ruleId,
        source: sourceEnt.name || sourceEnt.id,
        target: targetEnt.name || targetEnt.id,
        action: 'Impulse Transfer (Tool Use)',
        effectDescription: `Impulse ~ ${impulse.toFixed(1)}px`,
        confidence: 0.65,
        count: 1,
        isIndirect: true
      };
      this.causalEdges.push(edge);
      this.logThought(`Indirect Causality Discovered: [${sourceEnt.name}] transferred impulse to [${targetEnt.name}]! Tool-Use relationship established.`, 'causal');
    } else {
      edge.count++;
      edge.confidence = Math.min(0.99, edge.confidence + 0.08);
      edge.effectDescription = `Impulse ~ ${impulse.toFixed(1)}px`;
    }
  }
}
