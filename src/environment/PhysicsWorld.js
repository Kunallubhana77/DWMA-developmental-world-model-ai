/**
 * DWMA Continuous 2D Physics Environment
 * Simulates physical dynamics, rigid interactions, damping, and boundaries.
 */
export class PhysicsWorld {
  constructor(width = 800, height = 550) {
    this.width = width;
    this.height = height;

    // Embodied Baby AI Agent
    this.agent = {
      x: width / 2,
      y: height / 2,
      vx: 0,
      vy: 0,
      radius: 14,
      mass: 2.0,
      heading: 0,
      accelFactor: 0.85,
      friction: 0.88
    };

    this.entities = [];
    this.customBeacon = null;
    this.resetScenario();
  }

  resetScenario() {
    this.agent.x = this.width / 2;
    this.agent.y = this.height / 2;
    this.agent.vx = 0;
    this.agent.vy = 0;
    this.agent.heading = 0;
    this.agent.friction = 0.88;
    this.agent.accelFactor = 0.85;
    this.customBeacon = null;
    this.currentWorldName = 'World A (Earth Sandbox)';

    this.entities = [
      {
        id: 'box_light',
        name: 'Light Toy Box',
        x: this.width / 2 - 130,
        y: this.height / 2 - 90,
        vx: 0,
        vy: 0,
        radius: 18,
        mass: 1.2,
        friction: 0.85,
        color: '#38bdf8', // Cyan
        shape: 'box',
        interactions: 0
      },
      {
        id: 'heavy_crate',
        name: 'Heavy Steel Crate',
        x: this.width / 2 + 150,
        y: this.height / 2 - 80,
        vx: 0,
        vy: 0,
        radius: 24,
        mass: 22.0,
        friction: 0.65,
        color: '#94a3b8', // Slate
        shape: 'box',
        interactions: 0
      },
      {
        id: 'bouncy_ball',
        name: 'Elastic Ball',
        x: this.width / 2 + 100,
        y: this.height / 2 + 130,
        vx: 0,
        vy: 0,
        radius: 16,
        mass: 0.8,
        friction: 0.94,
        color: '#f59e0b', // Amber
        shape: 'circle',
        interactions: 0
      },
      {
        id: 'barrier_wall',
        name: 'Static Wall',
        x: this.width / 2 - 150,
        y: this.height / 2 + 120,
        vx: 0,
        vy: 0,
        radius: 22,
        mass: 9999.0, // Fixed
        friction: 0.0,
        color: '#ef4444', // Red
        shape: 'pillar',
        interactions: 0
      },
      {
        id: 'energy_node',
        name: 'Resonance Crystal',
        x: this.width / 2,
        y: this.height / 2 - 160,
        vx: 0,
        vy: 0,
        radius: 15,
        mass: 2.5,
        friction: 0.82,
        color: '#10b981', // Emerald
        shape: 'diamond',
        interactions: 0
      }
    ];
  }

  spawnEntity(x, y, type = 'dynamic') {
    const id = `custom_${Date.now().toString(36)}`;
    const presets = {
      light: { name: 'New Light Box', mass: 1.0, color: '#60a5fa', radius: 17, shape: 'box' },
      heavy: { name: 'New Boulder', mass: 20.0, color: '#64748b', radius: 24, shape: 'circle' },
      bouncy: { name: 'New Elastic Sphere', mass: 0.7, color: '#f59e0b', radius: 15, shape: 'circle' },
      barrier: { name: 'New Concrete Pillar', mass: 9999.0, color: '#f43f5e', radius: 20, shape: 'pillar' }
    };
    const preset = presets[type] || presets.light;
    this.entities.push({
      id,
      name: preset.name,
      x: Math.max(30, Math.min(this.width - 30, x)),
      y: Math.max(30, Math.min(this.height - 30, y)),
      vx: 0,
      vy: 0,
      radius: preset.radius,
      mass: preset.mass,
      friction: 0.85,
      color: preset.color,
      shape: preset.shape,
      interactions: 0
    });
  }

  step(motorAction) {
    const a = this.agent;

    // 1. Apply motor force to agent
    const fx = motorAction.x * a.accelFactor;
    const fy = motorAction.y * a.accelFactor;

    a.vx = (a.vx + fx) * a.friction;
    a.vy = (a.vy + fy) * a.friction;

    // Update heading smoothly towards movement
    if (Math.hypot(a.vx, a.vy) > 0.05) {
      const targetHeading = Math.atan2(a.vy, a.vx);
      a.heading = a.heading * 0.8 + targetHeading * 0.2;
    }

    a.x += a.vx;
    a.y += a.vy;

    // 2. Arena Boundary constraints for Agent
    const margin = a.radius + 2;
    if (a.x < margin) { a.x = margin; a.vx *= -0.5; }
    if (a.x > this.width - margin) { a.x = this.width - margin; a.vx *= -0.5; }
    if (a.y < margin) { a.y = margin; a.vy *= -0.5; }
    if (a.y > this.height - margin) { a.y = this.height - margin; a.vy *= -0.5; }

    let collidedEntity = null;
    let displacement = 0;
    const entityCollisions = [];

    // 3. Entity updates & Agent-Entity Collisions
    for (let i = 0; i < this.entities.length; i++) {
      const ent = this.entities[i];

      // Entity physics step
      if (ent.mass < 9000) {
        ent.x += ent.vx;
        ent.y += ent.vy;
        ent.vx *= ent.friction;
        ent.vy *= ent.friction;

        // Entity bounds
        const entMargin = ent.radius + 2;
        if (ent.x < entMargin) { ent.x = entMargin; ent.vx *= -0.6; }
        if (ent.x > this.width - entMargin) { ent.x = this.width - entMargin; ent.vx *= -0.6; }
        if (ent.y < entMargin) { ent.y = entMargin; ent.vy *= -0.6; }
        if (ent.y > this.height - entMargin) { ent.y = this.height - entMargin; ent.vy *= -0.6; }
      }

      // Check collision with agent
      const dx = ent.x - a.x;
      const dy = ent.y - a.y;
      const dist = Math.hypot(dx, dy);
      const minDist = a.radius + ent.radius;

      if (dist < minDist && dist > 0.001) {
        const nx = dx / dist;
        const ny = dy / dist;
        const overlap = minDist - dist;

        if (ent.mass >= 9000) {
          a.x -= nx * overlap;
          a.y -= ny * overlap;
          a.vx *= -0.3;
          a.vy *= -0.3;
          displacement = 0.0;
        } else {
          const pushRatio = a.mass / (a.mass + ent.mass);
          ent.x += nx * overlap * pushRatio;
          ent.y += ny * overlap * pushRatio;
          a.x -= nx * overlap * (1 - pushRatio);
          a.y -= ny * overlap * (1 - pushRatio);

          const impulse = (Math.hypot(a.vx, a.vy) + 0.4) * (a.mass / ent.mass);
          ent.vx += nx * impulse * 1.5;
          ent.vy += ny * impulse * 1.5;
          displacement = Math.hypot(ent.vx, ent.vy);
        }

        ent.interactions = (ent.interactions || 0) + 1;
        collidedEntity = ent;
      }

      // 4. Object-to-Object (Tool) Collisions
      for (let j = i + 1; j < this.entities.length; j++) {
        const other = this.entities[j];
        const odx = other.x - ent.x;
        const ody = other.y - ent.y;
        const odist = Math.hypot(odx, ody);
        const ominDist = ent.radius + other.radius;

        if (odist < ominDist && odist > 0.001) {
          const onx = odx / odist;
          const ony = ody / odist;
          const ooverlap = ominDist - odist;

          if (ent.mass < 9000 && other.mass < 9000) {
            // Both movable: elastic/momentum transfer
            const totalM = ent.mass + other.mass;
            ent.x -= onx * ooverlap * 0.5;
            ent.y -= ony * ooverlap * 0.5;
            other.x += onx * ooverlap * 0.5;
            other.y += ony * ooverlap * 0.5;

            const impulse = Math.hypot(ent.vx - other.vx, ent.vy - other.vy);
            ent.vx -= onx * (impulse * 0.6);
            ent.vy -= ony * (impulse * 0.6);
            other.vx += onx * (impulse * 0.6);
            other.vy += ony * (impulse * 0.6);

            entityCollisions.push({
              source: ent,
              target: other,
              impulse,
              x: (ent.x + other.x) / 2,
              y: (ent.y + other.y) / 2
            });
          } else if (ent.mass < 9000 && other.mass >= 9000) {
            // ent hits static barrier
            ent.x -= onx * ooverlap;
            ent.y -= ony * ooverlap;
            ent.vx *= -0.5;
            ent.vy *= -0.5;
          } else if (other.mass < 9000 && ent.mass >= 9000) {
            other.x += onx * ooverlap;
            other.y += ony * ooverlap;
            other.vx *= -0.5;
            other.vy *= -0.5;
          }
        }
      }
    }

    return {
      agentState: { x: a.x, y: a.y, vx: a.vx, vy: a.vy },
      collidedEntity,
      displacement,
      entityCollisions
    };
  }

  setupToolChallenge() {
    this.agent.x = 180;
    this.agent.y = 260;
    this.agent.vx = 0;
    this.agent.vy = 0;
    this.agent.heading = 0;
    this.customBeacon = null;

    // Tool challenge layout:
    // Immovable barrier wall with narrow slit
    // Movable Toy Box (tool) in front of slit
    // Target Resonance Crystal behind slit
    this.entities = [
      // Tool
      {
        id: 'box_tool',
        name: 'Projectile Tool (Box)',
        x: 320,
        y: 260,
        vx: 0,
        vy: 0,
        radius: 16,
        mass: 1.0,
        friction: 0.90,
        color: '#38bdf8',
        shape: 'box',
        interactions: 0
      },
      // Target Crystal
      {
        id: 'crystal_target',
        name: 'Target Crystal',
        x: 600,
        y: 260,
        vx: 0,
        vy: 0,
        radius: 18,
        mass: 1.5,
        friction: 0.85,
        color: '#10b981',
        shape: 'diamond',
        interactions: 0
      },
      // Top wall section
      {
        id: 'wall_top',
        name: 'Slit Barrier Top',
        x: 460,
        y: 130,
        vx: 0,
        vy: 0,
        radius: 28,
        mass: 9999.0,
        friction: 0.0,
        color: '#ef4444',
        shape: 'pillar',
        interactions: 0
      },
      // Bottom wall section
      {
        id: 'wall_bottom',
        name: 'Slit Barrier Bottom',
        x: 460,
        y: 390,
        vx: 0,
        vy: 0,
        radius: 28,
        mass: 9999.0,
        friction: 0.0,
        color: '#ef4444',
        shape: 'pillar',
        interactions: 0
      }
    ];
  }
}
