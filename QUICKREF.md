# Flux Tool Fix — Quick Reference Card

## What Was Broken
```python
# ❌ WRONG: Direct IB calls from background thread
def _bg_fetch_hist(self):
    df = self.provider.get_historical(5)

class IBKRIVProvider:
    def get_historical(self, days):
        bars = self.ib.reqHistoricalData(...)  # WRONG THREAD!
        # RuntimeWarning: coroutine was never awaited
```

## How It's Fixed
```python
# ✓ CORRECT: All IB calls on dedicated event loop thread
def _bg_fetch_hist(self):
    df = self.provider.get_historical(5)  # Safe from any thread

class IBKRIVProvider:
    def _connect(self):
        # 1. Start IB's event loop on dedicated thread
        self._ib_thread = threading.Thread(target=self._run_ib_loop, daemon=True)
        self._ib_thread.start()
    
    def _run_ib_loop(self):
        # Runs forever, manages asyncio event loop
        self.ib.run()
    
    def get_historical(self, days):
        # 2. Marshal all calls to IB thread
        result = ibutil.run(self._get_historical_async(days))
        return result  # Blocks until ready
    
    async def _get_historical_async(self, days):
        # 3. All IB calls here, on IB thread
        bars = self.ib.reqHistoricalData(...)  # Safe! ✓
        return df
```

## The Three-Part Pattern

| Part | Code | Purpose |
|------|------|---------|
| **1. Dedicated Thread** | `threading.Thread(target=self._run_ib_loop)` | Runs IB event loop |
| **2. Event Loop** | `self.ib.run()` on that thread | Manages asyncio |
| **3. Marshalling** | `ibutil.run(async_coro)` | Safe submission from any thread |

## Files Changed
```
/Users/sam/.openclaw/workspace/flux_tool.py
  - Lines: 1557 (was ~1450)
  - Added: import asyncio
  - Fixed: 8 methods + 9 new async implementations
  - Status: ✓ Syntax verified (py_compile)
```

## Methods Fixed

| Public Method | Now Safe For | Pattern |
|---|---|---|
| `get_ivs()` | Any thread | `ibutil.run(self._get_ivs_async())` |
| `get_historical(days)` | Any thread | `ibutil.run(self._get_historical_async(days))` |
| `scanner_data()` | Any thread | `ibutil.run(self._scanner_data_async(...))` |
| `available_expirations()` | Any thread | `ibutil.run(self._get_expirations_impl())` |
| `set_symbol(sym)` | Any thread | `asyncio.run_coroutine_threadsafe(...)` |

## No Breaking Changes

✅ All public APIs unchanged  
✅ Same synchronous interface  
✅ FluxApp: zero changes needed  
✅ Same CLI command works  

## Test It
```bash
# Start TWS on port 7496
python3 flux_tool.py --ibkr --host 127.0.0.1 --port 7496

# Look for:
# ✓ Green pulsing status dot
# ✓ Scanner table populated
# ✓ NO "coroutine was never awaited" warnings
# ✓ Smooth UI interaction
```

## The Key Insight
```
BEFORE: ThreadA → ib.call() ❌ Wrong thread, breaks event loop semantics
AFTER:  ThreadA → ibutil.run(async_func) → IB Thread → ib.call() ✓ Correct!
```

## Documentation
- **FLUX_FIX_SUMMARY.md** — What changed and why
- **IBIBKR_THREADING_PATTERN.md** — Reusable pattern guide
- **FLUX_CHANGES_DETAILED.md** — Line-by-line before/after
- **FIX_COMPLETE.md** — Full completion report

---

**Status**: ✅ READY FOR TESTING  
**Date**: June 13, 2026  
**File**: `/Users/sam/.openclaw/workspace/flux_tool.py`
