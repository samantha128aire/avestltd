# Flux Tool Threading Fix — Summary

## Problem
The original `IBKRIVProvider` class was calling `ib_insync.IB` methods from multiple background threads:
- `_bg_fetch_hist()` → `get_historical()` (background thread)
- `_bg_fetch_scanner()` → `scanner_data()` (background thread)
- `_refresh_loop()` → `get_ivs()` (background thread)
- `_on_symbol_change()` → `set_symbol()` → `_update_underlying_price()` (various threads)

This caused:
```
RuntimeWarning: coroutine 'IB.qualifyContractsAsync' was never awaited
```

The root cause: **`ib_insync.IB` manages its own asyncio event loop and is NOT thread-safe**. Calling it from threads other than its own event loop thread breaks the async semantics.

## Solution
Redesigned `IBKRIVProvider` to run the IB object's event loop on a **dedicated thread**, and marshal all IB calls to that loop from other threads using `ibutil.run()` (which internally uses `asyncio.run_coroutine_threadsafe()`).

### Key Changes

#### 1. **Dedicated IB Event Loop Thread**
```python
def _connect(self):
    self._ib_thread = threading.Thread(target=self._run_ib_loop, daemon=True)
    self._ib_thread.start()
    time.sleep(0.5)  # Let loop start
    # Connect via ibutil.run_in_background()

def _run_ib_loop(self):
    self.ib.run()  # Runs forever on this thread
```

The IB event loop now runs on its own dedicated thread, unblocking the main/UI thread and background workers.

#### 2. **Async/Sync Marshalling Pattern**
Every public method that calls IB is now a **blocking synchronous wrapper** that internally calls an async version via `ibutil.run()`:

```python
# Public API (blocks, safe from any thread)
def get_historical(self, days: int) -> pd.DataFrame:
    result = ibutil.run(self._get_historical_async(days))
    return result

# Private async implementation (runs on IB's event loop)
async def _get_historical_async(self, days: int) -> pd.DataFrame:
    # Direct IB calls here — safe because we're on IB's thread
    contracts = self.ib.qualifyContracts(underlying)
    bars = self.ib.reqHistoricalData(...)
    # ... process and return
```

This pattern ensures:
- Caller sees synchronous API: `provider.get_historical(5)` returns DataFrame
- Internally, all IB calls happen on the correct event loop thread
- No thread-safety issues, no "coroutine was never awaited" warnings

#### 3. **Methods Fixed**

| Method | Type | Before | After |
|--------|------|--------|-------|
| `get_historical()` | Public sync | Called from BG thread ❌ | Marshalled to IB loop ✓ |
| `scanner_data()` | Public sync | Called from BG thread ❌ | Marshalled to IB loop ✓ |
| `get_ivs()` | Public sync | Called from BG thread ❌ | Marshalled to IB loop ✓ |
| `_get_atm_iv()` | Internal | Direct IB calls ❌ | Async + marshalled ✓ |
| `_resolve_option_contract()` | Internal | Direct IB calls ❌ | Async + marshalled ✓ |
| `available_expirations()` | Public sync | Direct IB calls ❌ | Async + marshalled ✓ |
| `set_symbol()` | Public sync | Direct IB calls ❌ | Uses `asyncio.run_coroutine_threadsafe()` ✓ |

Each now has a corresponding `*_async()` implementation that runs on the IB event loop.

#### 4. **Imports**
Added `import asyncio` at the top to support the new async patterns.

## API Contract (Unchanged)
All public methods remain **synchronous and blocking**. Callers don't see async/await:

```python
provider = IBKRIVProvider(host="127.0.0.1", port=7497)
exps = provider.available_expirations()  # Still blocks, waits for result
ivs = provider.get_ivs()  # Still blocks
hist = provider.get_historical(5)  # Still blocks
scanner = provider.scanner_data()  # Still blocks
```

The threading and async machinery is **hidden** inside the implementation.

## Testing Recommendations
1. **Verify syntax**: `python3 -m py_compile flux_tool.py` ✓
2. **Run against TWS**: Start TWS on 127.0.0.1:7496 (live) or 7497 (paper)
   ```bash
   python3 flux_tool.py --ibkr --host 127.0.0.1 --port 7496
   ```
3. **Check data flow**:
   - Scanner should populate (not empty DataFrame)
   - Historical data should load for 5-day and 20-day views
   - No "RuntimeWarning: coroutine was never awaited" messages
   - Connection indicator should pulse green when connected

## Compatibility
- ✅ No breaking changes to `FluxApp` or any caller code
- ✅ `MockIVProvider` untouched (still works for demo mode)
- ✅ matplotlib UI threading unchanged
- ✅ Requires ib_insync with `util.run()` support (standard)

---
**Fixed by:** Subagent  
**Date:** June 13, 2026  
**Status:** Ready for testing against live TWS
