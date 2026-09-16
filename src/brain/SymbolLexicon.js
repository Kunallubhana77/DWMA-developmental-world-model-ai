/**
 * DWMA Symbol Lexicon (Symbol Grounding Engine)
 * Bridges human words/symbols directly to physical sensorimotor clusters and causal nodes.
 * Completely LLM-free: Operates via associative memory, ostensive pointing, and affordance queries.
 */
export class SymbolLexicon {
  constructor() {
    // word (uppercase) -> { entityId, entityName, physicalProfile, timestamp }
    this.groundedSymbols = new Map();
    this.activeQueryTarget = null;
  }

  /**
   * Ostensive Teaching: Pair a human symbol with an existing physical entity & concept
   */
  teachSymbol(word, entity, conceptProfile) {
    const cleanWord = word.trim().toUpperCase();
    if (!cleanWord) return null;

    const entry = {
      word: cleanWord,
      entityId: entity.id,
      entityName: entity.name,
      color: entity.color,
      shape: entity.shape,
      mass: entity.mass,
      concept: conceptProfile ? conceptProfile.concept : 'Unknown Concept',
      symbolIcon: conceptProfile ? conceptProfile.symbol : '🏷️',
      avgMobility: conceptProfile ? conceptProfile.avgMobility : 0,
      timestamp: new Date().toLocaleTimeString()
    };

    this.groundedSymbols.set(cleanWord, entry);
    return entry;
  }

  /**
   * The "What / Kaun" Query Operator:
   * Given a symbol, queries the internal memory and returns the grounded physical entity.
   */
  resolveQuery(word) {
    const cleanWord = word.trim().toUpperCase();
    const entry = this.groundedSymbols.get(cleanWord);
    if (!entry) return null;

    this.activeQueryTarget = entry.entityId;
    return entry;
  }

  clearActiveQuery() {
    this.activeQueryTarget = null;
  }

  getAllSymbols() {
    return Array.from(this.groundedSymbols.values());
  }

  getSymbolForEntity(entityId) {
    for (const [word, entry] of this.groundedSymbols.entries()) {
      if (entry.entityId === entityId) return word;
    }
    return null;
  }
}
