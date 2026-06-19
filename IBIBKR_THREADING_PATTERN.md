# ib_insync Thread-Safe Pattern — Complete Reference

## The Problem
`ib_insync.IB` manages its own asyncio event loop and is **NOT thread-safe**. Direct calls from background threads cause:
```
RuntimeWarning: coroutine 'IB.qualifyContractsAsync' was never awaited
RuntimeWarning: coroutine 'IB.reqHistoricalDataAsync' was never awaited
```

## The Solution: Dedicated Event Loop Thread
Run IB's event loop on a dedicated thread, marshal all calls to that thread via `asyncio.run_coroutine_threadsafe()`.

### Pattern 1: Initialize & Connect

```python
class IBKRProvider:
    def __init__(self, host="127.0.0.1", port=7497):
        self.ib = IB()
        self._connected = False
        self._ib_thread = None
        self._connect()

    def _connect(self):
        """Start IB event loop on dedicated thread, then connect."""
        try:
            # 1. Start IB's event loop on a dedicated thread
            self._ib_thread = threading.Thread(target=self._run_ib_loop, daemon=True)
            self._ib_thread.start()
            time.sleep(0.5)  # Let loop initialize
            
            # 2. Connect (uses ibutil.run_in_background)
            ibutil.run_in_background(self.ib.connectAsync, host, port, client_id)
            self.ib.sleep(2)  # Wait for connection
            self._connected = self.ib.isConnected()
        except Exception as e:
            self._connected = False

    def _run_ib_loop(self):
        """Run IB event loop forever (blocking)."""
        try:
            self.ib.run()  # Blocks forever on this thread
        except Exception as e:
            print(f"Event loop error: {e}")
```

### Pattern 2: Synchronous Wrapper + Async Implementation

**For simple operations:**

```python
def get_contract_info(self, symbol: str) -> Optional[Contract]:
    """PUBLIC: Blocking synchronous method (any thread can call)."""
    if not self.is_connected:
        return None
    try:
        # Marshal to IB thread, wait for result
        result = ibutil.run(self._get_contract_info_async(symbol))
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

async def _get_contract_info_async(self, symbol: str) -> Optional[Contract]:
    """PRIVATE: Async implementation (runs on IB thread)."""
    try:
        contract = Contract(symbol=symbol, exchange="SMART", secType="STK")
        qualified = self.ib.qualifyContracts(contract)  # Safe IB call on IB thread
        return qualified[0] if qualified else None
    except Exception:
        return None
```

**For complex operations returning DataFrames:**

```python
def get_historical_data(self, symbol: str, days: int) -> pd.DataFrame:
    """PUBLIC: Blocking synchronous method."""
    if not self.is_connected:
        return pd.DataFrame()
    try:
        result = ibutil.run(self._get_historical_data_async(symbol, days))
        return result if result is not None else pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

async def _get_historical_data_async(self, symbol: str, days: int) -> pd.DataFrame:
    """PRIVATE: Async implementation."""
    try:
        from ib_insync import Contract
        contract = Contract(symbol=symbol, exchange="SMART", secType="STK")
        contracts = self.ib.qualifyContracts(contract)
        if not contracts:
            return pd.DataFrame()
        
        # All IB calls here are safe (we're on IB thread)
        bars = self.ib.reqHistoricalData(
            contracts[0],
            endDateTime="",
            durationStr=f"{days} D",
            barSizeSetting="1 day",
            whatToShow="TRADES",
            useRTH=True,
            formatDate=1
        )
        
        if not bars:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = ibutil.df(bars)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
```

### Pattern 3: Direct Event Loop Submission (Alternative)

If you need more control, use `asyncio.run_coroutine_threadsafe()` directly:

```python
async def _update_price_async(self):
    """Async work on IB thread."""
    # Do IB calls...
    pass

def update_price_from_anywhere(self):
    """Can be called from any thread."""
    if not self.ib.loop:
        return
    future = asyncio.run_coroutine_threadsafe(
        self._update_price_async(),
        self.ib.loop
    )
    # Optionally wait for result:
    try:
        result = future.result(timeout=5)  # Block up to 5 seconds
    except concurrent.futures.TimeoutError:
        print("Timeout")
```

### Pattern 4: For Each Major IB Operation

| Operation | Wrapping Pattern |
|-----------|------------------|
| Qualify contracts | `ibutil.run(self._qualify_async())` → `ib.qualifyContracts()` |
| Request market data | `ibutil.run(self._get_market_data_async())` → `ib.reqMktData()` |
| Historical data | `ibutil.run(self._get_historical_async())` → `ib.reqHistoricalData()` |
| Option chains | `ibutil.run(self._get_chains_async())` → `ib.reqSecDefOptParams()` |
| Place order | `ibutil.run(self._place_order_async())` → `ib.placeOrder()` |

## Key Principles

1. **Public API is always synchronous**
   - Caller sees: `data = provider.get_data()` (returns immediately or blocks)
   - Never expose async/await to the caller

2. **All IB calls in async methods**
   - `_get_data_async()` contains `ib.qualifyContracts()`, `ib.reqHistoricalData()`, etc.
   - Safe because async methods run on IB's event loop thread

3. **Marshal via `ibutil.run()`**
   - `ibutil.run(coro)` internally calls `asyncio.run_coroutine_threadsafe(coro, self.ib.loop)`
   - Blocks caller until result ready
   - Thread-safe

4. **No direct IB calls from caller threads**
   - ❌ Don't: `result = ib.qualifyContracts(contract)` from any non-IB thread
   - ✅ Do: `result = ibutil.run(self._qualify_async())`

5. **Daemon thread is fine**
   - `daemon=True` means IB thread exits when main program exits
   - Since IB loop runs forever, it won't naturally exit anyway

## Error Handling

```python
def safe_method(self):
    if not self.is_connected:
        return default_value
    try:
        result = ibutil.run(self._async_impl())
        return result if result is not None else default_value
    except Exception as e:
        print(f"[IBError] {e}")
        return default_value
```

## Connectivity Check

```python
@property
def is_connected(self) -> bool:
    """Safe to call from any thread."""
    return self._connected and self.ib.isConnected()
```

## Testing Checklist

- [ ] No "coroutine was never awaited" warnings
- [ ] No thread-related race conditions or hangs
- [ ] Calling same method from multiple threads works
- [ ] Connection status updates correctly
- [ ] All data operations (qualify, historical, market data) work
- [ ] Graceful fallback when disconnected
- [ ] UI remains responsive during long IB operations

---

## Why This Works

1. **Dedicated thread owns event loop**: The `_run_ib_loop()` thread runs `ib.run()`, which blocks forever managing the event loop
2. **Thread-safe submission**: `asyncio.run_coroutine_threadsafe()` safely submits coroutines from any thread
3. **Synchronous API**: `ibutil.run()` waits for the coroutine to complete before returning, giving callers a simple blocking interface
4. **No context switching**: IB code always runs on the same event loop thread, eliminating race conditions

This pattern is the **standard way** to use `ib_insync` from a multi-threaded application.

---

**Reference**: [ib_insync GitHub — Threading](https://github.com/IbKr/ib_insync)  
**Applied to**: `flux_tool.py` IBKRIVProvider class
