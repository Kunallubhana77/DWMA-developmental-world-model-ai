/**
 * DWMA Real-time Metrics Chart
 * Plots dynamic Prediction Error & Surprise without external dependencies.
 */
export class MetricsChart {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
  }

  render(errorHistory, surpriseHistory) {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    ctx.clearRect(0, 0, w, h);

    // Chart grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
    ctx.lineWidth = 1;
    for (let y = 15; y < h; y += 25) {
      ctx.beginPath();
      ctx.moveTo(35, y);
      ctx.lineTo(w - 10, y);
      ctx.stroke();
    }

    if (!errorHistory || errorHistory.length < 2) {
      ctx.fillStyle = '#64748b';
      ctx.font = '11px JetBrains Mono, monospace';
      ctx.fillText('Accumulating sensory prediction stream...', 40, h / 2);
      return;
    }

    // Determine vertical scale
    const maxVal = Math.max(1.5, ...errorHistory.slice(-80));
    const paddingLeft = 35;
    const paddingBottom = 20;
    const chartW = w - paddingLeft - 10;
    const chartH = h - paddingBottom - 10;

    // Y-Axis labels
    ctx.fillStyle = '#64748b';
    ctx.font = '9px JetBrains Mono, monospace';
    ctx.textAlign = 'right';
    ctx.fillText(maxVal.toFixed(1), paddingLeft - 5, 15);
    ctx.fillText('0.0', paddingLeft - 5, chartH + 10);

    const history = errorHistory.slice(-100);
    const stepX = chartW / Math.max(1, history.length - 1);

    // 1. Draw Surprise / Curiosity area
    if (surpriseHistory && surpriseHistory.length > 1) {
      const sHist = surpriseHistory.slice(-100);
      ctx.beginPath();
      ctx.moveTo(paddingLeft, chartH + 10);
      sHist.forEach((val, i) => {
        const x = paddingLeft + i * stepX;
        const normY = Math.min(1.0, val / 1.0);
        const y = chartH + 10 - normY * chartH;
        ctx.lineTo(x, y);
      });
      ctx.lineTo(paddingLeft + (sHist.length - 1) * stepX, chartH + 10);
      ctx.closePath();
      ctx.fillStyle = 'rgba(234, 179, 8, 0.12)';
      ctx.fill();
    }

    // 2. Draw Prediction Error Line
    ctx.beginPath();
    history.forEach((err, i) => {
      const x = paddingLeft + i * stepX;
      const normY = Math.min(1.0, err / maxVal);
      const y = chartH + 10 - normY * chartH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Latest error badge
    const lastErr = history[history.length - 1];
    ctx.fillStyle = '#f43f5e';
    ctx.font = '10px JetBrains Mono, monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`Error: ${lastErr.toFixed(3)}`, w - 15, 18);
  }
}
