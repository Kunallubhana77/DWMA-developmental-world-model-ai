/**
 * DWMA World Renderer
 * High-performance 60 FPS Canvas visualizer for the simulated sandbox and sensory overlay.
 */
export class WorldRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
  }

  render(world, brain, currentTick) {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    ctx.clearRect(0, 0, w, h);

    // 1. Futuristic Arena Background Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1;
    const gridSize = 40;
    for (let x = 0; x <= w; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y <= h; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // 2. Curiosity Heatmap (Visited Sectors)
    for (const [key, count] of brain.curiosity.explorationGrid.entries()) {
      const [sx, sy] = key.split(',').map(Number);
      const intensity = Math.min(0.2, count * 0.015);
      ctx.fillStyle = `rgba(56, 189, 248, ${intensity})`;
      ctx.fillRect(sx * 40, sy * 40, 40, 40);
    }

    // 3. User Curiosity Beacon
    if (world.customBeacon) {
      const b = world.customBeacon;
      ctx.save();
      ctx.beginPath();
      ctx.arc(b.x, b.y, 18 + Math.sin(currentTick * 0.1) * 4, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(234, 179, 8, 0.8)';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.fillStyle = 'rgba(234, 179, 8, 0.2)';
      ctx.fill();
      ctx.fillStyle = '#fef08a';
      ctx.font = '10px JetBrains Mono, monospace';
      ctx.fillText('⚡ CURIOSITY BEACON', b.x - 45, b.y - 25);
      ctx.restore();
    }

    // 4. Physical Entities
    for (const ent of world.entities) {
      this.renderEntity(ctx, ent, brain);
    }

    // 4b. Active Symbolic Query Laser
    if (brain.lexicon && brain.lexicon.activeQueryTarget) {
      const qTarget = world.entities.find(e => e.id === brain.lexicon.activeQueryTarget);
      if (qTarget) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(world.agent.x, world.agent.y);
        ctx.lineTo(qTarget.x, qTarget.y);
        ctx.strokeStyle = '#fef08a';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([6, 6]);
        ctx.stroke();

        const midX = (world.agent.x + qTarget.x) / 2;
        const midY = (world.agent.y + qTarget.y) / 2;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.fillRect(midX - 75, midY - 12, 150, 22);
        ctx.fillStyle = '#fef08a';
        ctx.font = 'bold 10px JetBrains Mono, monospace';
        ctx.textAlign = 'center';
        ctx.fillText('🔍 SYMBOL RESOLVED', midX, midY + 3);
        ctx.restore();
      }
    }

    // 5. Agent Sensory Whiskers (Perception Rays)
    if (brain.sensory && brain.sensory.rays) {
      for (const ray of brain.sensory.rays) {
        ctx.beginPath();
        ctx.moveTo(world.agent.x, world.agent.y);
        ctx.lineTo(ray.endPoint.x, ray.endPoint.y);

        const isEscapeGap = brain.curiosity.isEscaping && brain.curiosity.bestEscapeRay && ray.angle === brain.curiosity.bestEscapeRay.angle && ray.distance > 30;

        if (isEscapeGap) {
          ctx.strokeStyle = '#10b981';
          ctx.lineWidth = 2.5;
        } else {
          const alpha = 0.15 + (1.0 - ray.normalizedDist) * 0.65;
          ctx.strokeStyle = ray.hitEntity ? `rgba(244, 63, 94, ${alpha})` : `rgba(56, 189, 248, ${alpha * 0.5})`;
          ctx.lineWidth = ray.hitEntity ? 1.5 : 1;
        }
        ctx.stroke();

        // Ray tip contact point
        if (isEscapeGap) {
          ctx.fillStyle = '#10b981';
          ctx.beginPath();
          ctx.arc(ray.endPoint.x, ray.endPoint.y, 4, 0, Math.PI * 2);
          ctx.fill();
        } else if (ray.hitEntity) {
          ctx.fillStyle = '#f43f5e';
          ctx.beginPath();
          ctx.arc(ray.endPoint.x, ray.endPoint.y, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    // 6. Stage 3 Mental Simulation / Imagined Trajectory
    if (brain.imaginedTrajectory && brain.imaginedTrajectory.length > 0) {
      ctx.save();
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.6)';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(world.agent.x, world.agent.y);
      for (const step of brain.imaginedTrajectory) {
        ctx.lineTo(step.x, step.y);
      }
      ctx.stroke();

      // Trajectory future nodes
      ctx.fillStyle = '#c084fc';
      for (const step of brain.imaginedTrajectory) {
        ctx.beginPath();
        ctx.arc(step.x, step.y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    // 7. Internal Forward Prediction Vector (Where the brain expects to be)
    if (brain.lastPrediction) {
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(world.agent.x, world.agent.y);
      ctx.lineTo(brain.lastPrediction.x, brain.lastPrediction.y);
      ctx.strokeStyle = 'rgba(234, 179, 8, 0.9)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Prediction Target Ghost
      ctx.beginPath();
      ctx.arc(brain.lastPrediction.x, brain.lastPrediction.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(234, 179, 8, 0.5)';
      ctx.fill();
      ctx.restore();
    }

    // 8. The Embodied Agent (DWMA Brain)
    this.renderAgent(ctx, world.agent, brain, currentTick);
  }

  renderEntity(ctx, ent, brain) {
    ctx.save();
    ctx.translate(ent.x, ent.y);

    const profile = brain.causalGraph.entityProfiles.get(ent.id);
    const concept = profile ? profile.concept : 'Undiscovered';

    // Entity Body Glow
    ctx.shadowBlur = 10;
    ctx.shadowColor = ent.color;

    ctx.fillStyle = ent.color;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 1.5;

    if (ent.shape === 'box') {
      const half = ent.radius;
      ctx.fillRect(-half, -half, half * 2, half * 2);
      ctx.strokeRect(-half, -half, half * 2, half * 2);
    } else if (ent.shape === 'pillar') {
      ctx.beginPath();
      ctx.arc(0, 0, ent.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
      ctx.beginPath();
      ctx.arc(0, 0, ent.radius * 0.5, 0, Math.PI * 2);
      ctx.fill();
    } else if (ent.shape === 'diamond') {
      ctx.beginPath();
      ctx.moveTo(0, -ent.radius);
      ctx.lineTo(ent.radius, 0);
      ctx.lineTo(0, ent.radius);
      ctx.lineTo(-ent.radius, 0);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    } else {
      ctx.beginPath();
      ctx.arc(0, 0, ent.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    ctx.shadowBlur = 0;

    // Entity Label & Inferred Concept Tag
    ctx.fillStyle = '#f8fafc';
    ctx.font = '11px Outfit, sans-serif';
    ctx.textAlign = 'center';

    const groundedWord = brain.lexicon ? brain.lexicon.getSymbolForEntity(ent.id) : null;
    if (groundedWord) {
      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 11px JetBrains Mono, monospace';
      ctx.fillText(`🏷️ "${groundedWord}"`, 0, -ent.radius - 18);
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '10px Outfit, sans-serif';
      ctx.fillText(ent.name, 0, -ent.radius - 6);
    } else {
      ctx.fillText(ent.name, 0, -ent.radius - 8);
    }

    if (profile && profile.concept !== 'Undiscovered Entity') {
      ctx.fillStyle = '#38bdf8';
      ctx.font = '9px JetBrains Mono, monospace';
      ctx.fillText(`${profile.symbol} ${profile.concept}`, 0, ent.radius + 14);
    }

    // Active Query Highlight Aura
    if (brain.lexicon && brain.lexicon.activeQueryTarget === ent.id) {
      ctx.beginPath();
      ctx.arc(0, 0, ent.radius + 10, 0, Math.PI * 2);
      ctx.strokeStyle = '#fef08a';
      ctx.lineWidth = 2.5;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
    }

    ctx.restore();
  }

  renderAgent(ctx, agent, brain, tick) {
    ctx.save();
    ctx.translate(agent.x, agent.y);
    ctx.rotate(agent.heading);

    // Baby Brain Aura
    const pulse = Math.sin(tick * 0.08) * 3;
    const stageColors = ['#38bdf8', '#10b981', '#f59e0b', '#a855f7'];
    const activeColor = stageColors[brain.stage] || '#38bdf8';

    ctx.shadowBlur = 16;
    ctx.shadowColor = activeColor;

    // Outer Hull
    ctx.fillStyle = '#0f172a';
    ctx.strokeStyle = activeColor;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(0, 0, agent.radius + pulse, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Inner Glowing Core (The Brain)
    ctx.fillStyle = activeColor;
    ctx.beginPath();
    ctx.arc(0, 0, 7, 0, Math.PI * 2);
    ctx.fill();

    // Orientation Indicator Nose
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(agent.radius + 4, 0);
    ctx.lineTo(agent.radius - 3, -4);
    ctx.lineTo(agent.radius - 3, 4);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }
}
