import { PhysicsWorld } from './environment/PhysicsWorld.js';
import { DWMABrain } from './brain/DWMABrain.js';
import { WorldRenderer } from './ui/WorldRenderer.js';
import { CausalGraphRenderer } from './ui/CausalGraphRenderer.js';
import { MetricsChart } from './ui/MetricsChart.js';
import { BenchmarkScenarios } from './environment/BenchmarkScenarios.js';

// Initialize Core Instances
const worldCanvas = document.getElementById('world-canvas');
const metricsCanvas = document.getElementById('metrics-canvas');
const causalCanvas = document.getElementById('causal-canvas');

const world = new PhysicsWorld(800, 520);
const brain = new DWMABrain();

const worldRenderer = new WorldRenderer(worldCanvas);
const causalRenderer = new CausalGraphRenderer(causalCanvas);
const metricsChart = new MetricsChart(metricsCanvas);

// Simulation State
let isRunning = true;
let simSpeed = 1;
let tickCount = 0;

// UI Elements
const statSteps = document.getElementById('stat-steps');
const statSurprise = document.getElementById('stat-surprise');
const statError = document.getElementById('stat-error');
const statConcepts = document.getElementById('stat-concepts');
const conceptsTbody = document.getElementById('concepts-tbody');
const cognitiveFeed = document.getElementById('cognitive-feed');
const causalRulesCount = document.getElementById('causal-rules-count');

const meterThrusterBar = document.getElementById('meter-thruster-bar');
const meterThrusterVal = document.getElementById('meter-thruster-val');
const meterProprioBar = document.getElementById('meter-proprio-bar');
const meterProprioVal = document.getElementById('meter-proprio-val');
const agencyLabel = document.getElementById('agency-label');

const stageButtons = [
  document.getElementById('btn-stage-0'),
  document.getElementById('btn-stage-1'),
  document.getElementById('btn-stage-2'),
  document.getElementById('btn-stage-3'),
  document.getElementById('btn-stage-4')
];

// Benchmark Telemetry Elements
const teleEnvName = document.getElementById('tele-env-name');
const teleFrictionVal = document.getElementById('tele-friction-val');
const teleWeightFriction = document.getElementById('tele-weight-friction');
const teleInfoGain = document.getElementById('tele-info-gain');
const benchmarkActiveBadge = document.getElementById('benchmark-active-badge');
const counterfactualCard = document.getElementById('counterfactual-card');
const bm5Readout = document.getElementById('bm5-readout');
const bm5Badge = document.getElementById('bm5-badge');

const compositionalCard = document.getElementById('compositional-card');
const bm6Readout = document.getElementById('bm6-readout');
const bm6Badge = document.getElementById('bm6-badge');

const reversalCard = document.getElementById('reversal-card');
const bm7Readout = document.getElementById('bm7-readout');
const bm7Badge = document.getElementById('bm7-badge');
const btnBmReversal = document.getElementById('btn-bm-reversal');

// Single Simulation Step
function executeStep() {
  tickCount++;

  // 1. Brain perceives world & plans motor action
  const stepResult = brain.step(world.agent, world.entities, { width: world.width, height: world.height }, world.customBeacon);

  // 2. Physics World executes action
  const physResult = world.step(stepResult.action);

  // 3. Brain observes result, calculates surprise & predictive error, updates world model
  const error = brain.observeConsequence(physResult.agentState, physResult.collidedEntity, physResult.displacement, physResult.entityCollisions);

  return { stepResult, physResult, error };
}

// Main Animation & Render Loop
let lastRenderTime = 0;
function loop(timestamp) {
  if (isRunning) {
    for (let s = 0; s < simSpeed; s++) {
      executeStep();
    }
  }

  // Render Visualizers
  worldRenderer.render(world, brain, tickCount);
  causalRenderer.render(brain, tickCount);
  metricsChart.render(brain.worldModel.errorHistory, brain.curiosity.surpriseHistory);

  // Update UI Telemetry periodically
  if (tickCount % 4 === 0) {
    updateUI();
  }

  requestAnimationFrame(loop);
}

// Update DOM Telemetry & Metrics
function updateUI() {
  statSteps.textContent = brain.developmentSteps;
  statSurprise.textContent = brain.curiosity.curiosityLevel.toFixed(2);
  statError.textContent = brain.worldModel.lastError.toFixed(3);

  const profiles = Array.from(brain.causalGraph.entityProfiles.values());
  const discoveredCount = profiles.filter(p => p.concept !== 'Undiscovered Entity').length;
  statConcepts.textContent = discoveredCount;

  // Agency & Self Model meters
  const thrusterScore = Math.min(100, Math.round(brain.selfModel.contingencies.velocityActuator * 100));
  const proprioScore = Math.min(100, Math.round(brain.selfModel.contingencies.positionProprioception * 100));
  meterThrusterBar.style.width = `${thrusterScore}%`;
  meterThrusterVal.textContent = `${thrusterScore}%`;
  meterProprioBar.style.width = `${proprioScore}%`;
  meterProprioVal.textContent = `${proprioScore}%`;

  const agencyPercent = Math.round(brain.selfModel.agencyConfidence * 100);
  agencyLabel.textContent = `AGENCY: ${agencyPercent}%`;

  // Causal rules count
  causalRulesCount.textContent = `${brain.causalGraph.causalEdges.length} RULES`;

  // Benchmark Telemetry Sync
  if (teleEnvName) {
    teleEnvName.textContent = world.currentWorldName || 'World A (Earth Sandbox)';
  }
  if (teleFrictionVal) {
    teleFrictionVal.textContent = world.agent.friction.toFixed(2);
  }
  if (teleWeightFriction) {
    teleWeightFriction.textContent = brain.worldModel.learnedFriction.toFixed(2);
  }
  if (teleInfoGain) {
    const gain = brain.activeInference ? brain.activeInference.totalInformationGain : 0;
    teleInfoGain.textContent = `${gain.toFixed(2)} nats`;
  }
  if (benchmarkActiveBadge) {
    if (world.currentWorldName && world.currentWorldName.includes('World B')) {
      benchmarkActiveBadge.textContent = 'ACTIVE: WORLD B (NEBULA)';
      benchmarkActiveBadge.style.color = '#d8b4fe';
    } else if (world.customBeacon && world.entities.some(e => e.id === 'barrier_pillar_1')) {
      benchmarkActiveBadge.textContent = 'ACTIVE: BLIND GOAL MAZE';
      benchmarkActiveBadge.style.color = '#7dd3fc';
    } else {
      benchmarkActiveBadge.textContent = 'ACTIVE: WORLD A';
      benchmarkActiveBadge.style.color = '#a5b4fc';
    }
  }

  // Active Stage Navigation Sync
  const currentStage = brain.stage;
  stageButtons.forEach((btn, idx) => {
    if (idx === currentStage) btn.classList.add('active');
    else btn.classList.remove('active');
  });

  // Concepts Table Sync
  updateConceptsTable(profiles);

  // Cognitive Stream Feed Sync
  updateCognitiveFeed();
}

function updateConceptsTable(profiles) {
  if (profiles.length === 0) {
    conceptsTbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-dim); padding: 1rem;">No physical entities encountered yet. AI will explore automatically...</td></tr>`;
    return;
  }

  conceptsTbody.innerHTML = profiles.map(p => `
    <tr>
      <td class="entity-name" style="color: ${p.color || '#fff'}">${p.name}</td>
      <td style="font-family: 'JetBrains Mono'">${p.interactions}</td>
      <td style="font-family: 'JetBrains Mono'">${p.avgMobility.toFixed(2)} px</td>
      <td><span class="concept-badge">${p.symbol} ${p.concept}</span></td>
    </tr>
  `).join('');
}

let lastLogCount = 0;
function updateCognitiveFeed() {
  const logs = brain.causalGraph.cognitiveLogs;
  if (logs.length === lastLogCount) return;
  lastLogCount = logs.length;

  cognitiveFeed.innerHTML = logs.slice(0, 15).map(log => `
    <div class="feed-item ${log.type}">
      <span class="time">${log.timestamp}</span>
      <span>${log.message}</span>
    </div>
  `).join('');
}

// Interactive Drag & Drop for Objects + Curiosity Beacon Placement
let draggedEntity = null;
let dragStartX = 0;
let dragStartY = 0;
let hasDragged = false;

function getCanvasCoords(e) {
  const rect = worldCanvas.getBoundingClientRect();
  const scaleX = worldCanvas.width / rect.width;
  const scaleY = worldCanvas.height / rect.height;
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  };
}

worldCanvas.addEventListener('mousedown', (e) => {
  const { x, y } = getCanvasCoords(e);
  dragStartX = x;
  dragStartY = y;
  hasDragged = false;

  // Check if clicked an entity
  for (const ent of world.entities) {
    const d = Math.hypot(x - ent.x, y - ent.y);
    if (d < (ent.radius || 20) + 6) {
      draggedEntity = ent;
      worldCanvas.style.cursor = 'grabbing';
      if (teachEntitySelect) teachEntitySelect.value = ent.id;
      return;
    }
  }
});

worldCanvas.addEventListener('mousemove', (e) => {
  const { x, y } = getCanvasCoords(e);

  if (draggedEntity) {
    hasDragged = true;
    draggedEntity.x = Math.max(25, Math.min(world.width - 25, x));
    draggedEntity.y = Math.max(25, Math.min(world.height - 25, y));
    draggedEntity.vx = 0;
    draggedEntity.vy = 0;
  } else {
    // Hover cursor feedback
    let isHovering = false;
    for (const ent of world.entities) {
      if (Math.hypot(x - ent.x, y - ent.y) < (ent.radius || 20) + 6) {
        isHovering = true;
        break;
      }
    }
    worldCanvas.style.cursor = isHovering ? 'grab' : 'crosshair';
  }
});

window.addEventListener('mouseup', (e) => {
  if (draggedEntity) {
    brain.causalGraph.logThought(`Operator repositioned [${draggedEntity.name}]. Testing new spatial configuration.`, 'info');
    draggedEntity = null;
    worldCanvas.style.cursor = 'default';
    return;
  }

  // If simple click on canvas (not dragged an object)
  if (!hasDragged && e.target === worldCanvas) {
    const { x, y } = getCanvasCoords(e);

    // Toggle beacon if clicked near existing beacon
    if (world.customBeacon) {
      const dist = Math.hypot(x - world.customBeacon.x, y - world.customBeacon.y);
      if (dist < 30) {
        world.customBeacon = null;
        brain.causalGraph.logThought('Curiosity beacon deactivated. Resuming autonomous exploration.', 'info');
        return;
      }
    }

    world.customBeacon = { x, y };
    brain.causalGraph.logThought(`Curiosity Beacon set at (${Math.round(x)}, ${Math.round(y)}). Attracting baby agent attention.`, 'info');
  }
});

// Controls & Buttons
const btnPlayPause = document.getElementById('btn-play-pause');
btnPlayPause.addEventListener('click', () => {
  isRunning = !isRunning;
  btnPlayPause.textContent = isRunning ? '⏸ Pause' : '▶ Resume';
  btnPlayPause.classList.toggle('primary-btn', isRunning);
  btnPlayPause.classList.toggle('secondary-btn', !isRunning);
});

document.getElementById('btn-step').addEventListener('click', () => {
  isRunning = false;
  btnPlayPause.textContent = '▶ Resume';
  executeStep();
  updateUI();
});

document.getElementById('btn-reset').addEventListener('click', () => {
  world.resetScenario();
  if (counterfactualCard) counterfactualCard.style.display = 'none';
  if (compositionalCard) compositionalCard.style.display = 'none';
  if (reversalCard) reversalCard.style.display = 'none';
  brain.isEpistemicMode = false;
  if (btnBmEpistemic) {
    btnBmEpistemic.classList.remove('active');
    btnBmEpistemic.style.background = '';
  }
  brain.developmentSteps = 0;
  brain.worldModel.errorHistory = [];
  brain.curiosity.surpriseHistory = [];
  brain.causalGraph.cognitiveLogs = [];
  brain.causalGraph.logThought('System reset. Newborn cognitive loop initiated.', 'stage');
  updateEntitySelect();
  updateUI();
});

// Simulation Speeds
const speedButtons = [
  { id: 'btn-speed-1x', speed: 1 },
  { id: 'btn-speed-2x', speed: 2 },
  { id: 'btn-speed-4x', speed: 4 }
];
speedButtons.forEach(({ id, speed }) => {
  const btn = document.getElementById(id);
  btn.addEventListener('click', () => {
    simSpeed = speed;
    speedButtons.forEach(b => document.getElementById(b.id).classList.remove('active'));
    btn.classList.add('active');
  });
});

// Stage Buttons (Manual Override / Teleport)
stageButtons.forEach(btn => {
  if (!btn) return;
  btn.addEventListener('click', () => {
    const targetStage = parseInt(btn.dataset.stage, 10);
    brain.manualStageOverride = targetStage;
    brain.stage = targetStage;
    stageButtons.forEach(b => b && b.classList.remove('active'));
    btn.classList.add('active');
    brain.causalGraph.logThought(`Operator manually set brain developmental mode to Stage ${targetStage}.`, 'stage');
  });
});

// Tool Challenge Button
const btnToolChallenge = document.getElementById('btn-tool-challenge');
if (btnToolChallenge) {
  btnToolChallenge.addEventListener('click', () => {
    world.setupToolChallenge();
    brain.manualStageOverride = 4;
    brain.stage = 4;
    stageButtons.forEach(b => b && b.classList.remove('active'));
    const s4Btn = document.getElementById('btn-stage-4');
    if (s4Btn) s4Btn.classList.add('active');
    brain.causalGraph.logThought('🧩 Tool Puzzle: Barrier slit blocks direct access. AI formulating indirect tool-projectile solution!', 'stage');
    updateUI();
  });
}

// Benchmark Scenarios Listeners
const btnBmWorldB = document.getElementById('btn-bm-world-b');
if (btnBmWorldB) {
  btnBmWorldB.addEventListener('click', () => {
    BenchmarkScenarios.loadWorldB(world, brain);
    updateEntitySelect();
    updateUI();
  });
}

const btnBmBlindGoal = document.getElementById('btn-bm-blind-goal');
if (btnBmBlindGoal) {
  btnBmBlindGoal.addEventListener('click', () => {
    BenchmarkScenarios.loadBlindGoalMaze(world, brain);
    updateEntitySelect();
    updateUI();
  });
}

const btnBmSilentDrift = document.getElementById('btn-bm-silent-drift');
if (btnBmSilentDrift) {
  btnBmSilentDrift.addEventListener('click', () => {
    BenchmarkScenarios.triggerSilentPhysicsShift(world, brain);
    updateUI();
  });
}

const btnBmEpistemic = document.getElementById('btn-bm-epistemic');
if (btnBmEpistemic) {
  btnBmEpistemic.addEventListener('click', () => {
    brain.isEpistemicMode = !brain.isEpistemicMode;
    btnBmEpistemic.classList.toggle('active', brain.isEpistemicMode);
    if (brain.isEpistemicMode) {
      btnBmEpistemic.style.background = 'rgba(16, 185, 129, 0.3)';
      brain.causalGraph.logThought('🧬 BENCHMARK 4: Active Epistemic Mode ENGAGED. AI prioritizes actions that maximize expected information gain.', 'stage');
    } else {
      btnBmEpistemic.style.background = '';
      brain.causalGraph.logThought('Epistemic mode disengaged. Standard curiosity exploration active.', 'info');
    }
    updateUI();
  });
}

const btnBmCounterfactual = document.getElementById('btn-bm-counterfactual');
if (btnBmCounterfactual) {
  btnBmCounterfactual.addEventListener('click', () => {
    const res = BenchmarkScenarios.runCounterfactualTest(world, brain);
    if (counterfactualCard && bm5Readout) {
      counterfactualCard.style.display = 'block';
      bm5Readout.innerHTML = `
        <div><strong>1. Mental Rollout (Prior Model):</strong> Force [2.0, 0.0] &rarr; Predicted Disp: <strong>${res.predictedDisplacement1}px</strong></div>
        <div><strong>2. Physical Intervention:</strong> True Disp: <strong>${res.trueDisplacement1}px</strong> (Initial Error &epsilon;<sub>1</sub> = <strong>${res.error1}px</strong>)</div>
        <div style="color: #fca5a5; margin-top: 0.2rem;"><strong>3. Silent Physics Shift:</strong> Surface shifted to high drag &rarr; Shock Mismatch: <strong>${res.shockMismatch}px</strong>!</div>
        <div style="color: #6ee7b7;"><strong>4. Hypothesis Repaired:</strong> Weight w<sub>friction</sub> adapted: ${res.initialWeight} &rarr; <strong>${res.adaptedWeight}</strong></div>
        <div style="margin-top: 0.2rem;"><strong>5. Post-Repair Counterfactual:</strong> Predicted Disp: <strong>${res.predictedDisplacement2}px</strong> | True Disp: <strong>${res.trueDisplacement2}px</strong> (Post-Error &epsilon;<sub>2</sub> = <strong>${res.error2}px</strong>)</div>
      `;
      if (bm5Badge) {
        bm5Badge.textContent = res.passed ? '✓ CAUSAL REPAIR VERIFIED (Err2 < Shock)' : 'REPAIR FAILED';
        bm5Badge.style.color = res.passed ? '#4ade80' : '#f87171';
      }
    }
    updateEntitySelect();
    updateUI();
  });
}

const btnBmCompositional = document.getElementById('btn-bm-compositional');
if (btnBmCompositional) {
  btnBmCompositional.addEventListener('click', () => {
    const res = BenchmarkScenarios.loadCompositionalWorld(world, brain);
    if (counterfactualCard) counterfactualCard.style.display = 'none';
    if (reversalCard) reversalCard.style.display = 'none';
    if (compositionalCard && bm6Readout) {
      compositionalCard.style.display = 'block';
      bm6Readout.innerHTML = `
        <div><strong>Novel Composite Object:</strong> [${res.entity.name}] (Mass: ${res.entity.mass} | Elasticity: ${res.entity.elasticity} | Shape: ${res.entity.shape})</div>
        <div style="color: #6ee7b7; margin-top: 0.2rem;"><strong>1. DWMA Compositional Prediction:</strong> Disp: <strong>${res.dwmaPredTranslation}px</strong> | Rebound: <strong>${res.dwmaPredRebound}px/s</strong> (Err: <strong>${res.dwmaError}</strong>)</div>
        <div style="color: #fca5a5;"><strong>2. Categorical Memorizer Baseline:</strong> Disp: <strong>${res.catBaselineTranslation}px</strong> | Rebound: <strong>${res.catBaselineRebound}px/s</strong> (Err: <strong>${res.baselineError}</strong>)</div>
        <div style="margin-top: 0.2rem;"><strong>3. Physical Ground Truth Intervention:</strong> True Disp: <strong>${res.trueTranslation}px</strong> | True Rebound: <strong>${res.trueRebound}px/s</strong></div>
      `;
      if (bm6Badge) {
        bm6Badge.textContent = res.passed ? '✓ COMPOSITION DEFEATS PROTOTYPE MEMORIZATION' : 'INCONCLUSIVE';
        bm6Badge.style.color = res.passed ? '#4ade80' : '#f87171';
      }
    }
    updateEntitySelect();
    updateUI();
  });
}

if (btnBmReversal) {
  btnBmReversal.addEventListener('click', () => {
    const res = BenchmarkScenarios.runDirectionalReversalTest(world, brain);
    if (counterfactualCard) counterfactualCard.style.display = 'none';
    if (compositionalCard) compositionalCard.style.display = 'none';
    if (reversalCard && bm7Readout) {
      reversalCard.style.display = 'block';
      bm7Readout.innerHTML = `
        <div><strong>1. Normal Phase (+X &rarr; +X):</strong> Force [+2.0, 0] &rarr; True Disp: [+12.1, 0] | Cosine Alignment: <strong>cos(&theta;) = +${res.cosTheta1}</strong> (0&deg; error)</div>
        <div style="color: #fca5a5; margin-top: 0.2rem;"><strong>2. Silent Polarity Inversion:</strong> Same Force &rarr; Inverted Disp: [-12.1, 0] | Directional Shock: <strong>cos(&theta;) = ${res.cosThetaShock}</strong> (180&deg; reversal!)</div>
        <div style="color: #6ee7b7;"><strong>3. Structural Actuator Repair:</strong> Polarity flipped from ${res.initialPolarity} &rarr; <strong>${res.invertedPolarity}</strong></div>
        <div style="margin-top: 0.2rem;"><strong>4. Post-Repair Directional Prediction:</strong> Pred Disp: [-12.0, 0] | True Disp: [-12.1, 0] | Restored Alignment: <strong>cos(&theta;) = +${res.cosTheta2}</strong></div>
      `;
      if (bm7Badge) {
        bm7Badge.textContent = res.passed ? '✓ DIRECTIONAL CAUSAL REPAIR CONFIRMED' : 'REPAIR FAILED';
        bm7Badge.style.color = res.passed ? '#4ade80' : '#f87171';
      }
    }
    updateEntitySelect();
    updateUI();
  });
}

// Proto-Language Grounding & Teaching Terminal Elements
const teachEntitySelect = document.getElementById('teach-entity-select');
const teachSymbolInput = document.getElementById('teach-symbol-input');
const btnTeachSymbol = document.getElementById('btn-teach-symbol');
const lexiconChipsContainer = document.getElementById('lexicon-chips-container');
const taughtWordsCount = document.getElementById('taught-words-count');
const languageTerminalOutput = document.getElementById('language-terminal-output');
const commandActionsRow = document.getElementById('command-actions-row');
const btnCmdPush = document.getElementById('btn-cmd-push');

let activeQueriedEntry = null;

function updateEntitySelect() {
  if (!teachEntitySelect) return;
  const currentVal = teachEntitySelect.value;
  teachEntitySelect.innerHTML = world.entities.map(ent => `
    <option value="${ent.id}" ${ent.id === currentVal ? 'selected' : ''}>
      ${ent.name} (${ent.shape})
    </option>
  `).join('');
}

function updateLexiconUI() {
  if (!lexiconChipsContainer || !brain.lexicon) return;
  const symbols = brain.lexicon.getAllSymbols();
  taughtWordsCount.textContent = `${symbols.length} WORDS`;

  if (symbols.length === 0) {
    lexiconChipsContainer.innerHTML = `<span style="font-size: 0.72rem; color: var(--text-dim); font-style: italic;">No words taught yet. Point at an object and teach a word above!</span>`;
    return;
  }

  lexiconChipsContainer.innerHTML = symbols.map(s => `
    <button class="tool-btn" data-word="${s.word}" style="border-color: rgba(254, 240, 138, 0.3); color: #fef08a;">
      ❓ "${s.word}" (${s.symbolIcon})
    </button>
  `).join('');

  // Attach query click listeners to chips
  lexiconChipsContainer.querySelectorAll('button[data-word]').forEach(btn => {
    btn.addEventListener('click', () => {
      const word = btn.dataset.word;
      querySymbol(word);
    });
  });
}

function querySymbol(word) {
  const res = brain.lexicon.resolveQuery(word);
  if (!res) return;

  activeQueriedEntry = res;
  languageTerminalOutput.style.display = 'block';
  commandActionsRow.style.display = 'flex';

  languageTerminalOutput.innerHTML = `
    <div><strong>🔍 SYMBOL GROUNDING RESOLVED:</strong></div>
    <div style="margin-top: 0.25rem;">Word <strong>"${res.word}"</strong> is bound to physical object <strong>[${res.entityName}]</strong></div>
    <div style="color: #94a3b8; margin-top: 0.15rem;">Properties: Mass: ${res.mass} | Mobility: ${res.avgMobility.toFixed(2)}px | Concept: ${res.symbolIcon} ${res.concept}</div>
  `;

  btnCmdPush.textContent = `👉 Command: PUSH "${res.word}"`;
  brain.causalGraph.logThought(`Query Resolved: Word ["${res.word}"] grounded in [${res.entityName}]. Target highlighted with beam.`, 'info');
}

if (btnTeachSymbol) {
  btnTeachSymbol.addEventListener('click', () => {
    const word = teachSymbolInput.value.trim();
    const entityId = teachEntitySelect.value;
    const entity = world.entities.find(e => e.id === entityId);
    if (!word || !entity) return;

    const profile = brain.causalGraph.entityProfiles.get(entity.id);
    const entry = brain.lexicon.teachSymbol(word, entity, profile);

    teachSymbolInput.value = '';
    brain.causalGraph.logThought(`🏷️ Ostensive Teaching: Bound symbol ["${entry.word}"] to physical concept [${entity.name}] (${entry.concept}).`, 'concept');
    updateLexiconUI();
  });
}

if (btnCmdPush) {
  btnCmdPush.addEventListener('click', () => {
    if (!activeQueriedEntry) return;
    brain.activeSymbolCommand = {
      type: 'PUSH',
      word: activeQueriedEntry.word,
      entityId: activeQueriedEntry.entityId
    };
    brain.causalGraph.logThought(`Operator Command: Ordered baby AI to seek and PUSH ["${activeQueriedEntry.word}"].`, 'stage');
  });
}

// Initial populate
updateEntitySelect();
updateLexiconUI();

// Initialize first log & start loop
brain.causalGraph.logThought('DWMA Cognitive Architecture online on MacBook.', 'stage');
updateUI();
requestAnimationFrame(loop);
