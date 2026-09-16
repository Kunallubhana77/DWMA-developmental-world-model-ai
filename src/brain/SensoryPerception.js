/**
 * DWMA Sensory Perception Layer
 * Encodes ego-centric raycasts, tactile collisions, and proprioception.
 */
export class SensoryPerception {
  constructor(numRays = 12, rayLength = 90) {
    this.numRays = numRays;
    this.rayLength = rayLength;
    this.rays = [];
    this.tactileContact = null;
  }

  processSensors(agent, entities, arenaBounds) {
    const readings = [];
    this.rays = [];
    this.tactileContact = null;

    const angleStep = (Math.PI * 2) / this.numRays;

    for (let i = 0; i < this.numRays; i++) {
      const angle = agent.heading + i * angleStep;
      const rayEnd = {
        x: agent.x + Math.cos(angle) * this.rayLength,
        y: agent.y + Math.sin(angle) * this.rayLength
      };

      let minHitDist = this.rayLength;
      let hitEntity = null;

      // Check arena borders
      if (rayEnd.x < 0) minHitDist = Math.min(minHitDist, agent.x / Math.abs(Math.cos(angle) || 0.001));
      if (rayEnd.x > arenaBounds.width) minHitDist = Math.min(minHitDist, (arenaBounds.width - agent.x) / (Math.cos(angle) || 0.001));
      if (rayEnd.y < 0) minHitDist = Math.min(minHitDist, agent.y / Math.abs(Math.sin(angle) || 0.001));
      if (rayEnd.y > arenaBounds.height) minHitDist = Math.min(minHitDist, (arenaBounds.height - agent.y) / (Math.sin(angle) || 0.001));

      // Check objects
      for (const ent of entities) {
        const d = Math.hypot(ent.x - agent.x, ent.y - agent.y);
        const radiusSum = (agent.radius || 14) + (ent.radius || 16);
        if (d < radiusSum + 5) {
          this.tactileContact = ent;
        }

        // Ray intersection approximation
        const dx = ent.x - agent.x;
        const dy = ent.y - agent.y;
        const objAngle = Math.atan2(dy, dx);
        let angleDiff = Math.abs(angle - objAngle);
        while (angleDiff > Math.PI) angleDiff = Math.PI * 2 - angleDiff;

        if (angleDiff < 0.25 && d < this.rayLength) {
          if (d < minHitDist) {
            minHitDist = d;
            hitEntity = ent;
          }
        }
      }

      const clampedDist = Math.max(0, Math.min(this.rayLength, minHitDist));
      const actualEnd = {
        x: agent.x + Math.cos(angle) * clampedDist,
        y: agent.y + Math.sin(angle) * clampedDist
      };

      this.rays.push({
        angle,
        distance: clampedDist,
        normalizedDist: clampedDist / this.rayLength,
        endPoint: actualEnd,
        hitEntity
      });

      readings.push(clampedDist / this.rayLength);
    }

    return {
      readings,
      tactileContact: this.tactileContact,
      pos: { x: agent.x, y: agent.y },
      vel: { vx: agent.vx, vy: agent.vy },
      speed: Math.hypot(agent.vx, agent.vy)
    };
  }
}
