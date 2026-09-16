import { SelfModel } from './SelfModel.js';
import { PredictiveWorldModel } from './PredictiveWorldModel.js';
import { CuriosityEngine } from './CuriosityEngine.js';
import { CausalGraph } from './CausalGraph.js';
import { SensoryPerception } from './SensoryPerception.js';
import { SymbolLexicon } from './SymbolLexicon.js';
import { EpistemicActiveInference } from './EpistemicActiveInference.js';

/**
 * Unified DWMA Brain: Developmental World-Model AI
 */
export class DWMABrain {
  constructor() {
    this.selfModel = new SelfModel();
    this.worldModel = new PredictiveWorldModel();
    this.curiosity = new CuriosityEngine();
    this.causalGraph = new CausalGraph();
    this.sensory = new SensoryPerception(12, 100);
    this.lexicon = new SymbolLexicon();
    this.activeInference = new EpistemicActiveInference();

    this.developmentSteps = 0;
    this.stage = 0; // 0: Babbling, 1: Physics/Objects, 2: Curiosity, 3: Causal Planning
    this.manualStageOverride = null;

    this.currentAction = { x: 0, y: 0, intent: 'Idle' };
    this.lastState = null;
    this.lastPrediction = null;
    this.imaginedTrajectory = [];
    this.activeSymbolCommand = null;
    this.isEpistemicMode = false;
  }

  getEffectiveStage() {
    if (this.manualStageOverride !== null) {
      return this.manualStageOverride;
    }
    if (this.developmentSteps < 80) return 0; // Motor Babbling
    if (this.developmentSteps < 220) return 1; // Physics Interaction
    if (this.developmentSteps < 500) return 2; // Active Curiosity
    return 3; // Causal Planning & Free Curiosity-Driven Roaming (Default)
  }

  step(agent, entities, arenaBounds, customBeacon = null) {
    this.developmentSteps++;
    this.stage = this.getEffectiveStage();

    // 1. Process sensory signals
    const sensorData = this.sensory.processSensors(agent, entities, arenaBounds);
    this.lastState = {
      x: agent.x,
      y: agent.y,
      vx: agent.vx,
      vy: agent.vy
    };

    // 2. Candidate motor impulses
    const candidateActions = [
      { x: 1.0, y: 0.0 }, { x: -1.0, y: 0.0 },
      { x: 0.0, y: 1.0 }, { x: 0.0, y: -1.0 },
      { x: 0.7, y: 0.7 }, { x: -0.7, y: 0.7 },
      { x: 0.7, y: -0.7 }, { x: -0.7, y: -0.7 },
      { x: 0.0, y: 0.0 }
    ];

    // 3. Stage-dependent action selection or Symbolic Command Override
    let selectedAction = null;

    if (this.activeSymbolCommand) {
      const targetEnt = entities.find(e => e.id === this.activeSymbolCommand.entityId);
      if (targetEnt) {
        const dx = targetEnt.x - agent.x;
        const dy = targetEnt.y - agent.y;
        const dist = Math.hypot(dx, dy);
        if (dist > (agent.radius + targetEnt.radius + 6)) {
          selectedAction = {
            x: (dx / dist) * 1.0,
            y: (dy / dist) * 1.0,
            intent: `Executing: PUSH [${this.activeSymbolCommand.word}]`
          };
        } else {
          selectedAction = {
            x: (dx / Math.max(0.1, dist)) * 1.2,
            y: (dy / Math.max(0.1, dist)) * 1.2,
            intent: `Contact: Pushed [${this.activeSymbolCommand.word}]!`
          };
          this.causalGraph.logThought(`Command Fulfilled: Located and pushed [${this.activeSymbolCommand.word}].`, 'concept');
          this.activeSymbolCommand = null;
        }
      } else {
        this.activeSymbolCommand = null;
      }
    }

    if (!selectedAction && this.isEpistemicMode) {
      const mostInformative = this.activeInference.selectMostInformativeEntity(entities);
      if (mostInformative) {
        const dx = mostInformative.x - agent.x;
        const dy = mostInformative.y - agent.y;
        const dist = Math.hypot(dx, dy);
        if (dist > (agent.radius + mostInformative.radius + 6)) {
          selectedAction = {
            x: (dx / dist) * 1.0,
            y: (dy / dist) * 1.0,
            intent: `Epistemic Probe: Testing [${mostInformative.name}] (Max Uncertainty)`
          };
        } else {
          selectedAction = {
            x: (dx / Math.max(0.1, dist)) * 1.1,
            y: (dy / Math.max(0.1, dist)) * 1.1,
            intent: `Impulse Probe: Measuring reaction of [${mostInformative.name}]`
          };
        }
      }
    }

    if (!selectedAction) {
      if (this.stage === 0) {
      const randAngle = Math.random() * Math.PI * 2;
      const mag = Math.random() * 0.9 + 0.1;
      selectedAction = {
        x: Math.cos(randAngle) * mag,
        y: Math.sin(randAngle) * mag,
        intent: 'Motor Babbling (Ego-Discovery)'
      };
    } else if (this.stage === 1) {
      if (Math.random() < 0.3) {
        const randAngle = Math.random() * Math.PI * 2;
        selectedAction = {
          x: Math.cos(randAngle) * 0.8,
          y: Math.sin(randAngle) * 0.8,
          intent: 'Physical Probe'
        };
      } else {
        selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
      }
    } else if (this.stage === 2) {
      selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
    } else if (this.stage === 3) {
      // Stage 3: Causal Planning & Mental Rollouts
      selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
      selectedAction.intent = 'Goal & Causal Planning';

      const planActions = [
        selectedAction,
        selectedAction,
        { x: selectedAction.x * 0.8, y: selectedAction.y * 0.8 },
        { x: selectedAction.x * 0.6, y: selectedAction.y * 0.6 }
      ];
      this.imaginedTrajectory = this.worldModel.imagineTrajectory(this.lastState, planActions);
    } else {
      // Stage 4: Multi-Step Tool Use (Indirect Object Shoving)
      const movableTools = entities.filter(e => e.mass < 5.0 && e.mass > 0.5);
      const targetEntity = customBeacon || entities.find(e => e.id.includes('target') || e.id.includes('crystal') || e.id.includes('node'));

      if (!this.toolAttemptCounter) this.toolAttemptCounter = 0;
      this.toolAttemptCounter++;

      // If tool pushing has been attempted for a while, rotate to curiosity break
      if (this.toolAttemptCounter > 60 && this.toolAttemptCounter < 160) {
        selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
      } else if (this.toolAttemptCounter >= 160) {
        this.toolAttemptCounter = 0;
      }

      if (!selectedAction && movableTools.length > 0 && targetEntity) {
        const tool = movableTools[0];
        // Line from Tool -> Target
        const tdx = targetEntity.x - tool.x;
        const tdy = targetEntity.y - tool.y;
        const tdist = Math.hypot(tdx, tdy);

        if (tdist < 45) {
          // Tool reached target! Satiated / Goal complete
          if (!this.toolGoalCelebrated) {
            this.toolGoalCelebrated = true;
            this.causalGraph.logThought(`🎯 Mission Accomplished! [${tool.name}] successfully delivered impulse to [${targetEntity.name}]. Disengaging.`, 'concept');
          }
          selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
        } else {
          // Desired position for Agent: Behind tool pointing at target
          const nx = tdist > 0.001 ? tdx / tdist : 1;
          const ny = tdist > 0.001 ? tdy / tdist : 0;
          const pushSlotX = tool.x - nx * 35;
          const pushSlotY = tool.y - ny * 35;

          const distToSlot = Math.hypot(pushSlotX - agent.x, pushSlotY - agent.y);

          if (distToSlot > 18) {
            // Navigate to position behind tool
            const sdx = pushSlotX - agent.x;
            const sdy = pushSlotY - agent.y;
            const sdist = Math.hypot(sdx, sdy);
            selectedAction = {
              x: (sdx / sdist) * 1.0,
              y: (sdy / sdist) * 1.0,
              intent: `Aligning Behind Tool [${tool.name}]`
            };
          } else {
            // Push directly through tool towards target
            selectedAction = {
              x: nx * 1.0,
              y: ny * 1.0,
              intent: `Striking Tool [${tool.name}] Towards Target!`
            };
          }
        }
      } else {
        selectedAction = this.curiosity.selectCuriousAction(candidateActions, agent, entities, customBeacon);
      }

      const planActions = [selectedAction, selectedAction, selectedAction];
      this.imaginedTrajectory = this.worldModel.imagineTrajectory(this.lastState, planActions);
    }
  }

    this.currentAction = selectedAction;

    // 4. Generate forward prediction using internal model
    this.lastPrediction = this.worldModel.predictNextState(this.lastState, this.currentAction);

    // Record spatial sector visit
    this.curiosity.recordSectorVisit(agent.x, agent.y);

    return {
      action: this.currentAction,
      prediction: this.lastPrediction,
      stage: this.stage,
      step: this.developmentSteps,
      imaginedTrajectory: this.imaginedTrajectory
    };
  }

  observeConsequence(nextState, collidedEntity = null, displacement = 0, entityCollisions = []) {
    if (!this.lastState || !this.lastPrediction) return 0;

    // 1. Calculate prediction error and update predictive world model
    const error = this.worldModel.update(this.lastState, this.currentAction, nextState);

    // 2. Intrinsic surprise reward & sensory feedback
    this.curiosity.computeIntrinsicReward(error);
    const actualDisplacement = Math.hypot(nextState.x - this.lastState.x, nextState.y - this.lastState.y);
    const actionMag = Math.hypot(this.currentAction.x, this.currentAction.y);
    const wasEscaping = this.curiosity.isEscaping;

    this.curiosity.recordSensoryFeedback(this.sensory.rays, actualDisplacement, actionMag);

    if (!wasEscaping && this.curiosity.isEscaping) {
      this.causalGraph.logThought('Mobility blocked! Initiating tangential gap search & contour navigation.', 'stage');
    } else if (wasEscaping && !this.curiosity.isEscaping) {
      this.causalGraph.logThought('Breakout successful! Escaped barrier cage through detected gap.', 'concept');
    }

    // 3. Update self-model agency
    const stateDelta = {
      dx: nextState.x - this.lastState.x,
      dy: nextState.y - this.lastState.y,
      vx: nextState.vx - this.lastState.vx,
      vy: nextState.vy - this.lastState.vy
    };
    this.selfModel.update(this.currentAction, stateDelta);

    // 4. Update causal graph if collision/interaction occurred
    if (collidedEntity) {
      const forceMag = Math.hypot(this.currentAction.x, this.currentAction.y);
      this.causalGraph.recordInteraction(collidedEntity, this.currentAction, displacement, forceMag);

      // Active Inference probe resolution
      const pRes = this.activeInference.recordProbeResult(collidedEntity, forceMag, displacement);
      if (pRes && pRes.infoGain > 0.35) {
        this.causalGraph.logThought(`🧬 Active Inference: Probe on [${collidedEntity.name}] collapsed variance from ${pRes.oldVariance.toFixed(1)} to ${pRes.newVariance.toFixed(1)} (+${pRes.infoGain.toFixed(2)} nats).`, 'concept');
      }
    }

    // Concept Drift & Sudden Physics Shift Detection
    if (error > 2.5 && this.worldModel.totalSteps > 60) {
      if (!this.lastDriftAlert || (Date.now() - this.lastDriftAlert) > 4000) {
        this.lastDriftAlert = Date.now();
        this.causalGraph.logThought(`⚠️ PREDICTIVE SURPRISE SHOCK (E=${error.toFixed(2)}): Sudden physics mismatch detected! Online weights recalibrating to new ground dynamics.`, 'stage');
      }
    }

    // 5. Object-to-Object (Tool Use) collisions
    if (entityCollisions && entityCollisions.length > 0) {
      for (const col of entityCollisions) {
        this.causalGraph.recordObjectToObjectCollision(col.source, col.target, col.impulse);
      }
    }

    return error;
  }
}
