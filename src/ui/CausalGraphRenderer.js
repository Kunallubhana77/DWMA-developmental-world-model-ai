/**
 * DWMA Causal Graph Visualizer
 * Force-directed neuro-symbolic causal network showing discovered entities,
 * agency links, and physical laws inferred by the baby AI.
 */
export class CausalGraphRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
  }

  render(brain, tick) {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    ctx.clearRect(0, 0, w, h);

    // Build Node List dynamically
    const nodes = [];
    const nodeMap = new Map();

    // 1. Central Self Node (Agent Ego)
    const selfNode = {
      id: 'self',
      label: 'SELF (Ego Agency)',
      color: '#38bdf8',
      x: w / 2,
      y: h / 2,
      radius: 22,
      symbol: '🧠'
    };
    nodes.push(selfNode);
    nodeMap.set('self', selfNode);

    // 2. Discovered Entity Concept Nodes
    const profiles = Array.from(brain.causalGraph.entityProfiles.values());
    const count = profiles.length;
    const radiusRing = Math.min(w, h) * 0.38;

    profiles.forEach((p, idx) => {
      const angle = (idx / Math.max(1, count)) * Math.PI * 2 + tick * 0.002;
      const node = {
        id: p.id,
        label: p.concept,
        name: p.name,
        color: p.color || '#94a3b8',
        x: w / 2 + Math.cos(angle) * radiusRing,
        y: h / 2 + Math.sin(angle) * radiusRing,
        radius: 18,
        symbol: p.symbol || '📦',
        interactions: p.interactions
      };
      nodes.push(node);
      nodeMap.set(p.id, node);
    });

    // 3. Draw Causal Edges
    for (const edge of brain.causalGraph.causalEdges) {
      let fromNode = selfNode;
      let toNode = null;

      if (edge.isIndirect) {
        // Tool-to-target edge
        fromNode = nodes.find(n => edge.source && (edge.source.includes(n.name) || edge.source.includes(n.id)));
        toNode = nodes.find(n => edge.target && (edge.target.includes(n.name) || edge.target.includes(n.id)));
      } else {
        toNode = nodes.find(n => edge.id.includes(n.id));
      }

      if (fromNode && toNode) {
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(fromNode.x, fromNode.y);
        ctx.lineTo(toNode.x, toNode.y);

        const confidence = edge.confidence || 0.5;
        if (edge.isIndirect) {
          ctx.strokeStyle = `rgba(245, 158, 11, ${0.4 + confidence * 0.5})`;
          ctx.setLineDash([4, 4]);
          ctx.lineWidth = 2.5;
        } else {
          ctx.strokeStyle = `rgba(56, 189, 248, ${0.3 + confidence * 0.6})`;
          ctx.lineWidth = 1.5 + confidence * 2.5;
        }
        ctx.stroke();

        // Flow particle along edge
        const t = (tick * 0.02 + edge.count * 0.1) % 1.0;
        const px = fromNode.x + (toNode.x - fromNode.x) * t;
        const py = fromNode.y + (toNode.y - fromNode.y) * t;
        ctx.fillStyle = edge.isIndirect ? '#f59e0b' : '#fef08a';
        ctx.beginPath();
        ctx.arc(px, py, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Edge label (Causal relationship)
        const midX = (fromNode.x + toNode.x) / 2;
        const midY = (fromNode.y + toNode.y) / 2;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.fillRect(midX - 45, midY - 10, 90, 18);
        ctx.fillStyle = edge.isIndirect ? '#f59e0b' : '#38bdf8';
        ctx.font = '9px JetBrains Mono, monospace';
        ctx.textAlign = 'center';
        const label = edge.isIndirect ? `TOOL (${edge.count}x)` : `P=${(confidence * 100).toFixed(0)}%`;
        ctx.fillText(label, midX, midY + 3);

        ctx.restore();
      }
    }

    // 4. Draw Nodes
    for (const node of nodes) {
      ctx.save();
      ctx.shadowBlur = 12;
      ctx.shadowColor = node.color;

      // Node background
      ctx.fillStyle = '#0f172a';
      ctx.strokeStyle = node.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.shadowBlur = 0;

      // Node Icon / Symbol
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.symbol, node.x, node.y);

      // Node Labels
      ctx.font = '10px Outfit, sans-serif';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText(node.label, node.x, node.y + node.radius + 12);

      if (node.name) {
        ctx.font = '8px JetBrains Mono, monospace';
        ctx.fillStyle = '#94a3b8';
        ctx.fillText(node.name, node.x, node.y + node.radius + 23);
      }

      ctx.restore();
    }
  }
}
