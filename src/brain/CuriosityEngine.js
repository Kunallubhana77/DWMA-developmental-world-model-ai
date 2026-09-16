/**
 * DWMA Epistemic Curiosity Engine
 * Drives exploratory behavior through intrinsic motivation and surprise.
 */
export class CuriosityEngine {
  constructor() {
    this.surpriseHistory = [];
    this.explorationGrid = new Map(); // "x,y" -> count
    this.curiosityLevel = 1.0;
    this.targetFocus = null;
    this.stuckCounter = 0;
    this.isEscaping = false;
    this.bestEscapeRay = null;
  }

  computeIntrinsicReward(predictionError) {
    // Non-linear surprise mapping
    const surprise = Math.tanh(predictionError * 1.8);
    this.surpriseHistory.push(surprise);
    if (this.surpriseHistory.length > 100) this.surpriseHistory.shift();

    // Running curiosity metric
    this.curiosityLevel = 0.9 * this.curiosityLevel + 0.1 * surprise;
    return surprise;
  }

  recordSectorVisit(x, y) {
    const sectorX = Math.floor(x / 40);
    const sectorY = Math.floor(y / 40);
    const key = `${sectorX},${sectorY}`;
    const count = (this.explorationGrid.get(key) || 0) + 1;
    this.explorationGrid.set(key, count);
    return count;
  }

  recordSensoryFeedback(rays, actualDisplacement, actionMag) {
    if (actionMag > 0.2 && actualDisplacement < 0.25) {
      this.stuckCounter++;
      if (this.stuckCounter > 6) {
        this.isEscaping = true;
      }
    } else if (actualDisplacement > 0.8) {
      this.stuckCounter = Math.max(0, this.stuckCounter - 2);
      if (this.stuckCounter === 0) {
        this.isEscaping = false;
      }
    }

    // Find the ray with the maximum clear distance (The Escape Gap)
    let maxDist = -1;
    let gapRay = null;
    if (rays && rays.length > 0) {
      for (const r of rays) {
        if (r.distance > maxDist) {
          maxDist = r.distance;
          gapRay = r;
        }
      }
    }
    this.bestEscapeRay = gapRay;
  }

  /**
   * Action selection balancing novelty search, targeted object interaction,
   * and tangential gap-seeking escape behavior when physically blocked.
   */
  selectCuriousAction(candidateActions, currentPos, entities, customBeacon = null) {
    // 1. ESCAPE INTELLIGENCE: When blocked / trapped
    if (this.isEscaping && this.bestEscapeRay) {
      // If we found a ray with open space (gap > 40px)
      if (this.bestEscapeRay.distance > 35) {
        const angle = this.bestEscapeRay.angle;
        return {
          x: Math.cos(angle) * 1.0,
          y: Math.sin(angle) * 1.0,
          intent: 'Gap Escape / Squeeze'
        };
      }

      // If tightly surrounded, slide tangentially (perpendicular contour search)
      const tangentAngle = (this.bestEscapeRay.angle + Math.PI / 2) + (Math.random() - 0.5) * 0.4;
      return {
        x: Math.cos(tangentAngle) * 0.95,
        y: Math.sin(tangentAngle) * 0.95,
        intent: 'Tangential Wall-Slide'
      };
    }

    // 2. Normal Curiosity & Beacon Navigation
    let bestAction = candidateActions[0];
    let highestScore = -Infinity;

    if (customBeacon) {
      const dx = customBeacon.x - currentPos.x;
      const dy = customBeacon.y - currentPos.y;
      const dist = Math.hypot(dx, dy);
      if (dist > 15) {
        return {
          x: (dx / dist) * 1.0,
          y: (dy / dist) * 1.0,
          intent: 'Beacon Nav'
        };
      }
    }

    for (const act of candidateActions) {
      const nextX = currentPos.x + act.x * 25;
      const nextY = currentPos.y + act.y * 25;

      const sectorX = Math.floor(nextX / 40);
      const sectorY = Math.floor(nextY / 40);
      const visits = this.explorationGrid.get(`${sectorX},${sectorY}`) || 0;
      const noveltyScore = 1.0 / (1.0 + visits * 0.15);

      let objectScore = 0;
      for (const ent of entities) {
        const d = Math.hypot(nextX - ent.x, nextY - ent.y);
        const interactions = ent.interactions || 0;

        // Habituation / Boredom Law:
        // As interactions on the same object increase, curiosity satiates and drops sharply.
        // After 6 touches, curiosity drops below zero (boredom / urge to explore elsewhere).
        let satiationFactor = 1.0;
        if (interactions > 5) {
          // Drops from 1.0 down to -0.6 (active desire to disengage and find another toy!)
          satiationFactor = Math.max(-0.6, 1.0 - (interactions - 5) * 0.25);
        }

        const noveltyWeight = Math.max(0.1, 2.5 / (1.0 + Math.sqrt(interactions)));
        const baseProximity = 25.0 / (d + 25.0);

        objectScore += satiationFactor * noveltyWeight * baseProximity;
      }

      // Stronger exploratory drive towards unvisited territory
      const jitter = (Math.random() - 0.5) * 0.4;
      const totalScore = noveltyScore * 2.2 + objectScore + jitter;

      if (totalScore > highestScore) {
        highestScore = totalScore;
        bestAction = { ...act, intent: objectScore > 0.5 ? 'Object Curiosity' : 'Novelty Search' };
      }
    }

    return bestAction;
  }
}
