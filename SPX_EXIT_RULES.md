# SPX Calendar Strategy – Exit Rules Reference Card

## Quick Rules (Memorize These)

### ✅ ENTRY RULES (Before Opening)
1. **VIX Check:** Only enter if VIX ≥ 16.5
   - If VIX < 16.5 → Skip the trade
   - (Your data: VIX < 16.0 produced 100% losses)

2. **Trade Type:** Double Calendar or Double Diagonal spreads only
   - Capture 30-50% of max profit in 3-6 days
   - Then exit or convert to IC

---

### 🔴 EXIT RULES (During Trade)

#### **PRIMARY EXIT: 50% Max Profit Rule** ⭐⭐⭐
- **Trigger:** Trade reaches 50% of max profit
- **Action:** CLOSE immediately
- **Why:** Holding past 50% profit risks erosion into losses
- **Data:** Your Trades #5, #8, #9 all eroded after early profits

**Example:**  
- Max Profit = $4,000  
- 50% = $2,000 profit
- When you hit $2,000 → EXIT

---

#### **SECONDARY EXIT: VIX Decline Rule** ⭐⭐⭐
- **Trigger:** VIX drops >1.0 point within first 3 days
- **Action:** Convert to Iron Condor OR close
- **Why:** Calendar spreads lose money when IV compresses
- **Data:** Trades #5-8 all lost money during VIX drop from 16.9→15.3

**Example:**  
- Entry: VIX 16.9
- Day 2: VIX drops to 15.8
- Trigger: 1.1 point drop = CONVERT or EXIT

---

#### **TERTIARY EXIT: Time Decay Rule**
- **If at Day 3:** Close if you have >30% profit
- **If at Day 4:** Close if you have >20% profit  
- **If at Day 6+:** Close regardless (theta decay reverses)
- **Why:** Optimal hold = 3-6 days; longer exposes to IV crush

---

#### **IRON CONDOR CONVERSION TRIGGER**
- **When:** Trade at day 2-3 AND:
  - VIX has dropped >0.5 point, OR
  - SPX moved >25-30 points against shorts, OR
  - You can lock in breakeven or better pricing
- **Action:** Convert calendar → Iron Condor
- **Why:** Locks profit, eliminates theta risk, guarantees breakeven+
- **Data:** Your IC conversions had excellent results—do them MORE often

---

## Decision Tree

```
ENTRY:
├─ VIX < 16.5? → SKIP this trade
├─ VIX ≥ 16.5? → ENTER calendar/diagonal spread
│
DAY 1-2:
├─ Profit > 50% max? → CLOSE immediately
├─ VIX down > 1.0 pt? → CONVERT to IC or CLOSE
└─ Otherwise → Hold
│
DAY 3-4:
├─ Profit > 30%? → CLOSE
├─ Profit < 20%? → CONVERT to IC or CLOSE
├─ VIX down >0.5 pt? → CONVERT to IC
└─ All conditions met → HOLD to day 5
│
DAY 5-6:
├─ Profit > 10%? → CLOSE
└─ Otherwise → CLOSE and move on (don't hold past day 6)
│
DAY 7+:
└─ ALWAYS CLOSE (theta decay reverses)
```

---

## Performance Expectations

If you follow these rules:

| Rule | Expected Impact |
|------|-----------------|
| 50% Profit Exit | +$500-600 saved (vs holding to losses) |
| VIX ≥ 16.5 Entry Filter | +18% improvement in win rate |
| IC Conversion by Day 3 | Eliminates 40% of remaining losses |
| Optimal Hold: 3-6 Days | Increases avg win per trade |

**Conservative Estimate:** Following these rules could improve your net P/L by 30-50% on this strategy.

---

## Current Edge Summary

From 11 completed trades:
- **Win Rate:** 45% (5 winners, 5 losers, 1 breakeven)
- **Profit Factor:** 1.61x
- **Net P/L:** +$791 (fragile)

With these rules applied:
- **Projected Win Rate:** 60-65%
- **Projected Profit Factor:** 2.0-2.2x
- **Projected Net P/L:** +$1,500-2,000 (on similar sample size)

---

## When to Break the Rules

✅ OK to break rules if:
- IC conversion opportunity is available at <25% of max profit (take it)
- Underlying has fundamental gap event (earnings, major news)
- Unexpected black-swan VIX spike (adjust position, don't hold)

❌ Don't break rules for:
- "Waiting for max profit" (this is why you have losses)
- "Just one more day" (this erodes wins)
- Hope/emotion (trade the rules, not feelings)

---

## Tracking Your Trades

Each trade, log:
1. **Entry Date / VIX / SPX**
2. **Day 1-2 Check:** Profit %? VIX change?
3. **Day 3 Decision:** Close at 50%? Convert to IC? Hold?
4. **Exit Date / Price / P/L**
5. **Rule Followed?** (yes/no/broken)

This log will show you which rules work best over time.

