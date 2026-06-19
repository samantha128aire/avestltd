# Flux Tool Threading Fix — Verification Checklist

## Compilation ✓
- [x] Python syntax check: `py_compile` passes
- [x] No import errors (asyncio added)
- [x] No undefined references

## Architecture Changes

### Before (Broken)
```
Main Thread (matplotlib UI)
  ├─ _refresh_loop() [BG thread]
  │  └─ get_ivs() → _get_atm_iv() → ib.reqMktData() ❌ Wrong thread!
  └─ _bg_fetch_hist() [BG thread]
     └─ get_historical() → ib.reqHistoricalData() ❌ Wrong thread!

IB Event Loop (main thread, never runs)
  └─ Broken because event loop isn't being run
```

**Problem**: IB object's asyncio event loop never starts. Background threads call blocking IB methods from wrong thread context, breaking async semantics.

### After (Fixed)
```
IB Thread (dedicated, runs forever)
  └─ self.ib.run() → manages asyncio event loop

Main Thread (matplotlib UI)
  └─ ibutil.run(coro) → asyncio.run_coroutine_threadsafe()
     └─ Submits coroutine to IB thread, waits for result

Background Threads (_refresh_loop, _bg_fetch_hist, etc.)
  └─ ibutil.run(coro) → asyncio.run_coroutine_threadsafe()
     └─ Submits coroutine to IB thread, waits for result
```

**Solution**: IB event loop runs on dedicated thread. All callers (any thread) marshal calls through `ibutil.run()`, which internally uses `asyncio.run_coroutine_threadsafe()`.

---

## Method-by-Method Verification

### 1. `_connect()` and `_run_ib_loop()` ✓
- [x] `_ib_thread` spawned as daemon thread
- [x] Calls `self.ib.run()` to start event loop
- [x] Waits 0.5s for loop to initialize
- [x] Uses `ibutil.run_in_background()` for async connection

### 2. `available_expirations()` ✓
- [x] Public method remains synchronous
- [x] Calls `ibutil.run(self._get_expirations_impl())`
- [x] `_get_expirations_impl()` is async, calls IB on event loop
- [x] Blocks until result returns to caller

### 3. `get_ivs()` ✓
- [x] Public synchronous method
- [x] Calls `ibutil.run(self._get_ivs_async())`
- [x] `_get_ivs_async()` awaits both `_get_atm_iv_async()` calls
- [x] All IB calls isolated to async implementation

### 4. `get_historical()` ✓
- [x] Public synchronous method
- [x] Calls `ibutil.run(self._get_historical_async(days))`
- [x] `_get_historical_async()` does all IB work
- [x] All `ib.qualifyContracts()`, `ib.reqHistoricalData()` on event loop

### 5. `scanner_data()` ✓
- [x] Public synchronous method
- [x] Calls `ibutil.run(self._scanner_data_async())`
- [x] `_scanner_data_async()` handles all IB operations
- [x] Calls `await self._get_expirations_impl()` for list

### 6. `_resolve_option_contract()` ✓
- [x] Internal method, still synchronous
- [x] Calls `ibutil.run(self._resolve_option_contract_async())`
- [x] Async version does `ib.qualifyContracts()` safely

### 7. `_get_atm_iv()` ✓
- [x] Internal method, synchronous wrapper
- [x] Calls `ibutil.run(self._get_atm_iv_async())`
- [x] Async version handles `ib.reqMktData()`

### 8. `set_symbol()` ✓
- [x] Checks `self.ib.loop` exists
- [x] Uses `asyncio.run_coroutine_threadsafe()` directly
- [x] Updates price via async wrapper

---

## No Breaking Changes ✓

| Component | Before | After | Breaking? |
|-----------|--------|-------|-----------|
| `FluxApp` | Calls `provider.get_ivs()` | Same call | ✓ No |
| `FluxApp._bg_fetch_hist()` | Calls `provider.get_historical(5)` | Same call | ✓ No |
| `FluxApp._bg_fetch_scanner()` | Calls `provider.scanner_data()` | Same call | ✓ No |
| `FluxApp._on_symbol_change()` | Calls `provider.set_symbol()` | Same call | ✓ No |
| `MockIVProvider` | Untouched | Untouched | ✓ No |
| CLI interface | `python flux_tool.py --ibkr` | Same command | ✓ No |

---

## Expected Behavior After Fix

### Demo Mode (No IBKR)
```bash
python3 flux_tool.py --demo
```
- Simulated data, unaffected
- Should work exactly as before

### Live Mode (IBKR Connected)
```bash
python3 flux_tool.py --ibkr --host 127.0.0.1 --port 7496
```
- ✓ Status dot pulses green (connected)
- ✓ Scanner populates with top 20 ratio pairs
- ✓ 5-day and 20-day historical views load
- ✓ Intraday IV chart updates smoothly
- ✓ No "RuntimeWarning: coroutine was never awaited" messages
- ✓ Symbol changes refresh data
- ✓ Expiration selectors update IV streams

### Live Mode (IBKR Disconnected)
```bash
python3 flux_tool.py --ibkr --host 127.0.0.1 --port 9999  # Wrong port
```
- ✓ Status dot stays red (disconnected)
- ✓ Mock data falls back gracefully
- ✓ UI remains responsive
- ✓ No crashes or hung threads

---

## Thread Safety Guarantees

1. **IB Event Loop Thread**
   - Only thread where `self.ib` methods are called
   - Runs `self.ib.run()` forever (blocking call)
   - Never touched by UI or background threads

2. **Main Thread (matplotlib)**
   - Calls `ibutil.run(coro)` → marshals to IB thread
   - Blocks until result ready (via `asyncio.run_coroutine_threadsafe()`)
   - Never calls `ib.*()` directly

3. **Background Threads** (_refresh_loop, _bg_fetch_hist, _bg_fetch_scanner)
   - Same pattern: `ibutil.run(coro)` → marshals to IB thread
   - Blocks until result ready
   - Never call `ib.*()` directly

4. **Shared State**
   - `self._spx_price`: updated from IB thread (safe)
   - `self._front_exp`, `self._back_exp`: read-only during IB calls (safe)
   - `self._symbol`: read-only during IB calls (safe)
   - `self._connected`: simple flag (safe enough for polling)

---

## Final Status
✅ **READY FOR TESTING**

All methods fixed. All IB calls marshalled to dedicated event loop thread. Public API unchanged. No breaking changes.

**Next step**: Start TWS (live or paper) and run:
```bash
python3 /Users/sam/.openclaw/workspace/flux_tool.py --ibkr --host 127.0.0.1 --port 7496
```

Watch for:
- Green pulsing status dot
- Scanner table populates
- No coroutine warnings in console
- Smooth UI interaction
