# DC Time Machine — Complete Trading Guide

**Strategy by:** Steve Bernich  
**Documented:** June 2026  
**Strategy type:** Double Calendar → Risk-Free Iron Condor Transformation  
**Underlying:** SPX (S&P 500 Index)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Why SPX](#2-why-spx)
3. [Step-by-Step Entry](#3-step-by-step-entry)
4. [Reading the Flux Chart](#4-reading-the-flux-chart)
5. [The Transformer Order](#5-the-transformer-order)
6. [Worked Example](#6-worked-example)
7. [Managing the Position](#7-managing-the-position)
8. [Exit Strategies](#8-exit-strategies)
9. [Risk Management](#9-risk-management)
10. [Results & Statistics](#10-results--statistics)
11. [Common Mistakes](#11-common-mistakes)
12. [Glossary](#12-glossary)

---

## 1. Overview

### What Is the DC Time Machine?

The DC Time Machine is an options trading strategy developed by **Steve Bernich** that transforms a standard Double Calendar spread into a **risk-free iron condor** — a position where you cannot lose money regardless of where the market moves.

The "time machine" metaphor refers to buying time (theta) cheaply and selling it expensively: you enter a calendar spread when implied volatility is elevated in the front expiration relative to the back, then as the IV ratio normalizes, you extract that premium by converting the position into a locked-in iron condor.

### Core Philosophy

> "The goal isn't to make money from the market moving. The goal is to make money from the market calming down."

The strategy exploits a reliable tendency in SPX options: when short-dated implied volatility spikes relative to longer-dated IV, it mean-reverts. By entering a double calendar at the right moment (high ratio, ratio beginning to fall), then transforming it when you have a small profit, you can often lock in a **guaranteed minimum profit** on the resulting iron condor — turning a risky position into a free trade.

### The Two-Stage Process

```
Stage 1: Double Calendar (risky, limited window)
    → Enter when front/back IV ratio is high and falling
    → Wait for 5–10% profit
    ↓
Stage 2: Transformer Order (single order, converts to risk-free IC)
    → Lock in guaranteed minimum profit
    → Position is now risk-free
    → Buying power recycled
```

---

## 2. Why SPX

SPX has specific advantages that make it ideal for this strategy:

| Feature | SPX | SPY / Other Equities |
|---------|-----|----------------------|
| **Settlement style** | European (cash) | American (can be assigned) |
| **Assignment risk** | **None** | Yes — can be exercised early |
| **Tax treatment** | 60/40 (60% long-term, 40% short-term) | 100% short-term |
| **Expiration cycle** | MWF weeklies + EOM | Fridays only (most) |
| **Liquidity** | Extreme — tightest bid/ask | High, but wider spreads |
| **Notional value** | ~$5,500 per point | ~$550 per point |
| **Multiplier** | $100 per contract | $100 per contract |

### Why European Settlement Matters

American-style options can be exercised at any time. This means if you're short an SPY put that goes deep in the money, you can be assigned and forced to buy/sell shares unexpectedly. SPX is cash-settled: at expiration, you receive (or pay) the cash difference. No shares, no assignment risk, no surprises.

### The 60/40 Tax Advantage

Under Section 1256 of the U.S. tax code, SPX options receive special treatment:
- **60% of gains** are taxed as long-term capital gains (max 20%)
- **40% of gains** are taxed as short-term capital gains (ordinary income)
- This applies regardless of how long you held the position
- Effective blended max rate for high earners: ~26.8% vs. 37% short-term

On $66,000 of gains, this can save $5,000–$7,000 in taxes annually.

### Weekly Expirations

SPX expires on **Monday, Wednesday, and Friday** each week, plus end-of-month expirations. This creates multiple opportunities each week to find the 1-day DTE gap between front and back expirations that the strategy requires.

---

## 3. Step-by-Step Entry

### 3.1 Find a Setup Using the Flux Tool

Before placing any trade, you need to identify when conditions are favorable using the **Flux chart** (see Section 4).

**Entry checklist:**
- [ ] Orange ratio line is **elevated** (above the mean, ideally above +1σ)
- [ ] Orange ratio line has **peaked and is beginning to fall**
- [ ] Market is in a relatively normal state (not immediately post-crash)
- [ ] You have enough capital to absorb full max loss without stopping trading

### 3.2 Select Your Strikes

The double calendar uses the **same strikes for both puts and calls**. Target the 30–40 delta strikes on both sides.

**How to find 30–40 delta strikes:**

1. Look at the SPX option chain
2. Find the put with ~35 delta below the current price → this is your put strike
3. Find the call with ~35 delta above the current price → this is your call strike
4. The two strikes will typically be 40–80 points apart depending on IV

**Example — SPX at 5,500:**
```
SPX = 5,500
Put strike:  5,450  (35 delta put)
Call strike: 5,550  (35 delta call)
Width:       100 points
```

**Rule of thumb:** Strikes should be roughly symmetric around the current price. Don't chase strikes — let the market tell you where the 35-delta line is.

### 3.3 Choose Your Expirations

| Leg | Expiration | DTE range | Action |
|-----|-----------|-----------|--------|
| Short | Front week (nearest) | 6–15 DTE | Sell |
| Long | Back week (next) | 7–16 DTE | Buy |
| Gap | | **Exactly 1 trading day** | Required |

**Why exactly 1-day gap?** The Flux ratio measures the IV difference between these two specific expirations. A 1-day gap maximizes the theta differential while keeping the vega exposure manageable. Wider gaps change the risk profile significantly.

**Finding expiration pairs (MWF weekly cycle):**
```
If today is Monday, June 3:
  Front: Wednesday, June 5  (2 days away — too short)
  Front: Friday, June 7     (4 days away — might work)
  Back:  Monday, June 10    (5 days away — 1 day after front)
  
Or:
  Front: Wednesday, June 12  (9 days away — ideal)
  Back:  Friday, June 14     (11 days away — 1 day after front)
```

### 3.4 Structure the Double Calendar

A **double calendar** consists of four legs:

```
SELL  Front Put  (e.g., Jun5 5450P)  →  credit received
BUY   Back Put   (e.g., Jun6 5450P)  →  debit paid
SELL  Front Call (e.g., Jun5 5550C)  →  credit received
BUY   Back Call  (e.g., Jun6 5550C)  →  debit paid

Net position: DEBIT (you pay to enter)
Typical cost: $800–$1,500 per contract
```

**Enter as a single 4-leg combo order.** Never leg into a double calendar — you'll get slippage on every leg.

### 3.5 Position Sizing

**Rule: Size so you can absorb 100% of the debit without stopping trading.**

```
Account size: $50,000
Max loss per DC: $1,500 (the debit you paid)
Position size: 1 contract

At 2 contracts: max loss = $3,000 = 6% of account (acceptable)
At 5 contracts: max loss = $7,500 = 15% of account (too large for most)
```

The mental stop is 20% of the debit (see Section 9). But you must be able to handle the full max loss in a worst-case scenario.

---

## 4. Reading the Flux Chart

The Flux chart has three lines:

### The Three Lines

| Line | Color | What It Shows | How to Use |
|------|-------|---------------|------------|
| **Front IV** | Blue | ATM implied volatility of the front (shorter) expiration | Rising = nervousness in short-dated options |
| **Back IV** | Green | ATM implied volatility of the back (longer) expiration | More stable than blue line |
| **Ratio** | Orange | Front IV ÷ Back IV | The KEY trading signal |

### What the Ratio Tells You

```
Ratio = Front IV / Back IV

Ratio = 1.00 → Front and back IVs are equal (fair value)
Ratio > 1.00 → Front IV elevated vs. back (calendar is cheap = good)
Ratio < 1.00 → Front IV compressed vs. back (calendar is expensive = avoid)
Ratio > 1.15 → Elevated, potential opportunity
Ratio > 1.25 → Very elevated, high-quality setup (rare)
```

### Reference Lines

The chart also shows:
- **Mean line (gray dashed):** Average ratio over the displayed period
- **+1σ line (red dotted):** One standard deviation above mean

**When ratio is at +1σ or above and starting to fall → that's your entry signal.**

### Entry Signal (⚡)

The Flux tool calculates when the ratio has dropped X% from its intraday high (default: 0.5%). When triggered:
- Yellow horizontal line appears on the ratio chart
- "⚡ ENTRY SIGNAL" label displayed with the % drop
- This is your cue to check if conditions are right

### Good Setup vs. Bad Setup

**Good Setup ✅**
```
- Orange ratio: 1.18 and falling (peaked 10 minutes ago)
- Blue line: recently spiked up, now pulling back
- Green line: relatively flat, mild uptrend
- Market: normal volatility environment, no macro event today
```

**Bad Setup ❌**
```
- Orange ratio: 1.02 (barely elevated, not worth entering)
- Orange ratio: 1.15 but still rising (wait for the peak)
- Orange ratio: 1.22 but FOMC announcement in 1 hour (IV could spike further)
- Blue line: wildly erratic (market in crisis)
```

### Intraday vs. Multi-Day Views

| View | Best for |
|------|---------|
| **Intraday (1-min)** | Timing your entry — watching for the exact peak and rollover |
| **5-Day** | Context — is today's ratio unusually high vs. recent days? |
| **20-Day** | Trend — what's the typical ratio range for this market regime? |
| **Scanner** | Finding the best expiration pair to trade right now |

---

## 5. The Transformer Order

This is the heart of the strategy. The transformer converts your double calendar into a **guaranteed profit iron condor** in a single order.

### What Is the Transformer Order?

After your double calendar is up 5–10%, you place a single 4-leg order that:

1. **Sells (closes)** your back-dated long options (both put and call)
2. **Buys (opens)** protective wings on the front-dated expiration

This leaves you holding:
- Short front put + long (protective) further-OTM front put = put credit spread
- Short front call + long (protective) further-OTM front call = call credit spread
- Combined = **Iron Condor** on the front expiration

### The Math Formula

```
Required transformer credit = Original DC debit + Wing width cost

Where:
  Wing width cost = wing width (points) × $100 per contract

For 5-point wings:
  Required credit ≥ (Original DC debit paid) + $500

For 10-point wings:
  Required credit ≥ (Original DC debit paid) + $1,000
```

### Why This Makes It Risk-Free

After transformation:

```
Net cash flow:
  - Paid: DC debit (e.g., $1,010)
  - Received: Transformer credit (e.g., $1,510)
  - Net credit received: $500

Iron condor max loss = wing width × $100 = 5 × $100 = $500

Worst case P&L = Net credit received − Iron condor max loss
              = $500 − $500 = $0

Best case P&L (all options expire worthless) = Net credit received = $500
```

You **cannot lose money** once transformed. The worst outcome is breaking even.

### Wing Selection

**Standard approach: 5-point OTM wings**

```
Short front put:   5,450
Long front put:    5,445  (5 points lower)

Short front call:  5,550
Long front call:   5,555  (5 points higher)
```

**Wider wings = more cushion, higher required credit**

You can use 10-point wings if you need more protection or if the transformer credit is generous:
```
5-point wings: Need $500 of credit above DC debit
10-point wings: Need $1,000 of credit above DC debit
```

### Setting the Transformer as a GTC Limit Order

**Enter the transformer order IMMEDIATELY after entering the DC — before it reaches profit target.**

Set it as:
- **GTC (Good Till Cancelled)**
- **Limit order for the required credit**
- The order fires automatically when the market provides your price

This way you don't have to watch the position constantly. The transformation happens automatically.

### Transformer Order Structure (4 legs)

```
Leg 1: SELL  Back Put   (close your long, e.g., Jun6 5450P) → credit
Leg 2: SELL  Back Call  (close your long, e.g., Jun6 5550C) → credit
Leg 3: BUY   Front Put  (open wing, e.g., Jun5 5445P)       → debit
Leg 4: BUY   Front Call (open wing, e.g., Jun5 5555C)       → debit

Net: Should be a CREDIT equal to (original DC debit + wing width cost)
```

---

## 6. Worked Example

### Setup

```
Date:    Monday, June 2
SPX:     5,500
Account: $50,000
```

### Step 1: Identify the Setup

Flux chart shows:
- Front exp (Jun 5) IV: 18.5%
- Back exp (Jun 6) IV: 15.8%
- Ratio: 1.171 (elevated, peaked 8 minutes ago, now at 1.166 and falling)
- Entry signal fired: ratio dropped 0.5% from intraday high of 1.174

### Step 2: Select Strikes

```
SPX = 5,500
35-delta put:  5,450
35-delta call: 5,550
```

### Step 3: Enter the Double Calendar

```
SELL  1 Jun5 5450 Put    @ $12.50    +$1,250 credit
BUY   1 Jun6 5450 Put    @ $14.80   -$1,480 debit
SELL  1 Jun5 5550 Call   @ $11.20    +$1,120 credit
BUY   1 Jun6 5550 Call   @ $12.10   -$1,210 debit

Net debit: ($1,480 + $1,210) − ($1,250 + $1,120) = $2,690 − $2,370 = $320

Wait — that's too cheap. Let's use a more realistic example:

SELL  1 Jun5 5450 Put    @ $8.50     +$850 credit
BUY   1 Jun6 5450 Put    @ $12.30   -$1,230 debit
SELL  1 Jun5 5550 Call   @ $7.80     +$780 credit
BUY   1 Jun6 5550 Call   @ $11.10   -$1,110 debit

Net debit: ($1,230 + $1,110) − ($850 + $780)
         = $2,340 − $1,630
         = $710 debit paid
```

### Step 4: Set Transformer Order Immediately

```
Required transformer credit = DC debit + wing width cost
                            = $710 + $500 (5-point wings × $100)
                            = $1,210 minimum

Transformer order (GTC limit, $15.25 credit target):
  SELL  1 Jun6 5450 Put    (close back long)
  SELL  1 Jun6 5550 Call   (close back long)
  BUY   1 Jun5 5445 Put    (open front wing)
  BUY   1 Jun5 5555 Call   (open front wing)
  → Enter for a net CREDIT of at least $12.10 ($1,210)
```

### Step 5: Double Calendar Profit Phase

Next day (June 3), SPX barely moves. Front IV contracts:
- Front exp IV: 16.8% (fell from 18.5%)
- Back exp IV: 15.4% (fell slightly)
- Ratio: 1.091 (returned toward mean)

Double calendar value has increased ~8%. Transformer order fills at $12.50 credit = $1,250.

### Step 6: Post-Transformation Position

```
Position after transformation:
  Short Jun5 5450 Put  +  Long Jun5 5445 Put  = Put credit spread (5-pt wide)
  Short Jun5 5550 Call +  Long Jun5 5555 Call = Call credit spread (5-pt wide)
  = Iron Condor on Jun5

P&L Analysis:
  DC debit paid:        −$710
  Transformer credit:   +$1,250
  Net credit:           +$540

  Max IC loss (if SPX blows through wings):  −$500 (5 × $100)

  Worst case: +$540 − $500 = +$40 (tiny profit, not zero — slightly better than break-even)
  Best case:  +$540         (SPX stays between 5445 and 5555 through Jun5 expiration)
```

### P&L Diagram (Post-Transformation Iron Condor)

```
Profit
  $540 |----\                          /----
       |     \                        /
  $40  |      \                      /   ← worst case (wing cost)
  $0   |       \--------------------/
       |
  -    |   (impossible — position is risk-free)
       +----+----+----+----+----+----+----→  SPX at expiration
          5440  5445 5450       5550 5555 5560

Zone:  Loss    Flat  Profit Zone      Flat  Loss (but floored at $40 due to net credit)
```

*Note: Because the net credit ($540) exceeds the wing cost ($500), even the "loss" zone of the IC results in a small profit.*

---

## 7. Managing the Position

### Phase 1: During the Double Calendar (Before Transformation)

| Situation | Action |
|-----------|--------|
| DC shows 5–10% gain | **Place transformer order at limit for required credit** |
| DC shows <5% gain | Wait. Monitor ratio. |
| DC shows −20% loss | Consider closing (mental stop). See Section 9. |
| Market makes large move toward your strikes | Watch closely — may want to exit DC |
| Front IV spikes further (ratio rises again) | Good — calendar likely gaining value |
| News event approaching (FOMC, CPI, etc.) | Consider closing before event |

**Never add to a losing DC position.**

### Phase 2: After Transformation (Iron Condor)

Once transformed: **Do nothing.**

The position is risk-free. There is no stop loss to monitor. Let it expire.

| Situation | Action |
|-----------|--------|
| SPX inside the iron condor wings | Let expire worthless → collect full credit |
| SPX approaching or beyond a wing | Still no action needed — you've already guaranteed a profit |
| Transformer order gets filled early | Great — set a reminder for expiration |

**Exception:** If you can close the IC early for 80%+ of max profit with significant time remaining, it may be worth closing to recycle the buying power sooner.

### Partial Transformation Strategy

Advanced approach: Transform only **half** the position early, leave the rest open.

```
Example: 4 contracts of DC
  At 5% DC profit → Transform 2 contracts at lower credit
  At 12% DC profit → Transform remaining 2 contracts at higher credit
  
Result: Higher blended credit on the full position
Risk: The remaining 2 contracts still carry DC risk until transformed
```

This works best when you expect the ratio to continue falling and the DC to gain more value before plateauing.

---

## 8. Exit Strategies

### Option A: Let the Iron Condor Expire

**Best when:** SPX is comfortably inside the iron condor range with 1–2 days to expiration.

- No commissions on expiring worthless positions (at most brokers)
- Maximum profit achieved
- No action required

### Option B: Close the Iron Condor Early

**Consider closing when:**
- You can capture 75–80%+ of the max credit with ≥3 days remaining
- You need buying power for a new trade
- Gamma risk increases (last 24 hours before expiration with SPX near a short strike)

**How to close:** Buy back the iron condor as a 4-leg order. Do not leg out.

### Option C: Close the DC Early (Before Transformation)

**When transformation is NOT achievable:**
- If the required credit for transformation is not available in the market
- If market conditions have changed (e.g., IV crashed before you got 5% profit)
- Close the DC for a small loss and move on

### Probability of Hitting Max Profit

Steve Bernich's data suggests the iron condor (after transformation) hits max profit approximately **25% of the time** — meaning SPX expires inside the wings. The other 75% of the time, SPX moves through at least one wing, but you still profit because your net credit exceeds the wing cost.

```
P(max profit) = ~25%
P(positive profit) = ~100% (it's risk-free after transformation)
P(break-even) = rare edge case where net credit exactly equals wing cost
```

---

## 9. Risk Management

### Position Sizing Philosophy

**Rule #1:** Size so that the maximum DC loss (full debit) doesn't end your trading.

```
If max DC loss = $1,500:
  Account must be ≥ $15,000 to risk 10% per trade (aggressive)
  Account must be ≥ $30,000 to risk 5% per trade (moderate)
  Account must be ≥ $75,000 to risk 2% per trade (conservative)
```

**Rule #2:** The strategy compounds. If you're running it 2–4x per week, you need to account for concurrent positions.

```
Running 3 DCs simultaneously, each with $1,000 max loss:
  Total exposure: $3,000
  Required account: $30,000 (10%) to $150,000 (2%)
```

### The Mental Stop: 20% of Debit

The DC has no hard stop. Instead, use a **mental stop at 20% of the debit paid.**

```
DC debit paid: $1,000
Mental stop:   $200 loss

If DC position value drops $200 below purchase price → close the DC
```

**Why a mental stop vs. hard stop?**
- Double calendars can gap around and recover quickly
- A hard stop can trigger on a momentary spike, closing a position that would have recovered
- You're watching this during market hours anyway

### Black Swan Risk

The DC's maximum loss is the debit paid — period. No matter how far SPX moves, you cannot lose more than you put in. This is a key feature:

```
SPX down 10% in one day → DC worth $0 → You lost the debit. Done.
You did NOT lose $5,500 per contract like a short straddle would.
```

The post-transformation IC is also floored — you can't lose more than break-even (or a tiny profit) regardless of what SPX does.

### Why No Hard Stop Loss on the IC

After transformation, there is literally nothing to stop-loss. The position is mathematically guaranteed to be profitable at expiration. The only "management" is deciding whether to close early for convenience.

### Buying Power Recycling

One underappreciated aspect of this strategy: **your buying power comes back fully after transformation.**

```
Before transformation:
  - DC costs $1,000 debit
  - Broker also ties up margin for the short options (variable)
  
After transformation:
  - IC is a defined-risk position
  - Margin = wing width × $100 = $500 per contract (for 5-wide wings)
  - The $1,000 DC buying power is replaced by $500 IC margin
  - Net: MORE buying power available than before
```

This allows you to run more trades simultaneously as the strategy progresses.

---

## 10. Results & Statistics

### Steve Bernich — Feb–Apr 2026 Real Results

| Metric | Value |
|--------|-------|
| **Total profit** | $66,000+ |
| **Number of trades** | 106 |
| **Win rate** | 63% |
| **Transformation rate** | ~60% of trades successfully transformed |
| **Period** | February 2026 – April 2026 (≈ 3 months) |
| **Average profit per trade** | ~$623 (on winning trades) |

### Interpreting the 63% Win Rate

A "win" in Steve's tracking appears to include both:
- Successfully transformed ICs (guaranteed minimum profit)
- Profitably closed DCs that weren't transformed

Approximately 60% of trades reached the transformation threshold, meaning 37% were either closed early (at small loss or gain) or expired without reaching the 5–10% profit trigger.

### Average Return per Trade

```
$66,000 ÷ 106 trades = $623 average profit per trade
Running at 3–5 trades per week: 
  Low: 3/week × $623 × 12 weeks = $22,428
  High: 5/week × $623 × 12 weeks = $37,380
```

Scaling up (2 contracts, account allowing) effectively doubles this.

---

## 11. Common Mistakes

### Mistake 1: Entering When Ratio Is Still Rising

**What happens:** You enter the DC hoping the ratio has peaked. It hasn't. IV keeps rising in the front, calendar loses value, you hit your mental stop.

**Fix:** Wait for the ratio to clearly peak and start falling. Patience beats premature entry.

---

### Mistake 2: Not Setting the Transformer Order Immediately

**What happens:** DC reaches 8% profit. You're away from the computer. By the time you're back, the DC has pulled back to flat. Transformation opportunity missed.

**Fix:** The moment you enter the DC, set the transformer order as GTC. It works while you sleep.

---

### Mistake 3: Setting the Transformer Credit Too Low

**What happens:** Transformer fills at $800 credit on a $1,000 debit. Net credit = $800. Wing cost = $500. Break-even = $300. You've left yourself open to a $300 loss if IC goes to max loss.

**Fix:** Always verify: Transformer credit ≥ (DC debit) + (wing width × $100). Use the formula. Don't estimate.

---

### Mistake 4: Using the Wrong Wing Width

**What happens:** You use 10-point wings but set the credit threshold for 5-point wings. Required credit should be $1,500 (debit + $1,000) but you accept $1,300. Not risk-free.

**Fix:** Double-check wing width and recalculate required credit every time.

---

### Mistake 5: Entering Before a Known Catalyst

**What happens:** You enter a DC 2 hours before FOMC. IV spikes massively. Front IV explodes. Calendar initially profitable, then SPX moves 50 points in 5 minutes. DC loses value fast.

**Fix:** Check the economic calendar. Avoid entering DCs within 2–3 hours of: FOMC decisions, CPI/PCE releases, NFP (jobs report), major Fed speeches.

---

### Mistake 6: Oversizing

**What happens:** You put on 10 contracts of DC at $1,500 debit each = $15,000 at risk. Market doesn't cooperate. You lose $3,000 (20% mental stop × 10 contracts). This is 30% of a $10,000 account.

**Fix:** Position size conservatively. 1–2 contracts is fine when learning. The strategy's edge comes from consistency, not from big bets.

---

### Mistake 7: Legging into the Double Calendar

**What happens:** You sell the front legs first, wait for a better price on the back legs. Front IV shifts. You end up with a worse entry than if you'd done it as a combo.

**Fix:** Always enter as a single 4-leg combo order. Pay a little extra in slippage to get the hedge locked in simultaneously.

---

### Mistake 8: Closing the IC After Transformation

**What happens:** SPX moves toward your short strike after transformation. You panic-close the IC at a loss. You forgot: you can't lose money on it.

**Fix:** If you're transformed, do not close the IC out of fear. Review the math. The worst-case outcome is already locked in as a profit (or break-even).

---

### Mistake 9: Not Using SPX (Using SPY Instead)

**What happens:** You use SPY to get cheaper options (1/10th the notional). American-style exercise means you can be assigned on short legs. Also, tax treatment is worse.

**Fix:** Use SPX. The higher notional is a feature, not a bug — it ensures liquid options and the ideal tax treatment.

---

### Mistake 10: Ignoring the Flux Ratio

**What happens:** You enter DCs at random without checking the ratio. Some work, many don't. Win rate drops below 50%.

**Fix:** The Flux ratio is what makes this strategy work. Only enter when the ratio is elevated and falling. No exceptions.

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| **ATM** | At-the-money. An option whose strike price is equal (or very close) to the current price of the underlying asset. |
| **Back expiration** | The longer-dated of the two expirations in the double calendar. You buy (go long) these options. |
| **Black Swan** | An extreme, unexpected market event (e.g., 2008 crash, COVID March 2020). |
| **Buying power** | The amount of capital a brokerage allows you to deploy based on margin requirements. |
| **Calendar spread** | A position where you buy and sell options at the same strike but different expirations. Profits from the difference in time decay rates. |
| **Cash-settled** | Options where settlement is in cash, not shares. SPX is cash-settled. |
| **Delta** | A measure of how much an option's price moves when the underlying moves $1. A 35-delta option moves ~$0.35 per $1 move in the underlying. Also approximates the probability of expiring in-the-money. |
| **DC** | Double Calendar spread — a calendar on both the put side and the call side simultaneously. |
| **DTE** | Days to expiration. The number of calendar days until the option expires. |
| **European-style** | Options that can only be exercised at expiration (not before). Eliminates early assignment risk. |
| **Front expiration** | The shorter-dated of the two expirations in the double calendar. You sell (go short) these options. |
| **Flux tool** | A custom charting application developed as part of the DC Time Machine strategy that tracks and displays front/back IV and their ratio. |
| **GTC** | Good Till Cancelled. An order that remains active until it fills or you cancel it. |
| **Implied Volatility (IV)** | The market's expectation of future volatility, derived from option prices. Higher IV = more expensive options. |
| **Iron Condor (IC)** | A four-leg options strategy: short put spread + short call spread. Profits when the underlying stays within a range. Defined risk. |
| **Max loss** | The maximum amount you can lose on a defined-risk position. For a DC: the debit paid. For an IC: the wing width × $100. |
| **Mean reversion** | The tendency of a metric (like the IV ratio) to return to its average value after deviating. |
| **Mental stop** | A self-imposed loss limit that triggers a position close — not automated, requires discipline. |
| **Ornstein-Uhlenbeck** | A mean-reverting stochastic process used in quantitative finance to model IV dynamics. |
| **OTM** | Out-of-the-money. An option with no intrinsic value (put strike below market, call strike above market). |
| **Risk-free position** | A position where the worst-case outcome is break-even or better. The DC Time Machine achieves this after the Transformer order. |
| **Section 1256** | U.S. tax code section governing futures contracts and certain options (including SPX). Provides 60/40 long-term/short-term tax treatment. |
| **Theta** | Time decay. The rate at which an option loses value as time passes, all else equal. Sellers of options benefit from theta. |
| **Transformer order** | The 4-leg combo order that converts a profitable double calendar into a risk-free iron condor. Must be entered for a net credit ≥ original debit + wing cost. |
| **Vega** | Sensitivity of an option's price to changes in implied volatility. Calendar spreads have positive vega — they benefit from rising IV in the back month relative to the front. |
| **Wing** | The protective long option added to convert a short option into a credit spread. The "wing" limits maximum loss. |

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║              DC TIME MACHINE — QUICK REFERENCE               ║
╠══════════════════════════════════════════════════════════════╣
║  ENTRY                                                       ║
║  • Wait for Flux orange ratio: elevated + falling            ║
║  • Strikes: 30–40 delta put + 30–40 delta call               ║
║  • Expirations: front (sell) + back (buy), 1-day gap         ║
║  • Order: 4-leg combo, debit, $800–$1,500 typical            ║
╠══════════════════════════════════════════════════════════════╣
║  TRANSFORMER (set immediately as GTC)                        ║
║  • Sell back long put + sell back long call                  ║
║  • Buy front OTM put wing + buy front OTM call wing          ║
║  • Required credit = DC debit + (wing points × $100)         ║
║  • 5-wide wings: credit ≥ DC debit + $500                    ║
╠══════════════════════════════════════════════════════════════╣
║  MANAGEMENT                                                   ║
║  • DC mental stop: −20% of debit paid                        ║
║  • Post-IC: no management needed (risk-free)                 ║
║  • Target transformation at 5–10% DC profit                  ║
╠══════════════════════════════════════════════════════════════╣
║  SPX ADVANTAGES                                              ║
║  • European style: no assignment risk                        ║
║  • 60/40 tax treatment (Section 1256)                        ║
║  • MWF weekly expirations                                    ║
║  • Deep liquidity, tight spreads                             ║
╠══════════════════════════════════════════════════════════════╣
║  RESULTS (Feb–Apr 2026)                                      ║
║  • $66k+ profit | 106 trades | 63% win rate                  ║
║  • ~60% of trades successfully transformed                   ║
╚══════════════════════════════════════════════════════════════╝
```

---

*This guide is for educational purposes. Options trading involves substantial risk of loss. Past results (including Steve Bernich's Feb–Apr 2026 results) are not indicative of future performance. Always paper trade a strategy before committing real capital.*
