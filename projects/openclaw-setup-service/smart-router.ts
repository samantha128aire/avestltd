/**
 * AvestAI Smart Model Router
 * Automatically selects the best AI model based on message complexity.
 *
 * Tiers:
 *   FAST   → claude-haiku-4-5   (simple questions, reminders, translations)
 *   SMART  → claude-sonnet-4-6  (writing, summaries, explanations — default)
 *   DEEP   → claude-opus-4-6    (analysis, code, legal, complex reasoning)
 *
 * Config (openclaw.json):
 *   plugins.entries.smart-router.config.enabled        — true/false (default: true)
 *   plugins.entries.smart-router.config.fastModel       — model id for FAST tier
 *   plugins.entries.smart-router.config.smartModel      — model id for SMART tier
 *   plugins.entries.smart-router.config.deepModel       — model id for DEEP tier
 *   plugins.entries.smart-router.config.explainRouting  — log routing decisions (default: false)
 */

// ── Tier keyword banks ───────────────────────────────────────────────────────

const FAST_KEYWORDS = [
  // Lookups & facts
  "what is", "what are", "who is", "who are", "where is", "where are",
  "when is", "when was", "when did", "define", "definition", "meaning of",
  "how do you spell", "how do you say", "translate", "convert",
  // Scheduling & reminders
  "remind me", "set a reminder", "schedule", "add to calendar", "what time",
  "when does", "what day", "today", "tomorrow", "tonight",
  // Simple tasks
  "send a message", "send message", "text", "call", "email",
  "search for", "look up", "find", "open", "show me",
  "what's the weather", "weather", "temperature",
  "how many", "how much", "price of", "cost of",
  "yes", "no", "ok", "okay", "thanks", "thank you", "got it",
  "stop", "pause", "cancel", "never mind",
];

const DEEP_KEYWORDS = [
  // Reasoning & analysis
  "analyze", "analyse", "analysis", "evaluate", "assessment", "assess",
  "compare and contrast", "pros and cons", "tradeoffs", "trade-offs",
  "in depth", "in-depth", "detailed", "comprehensive", "thorough",
  "strategic", "strategy", "recommend", "recommendations",
  // Technical
  "debug", "fix this code", "refactor", "architecture", "implement",
  "algorithm", "optimize", "performance", "security audit",
  "write a program", "write a script", "build a",
  // Professional / high-stakes
  "legal", "contract", "agreement", "compliance", "regulation",
  "financial model", "forecast", "projection", "business plan",
  "investment", "risk assessment", "due diligence",
  "research paper", "literature review", "academic",
  // Long-form writing
  "write a report", "write a proposal", "write an essay",
  "draft a contract", "create a plan", "develop a",
  "step by step", "step-by-step", "detailed plan",
];

// ── Routing logic ────────────────────────────────────────────────────────────

type Tier = "fast" | "smart" | "deep";

function classifyPrompt(prompt: string): { tier: Tier; reason: string } {
  const lower = prompt.toLowerCase().trim();
  const wordCount = lower.split(/\s+/).length;

  // Very short messages → fast (greetings, confirmations, quick questions)
  if (wordCount <= 4) {
    return { tier: "fast", reason: `short message (${wordCount} words)` };
  }

  // Check for deep keywords first (they take priority)
  for (const kw of DEEP_KEYWORDS) {
    if (lower.includes(kw)) {
      return { tier: "deep", reason: `matched deep keyword: "${kw}"` };
    }
  }

  // Check for fast keywords
  for (const kw of FAST_KEYWORDS) {
    if (lower.includes(kw)) {
      return { tier: "fast", reason: `matched fast keyword: "${kw}"` };
    }
  }

  // Long messages without keywords → probably needs reasoning
  if (wordCount > 150) {
    return { tier: "deep", reason: `long prompt (${wordCount} words)` };
  }

  // Medium messages → smart (default)
  return { tier: "smart", reason: `medium complexity (${wordCount} words)` };
}

// ── Plugin registration ──────────────────────────────────────────────────────

const DEFAULT_MODELS = {
  fast: "anthropic/claude-haiku-4-5",
  smart: "anthropic/claude-sonnet-4-6",
  deep: "anthropic/claude-opus-4-6",
};

const TIER_LABELS: Record<Tier, string> = {
  fast: "⚡ Fast (Haiku)",
  smart: "🧠 Smart (Sonnet)",
  deep: "🔬 Deep (Opus)",
};

export default function register(api: any) {
  const cfg = api.config?.plugins?.entries?.["smart-router"]?.config ?? {};
  const enabled = cfg.enabled !== false; // default: true

  if (!enabled) {
    console.log("[smart-router] Disabled via config. Skipping registration.");
    return;
  }

  const models = {
    fast: cfg.fastModel ?? DEFAULT_MODELS.fast,
    smart: cfg.smartModel ?? DEFAULT_MODELS.smart,
    deep: cfg.deepModel ?? DEFAULT_MODELS.deep,
  };

  const explainRouting = cfg.explainRouting === true;

  console.log("[smart-router] ✅ Loaded. Models:");
  console.log(`  ⚡ Fast  → ${models.fast}`);
  console.log(`  🧠 Smart → ${models.smart}`);
  console.log(`  🔬 Deep  → ${models.deep}`);
  if (explainRouting) console.log("  🗣️  Explain routing: ON");

  api.on("before_model_resolve", async (event: any, ctx: any) => {
    const prompt: string = event.prompt ?? "";

    // Skip empty or system prompts
    if (!prompt.trim()) return;

    const { tier, reason } = classifyPrompt(prompt);
    const modelOverride = models[tier];

    if (explainRouting) {
      console.log(
        `[smart-router] ${TIER_LABELS[tier]} | reason: ${reason} | session: ${ctx.sessionKey ?? "?"}`
      );
    }

    return { modelOverride };
  });
}
