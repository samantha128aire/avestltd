#!/usr/bin/env python3
"""
Flux Tool v2 - DC Time Machine IV Ratio Charting Tool
Recreates Steve Bernich's "Flux" tool for tracking front/back expiration IV ratios.

NEW in v2:
  - Symbol selector (SPX, SPY, NDX, QQQ, RUT, IWM)
  - Front / Back expiration date selectors (populated from available option expirations)
  - Live connection status indicator (pulsing green dot = connected, red = demo/disconnected)

pip dependencies:
    pip install matplotlib numpy pandas yfinance ib_insync

Run in demo/mock mode (no brokerage needed):
    python flux_tool.py --demo

Run with IBKR TWS (paper or live, TWS must be running):
    python flux_tool.py --ibkr --host 127.0.0.1 --port 7497
"""

import argparse
import asyncio
import datetime
import math
import random
import sys
import threading
import time
from collections import deque
from typing import List, Optional, Tuple

import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.ticker
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, TextBox
import numpy as np
import pandas as pd

try:
    from ib_insync import IB, Index, Option, util as ibutil
    IBKR_AVAILABLE = True
except ImportError:
    IBKR_AVAILABLE = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MARKET_OPEN    = datetime.time(9, 30)
MARKET_CLOSE   = datetime.time(16, 0)
REFRESH_SEC    = 60
MAX_INTRADAY   = 390

SUPPORTED_SYMBOLS = ["SPX", "SPY", "NDX", "QQQ", "RUT", "IWM"]

BG_DARK   = "#1a1a2e"
BG_CHART  = "#0f0f23"
PANEL_BG  = "#12122a"
BTN_NORM  = "#2a2a4e"
BTN_HOV   = "#4a4a8e"
BTN_ACTV  = "#5555aa"
COL_BLUE  = "#4488ff"
COL_GREEN = "#44cc44"
COL_ORNG  = "#ff8800"
COL_TICK  = "#aaaaaa"
COL_SPINE = "#333355"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _next_weekday_expirations(n: int = 16) -> List[str]:
    """Generate the next n option expiration dates (Mon/Wed/Thu/Fri — excludes Sat/Sun).
    Thursdays are included for monthly OPEX (e.g. 3rd Thursday index settlements).
    """
    exps = []
    d = datetime.date.today()
    while len(exps) < n:
        d += datetime.timedelta(days=1)
        if d.weekday() in (0, 2, 3, 4):   # Mon=0, Wed=2, Thu=3, Fri=4
            exps.append(d.strftime("%Y-%m-%d"))
    return exps


def _dte(exp_str: str) -> int:
    d = datetime.datetime.strptime(exp_str, "%Y-%m-%d").date()
    return max(0, (d - datetime.date.today()).days)

# ---------------------------------------------------------------------------
# Mock IV Provider
# ---------------------------------------------------------------------------

class MockIVProvider:
    """Simulated IV data for demo mode. Uses Ornstein-Uhlenbeck mean-reversion."""

    def __init__(self):
        self._symbol      = "SPX"
        self._front_exp   = None
        self._back_exp    = None
        self._front_iv    = 0.18
        self._back_iv     = 0.16
        self._t           = 0
        random.seed(42)
        self._spike_at    = random.randint(40, 80)
        self._connected   = True          # always "connected" in demo
        self._last_update = datetime.datetime.now()

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def connection_label(self) -> str:
        return "DEMO MODE"

    @property
    def last_update(self) -> datetime.datetime:
        return self._last_update

    def set_symbol(self, symbol: str):
        self._symbol = symbol
        self._front_iv = random.uniform(0.15, 0.22)
        self._back_iv  = random.uniform(0.13, 0.19)
        self._t        = 0
        self._spike_at = random.randint(30, 90)

    def set_expirations(self, front_exp: str, back_exp: str):
        self._front_exp = front_exp
        self._back_exp  = back_exp

    def available_expirations(self) -> List[str]:
        return _next_weekday_expirations(20)

    def _ou(self, x, mu, theta=0.08, sigma=0.004):
        return x + theta * (mu - x) + sigma * random.gauss(0, 1)

    def get_ivs(self) -> Tuple[float, float]:
        self._t += 1
        spike = 0.0
        d = self._t - self._spike_at
        if -5 <= d <= 12:
            spike = 0.018 * math.exp(-0.25 * max(0, d))

        self._front_iv = max(0.05, self._ou(self._front_iv, 0.18) + spike)
        self._back_iv  = max(0.05, self._ou(self._back_iv,  0.16, theta=0.06, sigma=0.003))
        self._last_update = datetime.datetime.now()
        return self._front_iv, self._back_iv

    def get_historical(self, days: int) -> pd.DataFrame:
        rows, f, b = [], 0.18, 0.16
        base = datetime.datetime.now() - datetime.timedelta(days=days)
        for d in range(days):
            for m in range(78):   # ~5 bars/hour × 6.5h ≈ 390/5 sparse for speed
                ts = base + datetime.timedelta(days=d, minutes=m * 5)
                f = max(0.05, self._ou(f, 0.18))
                b = max(0.05, self._ou(b, 0.16, theta=0.06, sigma=0.003))
                rows.append({"time": ts, "front_iv": f, "back_iv": b, "ratio": f / b})
        return pd.DataFrame(rows).set_index("time")

    def scanner_data(self, dte_min=0, dte_max=30, min_gap=1) -> pd.DataFrame:
        rows, today = [], datetime.date.today()
        for fte in range(3, dte_max, 3):
            for gap in [1, 2, 3]:
                bte = fte + gap
                if bte > dte_max or gap < min_gap or fte < dte_min:
                    continue
                fiv = random.uniform(0.12, 0.28)
                biv = random.uniform(0.11, 0.22)
                ratio = fiv / biv
                rows.append({
                    "Front Exp":   (today + datetime.timedelta(days=fte)).strftime("%Y-%m-%d"),
                    "Back Exp":    (today + datetime.timedelta(days=bte)).strftime("%Y-%m-%d"),
                    "Front DTE":   fte,
                    "Back DTE":    bte,
                    "Gap":         gap,
                    "Front IV":    f"{fiv:.1%}",
                    "Back IV":     f"{biv:.1%}",
                    "Ratio":       round(ratio, 3),
                    "DC Cost Est": f"${random.randint(700, 1800)}",
                    "Quality":     "⭐⭐⭐" if ratio > 1.15 else ("⭐⭐" if ratio > 1.05 else "⭐"),
                })
        return pd.DataFrame(rows).sort_values("Ratio", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# IBKR Live Provider
# ---------------------------------------------------------------------------

class IBKRIVProvider:
    def __init__(self, host="127.0.0.1", port=7497, client_id=10):
        if not IBKR_AVAILABLE:
            raise RuntimeError("ib_insync not installed. pip install ib_insync")
        self._host        = host
        self._port        = port
        self._client_id   = client_id
        self._connected   = False
        self._symbol      = "SPX"
        self._front_exp   = None
        self._back_exp    = None
        self._spx_price   = 5500.0
        self._last_update = datetime.datetime.now()
        self._lock        = threading.Lock()
        # Each background thread gets its own IB connection via thread-local storage
        self._tls         = threading.local()
        # Establish a primary connection to verify TWS is reachable
        self._connect()

    def _ib(self) -> "IB":
        """Return a per-thread IB connection, creating one if needed.
        ib_insync is NOT thread-safe — each thread must have its own IB instance.
        """
        if not getattr(self._tls, 'ib', None) or not self._tls.ib.isConnected():
            ib = IB()
            # Use a unique clientId per thread to avoid conflicts
            import os
            cid = self._client_id + (hash(threading.current_thread().ident) % 50)
            try:
                ib.connect(self._host, self._port, clientId=cid, timeout=10)
            except Exception as e:
                print(f"[IBKR] Thread connection failed (cid={cid}): {e}")
                return None
            self._tls.ib = ib
        return self._tls.ib

    def _connect(self):
        """Verify TWS is reachable on startup using a simple direct connection."""
        try:
            ib = IB()
            ib.connect(self._host, self._port, clientId=self._client_id, timeout=10)
            if ib.isConnected():
                self._connected = True
                self._tls.ib = ib
                self._update_underlying_price()
                print(f"[IBKR] Connected to {self._host}:{self._port}")
            else:
                self._connected = False
        except Exception as e:
            print(f"[IBKR] Connection failed: {e}")
            self._connected = False

    def _update_underlying_price(self):
        """Fetch current underlying price from IBKR."""
        try:
            ib = self._ib()
            if not ib:
                return
            sym_map = {
                "SPX": ("SPX", "CBOE",    "IND"),
                "SPY": ("SPY", "ARCA",    "STK"),
                "NDX": ("NDX", "NASDAQ",  "IND"),
                "QQQ": ("QQQ", "NASDAQ",  "STK"),
                "RUT": ("RUT", "RUSSELL", "IND"),
                "IWM": ("IWM", "ARCA",    "STK"),
            }
            sym, exch, sec = sym_map.get(self._symbol, ("SPX", "CBOE", "IND"))
            from ib_insync import Contract
            c = Contract(symbol=sym, exchange=exch, secType=sec, currency="USD")
            contracts = ib.qualifyContracts(c)
            if not contracts:
                return
            bars = ib.reqHistoricalData(
                contracts[0], endDateTime='', durationStr='1 D',
                barSizeSetting='1 hour', whatToShow='TRADES',
                useRTH=True, formatDate=1)
            if bars:
                with self._lock:
                    self._spx_price = bars[-1].close
                print(f"[IBKR] {self._symbol} price: {self._spx_price}")
        except Exception as e:
            print(f"[IBKR] Price update failed: {e}")

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def connection_label(self) -> str:
        return f"IBKR LIVE ({self._host}:{self._port})" if self._connected else "IBKR DISCONNECTED"

    @property
    def last_update(self) -> datetime.datetime:
        return self._last_update

    def set_symbol(self, symbol: str):
        self._symbol = symbol
        threading.Thread(target=self._update_underlying_price, daemon=True).start()

    def set_expirations(self, front_exp: str, back_exp: str):
        self._front_exp = front_exp
        self._back_exp  = back_exp

    def available_expirations(self) -> List[str]:
        if not self._connected:
            return _next_weekday_expirations(20)
        try:
            ib = self._ib()
            if not ib:
                return _next_weekday_expirations(20)
            from ib_insync import Contract
            c = Contract(symbol=self._symbol, exchange="CBOE", secType="IND", currency="USD")
            contracts = ib.qualifyContracts(c)
            if not contracts:
                return _next_weekday_expirations(20)
            chains = ib.reqSecDefOptParams(self._symbol, "", "IND", contracts[0].conId)
            if chains:
                today = datetime.date.today()
                exps  = sorted(set(chains[0].expirations))
                return [
                    datetime.datetime.strptime(e, "%Y%m%d").strftime("%Y-%m-%d")
                    for e in exps
                    if datetime.datetime.strptime(e, "%Y%m%d").date() > today
                    and datetime.datetime.strptime(e, "%Y%m%d").weekday() <= 4
                ][:30]
        except Exception as e:
            print(f"[IBKR] available_expirations error: {e}")
        return _next_weekday_expirations(20)

    def _resolve_option_contract(self, exp_str: str, right: str = "C"):
        """Qualify an ATM option contract, handling SPX/SPXW ambiguity."""
        ib = self._ib()
        if not ib:
            return None
        exp_ibkr = datetime.datetime.strptime(exp_str, "%Y-%m-%d").strftime("%Y%m%d")
        with self._lock:
            strike = round(self._spx_price / 5) * 5
        from ib_insync import Contract
        for trading_class in ("SPXW", "SPX", None):
            try:
                if trading_class:
                    opt = Contract(secType='OPT', symbol=self._symbol,
                                   lastTradeDateOrContractMonth=exp_ibkr,
                                   strike=strike, right=right,
                                   exchange='CBOE', currency='USD',
                                   tradingClass=trading_class)
                else:
                    opt = Option(self._symbol, exp_ibkr, strike, right, 'CBOE')
                contracts = ib.qualifyContracts(opt)
                if contracts:
                    return contracts[0]
            except Exception:
                continue
        return None

    def _get_atm_iv(self, exp_str: str, right: str = "C") -> float:
        ib = self._ib()
        if not ib:
            return 0.18
        contract = self._resolve_option_contract(exp_str, right)
        if not contract:
            return 0.18
        ticker = ib.reqMktData(contract, "106", False, False)
        ib.sleep(1.5)
        return ticker.impliedVolatility or 0.18

    def get_ivs(self) -> Tuple[float, float]:
        if not self._connected or not self._front_exp or not self._back_exp:
            return 0.18, 0.16
        try:
            fiv = self._get_atm_iv(self._front_exp)
            biv = self._get_atm_iv(self._back_exp)
            self._last_update = datetime.datetime.now()
            return fiv, biv
        except Exception as e:
            print(f"[IBKR] get_ivs error: {e}")
            return 0.18, 0.16

    def _get_underlying_iv(self) -> Optional[float]:
        """Get current IV from the underlying index (always available on Pro)."""
        try:
            ib = self._ib()
            if not ib:
                return None
            from ib_insync import Contract
            sym_map = {
                "SPX": ("SPX", "CBOE",    "IND"),
                "SPY": ("SPY", "ARCA",    "STK"),
                "NDX": ("NDX", "NASDAQ",  "IND"),
                "QQQ": ("QQQ", "NASDAQ",  "STK"),
                "RUT": ("RUT", "RUSSELL", "IND"),
                "IWM": ("IWM", "ARCA",    "STK"),
            }
            sym, exch, sec = sym_map.get(self._symbol, ("SPX", "CBOE", "IND"))
            c = Contract(symbol=sym, exchange=exch, secType=sec, currency="USD")
            contracts = ib.qualifyContracts(c)
            if not contracts:
                return None
            bars = ib.reqHistoricalData(
                contracts[0], endDateTime="", durationStr="1 D",
                barSizeSetting="1 hour", whatToShow="OPTION_IMPLIED_VOLATILITY",
                useRTH=True, formatDate=1)
            if bars:
                return bars[-1].close
        except Exception as e:
            print(f"[IBKR] get_underlying_iv error: {e}")
        return None

    def get_historical(self, days: int) -> pd.DataFrame:
        """Fetch historical IV from the underlying index, scaled by term structure."""
        if not self._connected:
            return pd.DataFrame(columns=["front_iv", "back_iv", "ratio"])
        try:
            ib = self._ib()
            if not ib:
                return pd.DataFrame(columns=["front_iv", "back_iv", "ratio"])
            from ib_insync import Contract
            sym_map = {
                "SPX": ("SPX", "CBOE",    "IND"),
                "SPY": ("SPY", "ARCA",    "STK"),
                "NDX": ("NDX", "NASDAQ",  "IND"),
                "QQQ": ("QQQ", "NASDAQ",  "STK"),
                "RUT": ("RUT", "RUSSELL", "IND"),
                "IWM": ("IWM", "ARCA",    "STK"),
            }
            sym, exch, sec = sym_map.get(self._symbol, ("SPX", "CBOE", "IND"))
            c = Contract(symbol=sym, exchange=exch, secType=sec, currency="USD")
            contracts = ib.qualifyContracts(c)
            if not contracts:
                return pd.DataFrame(columns=["front_iv", "back_iv", "ratio"])
            bar_size = "1 hour" if days <= 5 else "4 hours"
            bars = ib.reqHistoricalData(
                contracts[0], endDateTime="", durationStr=f"{days} D",
                barSizeSetting=bar_size, whatToShow="OPTION_IMPLIED_VOLATILITY",
                useRTH=True, formatDate=1)
            if not bars:
                print(f"[IBKR] No historical IV bars for {sym}")
                return pd.DataFrame(columns=["front_iv", "back_iv", "ratio"])
            df     = ibutil.df(bars)
            df.index = pd.to_datetime(df["date"])
            raw_iv = df["close"]
            front_dte   = max(1, _dte(self._front_exp)) if self._front_exp else 7
            back_dte    = max(1, _dte(self._back_exp))  if self._back_exp  else 14
            ref_dte     = (front_dte + back_dte) / 2.0
            front_scale = (ref_dte / front_dte) ** 0.5
            back_scale  = (ref_dte / back_dte)  ** 0.5
            combined = pd.DataFrame({
                "front_iv": raw_iv * front_scale,
                "back_iv":  raw_iv * back_scale,
            }).dropna()
            combined["ratio"] = combined["front_iv"] / combined["back_iv"]
            combined.index.name = "time"
            print(f"[IBKR] Historical {days}d: {len(combined)} bars")
            return combined
        except Exception as e:
            print(f"[IBKR] get_historical error: {e}")
            return pd.DataFrame(columns=["front_iv", "back_iv", "ratio"])

    def scanner_data(self, dte_min=1, dte_max=120, min_gap=1) -> pd.DataFrame:
        """Build scanner table ranked by IV ratio using sqrt(T) term structure."""
        if not self._connected:
            return pd.DataFrame()
        try:
            base_iv = self._get_underlying_iv()
            if base_iv is None:
                print("[IBKR] scanner_data: could not get base IV")
                return pd.DataFrame()
            exps  = self.available_expirations()
            today = datetime.date.today()

            def iv_for_dte(d: int) -> float:
                return base_iv * (30.0 / max(1, d)) ** 0.5

            rows = []
            for fi, fexp in enumerate(exps):
                fdte = _dte(fexp)
                if fdte < dte_min or fdte > dte_max:
                    continue
                fiv = iv_for_dte(fdte)
                for bexp in exps[fi + 1:]:
                    bdte = _dte(bexp)
                    if bdte > dte_max:
                        break
                    gap = bdte - fdte
                    if gap < min_gap:
                        continue
                    biv   = iv_for_dte(bdte)
                    ratio = fiv / biv if biv > 0 else 1.0
                    if ratio < 1.0:
                        continue
                    quality = "⭐⭐⭐" if ratio >= 1.20 else ("⭐⭐" if ratio >= 1.08 else "⭐")
                    rows.append({
                        "Front Exp":  fexp,
                        "Back Exp":   bexp,
                        "Front DTE":  fdte,
                        "Back DTE":   bdte,
                        "Gap (days)": gap,
                        "Front IV":   f"{fiv:.1%}",
                        "Back IV":    f"{biv:.1%}",
                        "Ratio":      round(ratio, 3),
                        "Quality":    quality,
                    })
            if not rows:
                print("[IBKR] scanner_data: no rows generated")
                return pd.DataFrame()
            df = pd.DataFrame(rows).sort_values("Ratio", ascending=False).reset_index(drop=True)
            print(f"[IBKR] scanner_data: {len(df)} pairs found")
            return df.head(20)
        except Exception as e:
            print(f"[IBKR] scanner_data error: {e}")
            return pd.DataFrame()


# ---------------------------------------------------------------------------
# Flux Application
# ---------------------------------------------------------------------------

class FluxApp:

    def __init__(self, provider, entry_threshold_pct: float = 0.5):
        self.provider              = provider
        self.entry_threshold_pct   = entry_threshold_pct
        self.times                 = deque(maxlen=MAX_INTRADAY)
        self.front_ivs             = deque(maxlen=MAX_INTRADAY)
        self.back_ivs              = deque(maxlen=MAX_INTRADAY)
        self.ratios                = deque(maxlen=MAX_INTRADAY)
        self._view                 = "intraday"
        self._running              = True
        self._lock                 = threading.Lock()
        self._hist5                = None
        self._hist20               = None
        self._scanner_df           = None
        self._symbol               = SUPPORTED_SYMBOLS[0]
        self._available_exps       = []
        self._front_exp_idx        = 0
        self._back_exp_idx         = 1
        self._pulse_state          = 0   # for connection dot animation
        # Dropdown state
        self._dd_ax        = None
        self._dd_bg        = None
        self._dd_items     = []
        self._dd_which     = None
        self._dd_exps      = []
        self._dd_scroll    = 0
        self._dd_hover     = 0
        self._dd_visible   = 12
        self._dd_row_h     = 0.040
        self._dd_color     = COL_BLUE
        self._dd_cid_click  = None
        self._dd_cid_motion = None
        self._dd_cid_scroll = None

        self._refresh_expirations()
        self._load_historical()
        self._build_figure()
        self._fetch_and_append()

        # Background refresh thread
        self._refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._refresh_thread.start()

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------

    def _refresh_expirations(self):
        self._available_exps = self.provider.available_expirations()
        if len(self._available_exps) < 2:
            self._available_exps = _next_weekday_expirations(20)
        self._front_exp_idx = 0
        self._back_exp_idx  = 1
        self._apply_expirations()

    def _apply_expirations(self):
        fe = self._available_exps[self._front_exp_idx]
        be = self._available_exps[self._back_exp_idx]
        self.provider.set_expirations(fe, be)

    @property
    def _front_exp(self) -> str:
        return self._available_exps[self._front_exp_idx] if self._available_exps else "—"

    @property
    def _back_exp(self) -> str:
        return self._available_exps[self._back_exp_idx] if self._available_exps else "—"

    def _load_historical(self):
        """Load historical + scanner data each in their own background thread."""
        def _fetch_hist():
            h5  = self.provider.get_historical(5)
            h20 = self.provider.get_historical(20)
            with self._lock:
                self._hist5  = h5
                self._hist20 = h20
            if self._view in ("5day", "20day"):
                self._draw()

        def _fetch_scanner():
            sc = self.provider.scanner_data()
            with self._lock:
                self._scanner_df = sc
            if self._view == "scanner":
                self._draw()

        threading.Thread(target=_fetch_hist,    daemon=True).start()
        threading.Thread(target=_fetch_scanner, daemon=True).start()

    def _fetch_and_append(self):
        try:
            fiv, biv = self.provider.get_ivs()
            ratio    = fiv / biv if biv > 0 else 1.0
            now      = datetime.datetime.now()
            with self._lock:
                self.times.append(now)
                self.front_ivs.append(fiv)
                self.back_ivs.append(biv)
                self.ratios.append(ratio)
        except Exception as e:
            print(f"[Flux] Fetch error: {e}")

    def _refresh_loop(self):
        while self._running:
            time.sleep(REFRESH_SEC)
            self._fetch_and_append()
            try:
                self.fig.canvas.draw_idle()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Figure
    # ------------------------------------------------------------------

    def _build_figure(self):
        self.fig = plt.figure(figsize=(15, 9), facecolor=BG_DARK)
        self.fig.canvas.manager.set_window_title("Flux — DC Time Machine IV Ratio Tool v2")

        # ── Layout ──────────────────────────────────────────────────────
        #  Row 0 (thin): top toolbar  — symbol, expirations, status
        #  Row 1 (tall): chart area   — IV panel + ratio panel
        #  Row 2 (thin): bottom bar   — view buttons + threshold
        # ────────────────────────────────────────────────────────────────
        self._gs = gridspec.GridSpec(
            3, 1, figure=self.fig,
            height_ratios=[0.10, 0.82, 0.08],
            hspace=0.04,
        )

        self._gs_charts = gridspec.GridSpecFromSubplotSpec(
            2, 1, subplot_spec=self._gs[1],
            hspace=0.06, height_ratios=[2.2, 1],
        )

        self.ax_iv     = self.fig.add_subplot(self._gs_charts[0])
        self.ax_ratio  = self.fig.add_subplot(self._gs_charts[1], sharex=self.ax_iv)
        self.ax_top    = self.fig.add_subplot(self._gs[0])
        self.ax_bottom = self.fig.add_subplot(self._gs[2])

        for ax in [self.ax_top, self.ax_bottom]:
            ax.set_facecolor(PANEL_BG)
            ax.axis("off")

        self._style_chart_axes()
        self._build_top_toolbar()
        self._build_bottom_toolbar()

    def _style_chart_axes(self):
        for ax in [self.ax_iv, self.ax_ratio]:
            ax.set_facecolor(BG_CHART)
            ax.tick_params(colors=COL_TICK)
            for sp in ax.spines.values():
                sp.set_color(COL_SPINE)
            ax.yaxis.label.set_color(COL_TICK)
            ax.xaxis.label.set_color(COL_TICK)

    # ------------------------------------------------------------------
    # Top Toolbar — Symbol, Expirations, Status
    # ------------------------------------------------------------------

    def _build_top_toolbar(self):
        """Symbol buttons, expiration selectors, connection status."""
        fig = self.fig

        # ── Symbol buttons ────────────────────────────────────────────
        sym_x0  = 0.02
        sym_w   = 0.055
        sym_gap = 0.005
        sym_y   = 0.925
        sym_h   = 0.045

        self._sym_buttons = {}
        for i, sym in enumerate(SUPPORTED_SYMBOLS):
            x    = sym_x0 + i * (sym_w + sym_gap)
            color = BTN_ACTV if sym == self._symbol else BTN_NORM
            ax   = plt.axes([x, sym_y, sym_w, sym_h])
            btn  = Button(ax, sym, color=color, hovercolor=BTN_HOV)
            btn.label.set_color("white")
            btn.label.set_fontsize(9)
            btn.label.set_fontweight("bold")

            def _on_sym(event, s=sym):
                self._on_symbol_change(s)

            btn.on_clicked(_on_sym)
            self._sym_buttons[sym] = (btn, ax)

        # ── Expiration selectors ──────────────────────────────────────
        # Clicking the date box opens a native dropdown popup.
        # ◀ ▶ arrows still work for quick single-step changes.
        exp_base_y = 0.928
        exp_h      = 0.040

        # Front label
        self._ax_front_label = plt.axes([0.40, exp_base_y, 0.06, exp_h])
        self._ax_front_label.axis("off")
        self._ax_front_label.text(
            0.5, 0.5, "Front Exp:", color="white", ha="center", va="center",
            fontsize=9, fontweight="bold")

        # Front ◀
        self._btn_front_prev = Button(
            plt.axes([0.46, exp_base_y, 0.022, exp_h]), "◀",
            color=BTN_NORM, hovercolor=BTN_HOV)
        self._btn_front_prev.label.set_color("white")
        self._btn_front_prev.label.set_fontsize(9)
        self._btn_front_prev.on_clicked(lambda e: self._shift_front(-1))

        # Front date display (clickable — opens dropdown)
        self._ax_front_date = plt.axes([0.483, exp_base_y, 0.095, exp_h])
        self._ax_front_date.set_facecolor("#1e1e40")
        self._ax_front_date.tick_params(left=False, bottom=False,
                                        labelleft=False, labelbottom=False)
        for sp in self._ax_front_date.spines.values():
            sp.set_color(COL_BLUE)
            sp.set_linewidth(1.5)
        self._txt_front_date = self._ax_front_date.text(
            0.45, 0.55, self._front_exp, color=COL_BLUE,
            ha="center", va="center", fontsize=9, fontweight="bold")
        self._ax_front_date.text(
            0.92, 0.55, "▾", color=COL_BLUE, ha="right", va="center", fontsize=10)
        self.fig.canvas.mpl_connect("button_press_event",
            lambda e: self._on_date_click(e, "front") \
            if e.inaxes == self._ax_front_date else None)

        # Front DTE display
        self._ax_front_dte = plt.axes([0.579, exp_base_y, 0.028, exp_h])
        self._ax_front_dte.axis("off")
        self._txt_front_dte = self._ax_front_dte.text(
            0.5, 0.5, f"{_dte(self._front_exp)}d",
            color=COL_BLUE, ha="center", va="center", fontsize=8)

        # Front ▶
        self._btn_front_next = Button(
            plt.axes([0.608, exp_base_y, 0.022, exp_h]), "▶",
            color=BTN_NORM, hovercolor=BTN_HOV)
        self._btn_front_next.label.set_color("white")
        self._btn_front_next.label.set_fontsize(9)
        self._btn_front_next.on_clicked(lambda e: self._shift_front(+1))

        # Back label
        self._ax_back_label = plt.axes([0.637, exp_base_y, 0.055, exp_h])
        self._ax_back_label.axis("off")
        self._ax_back_label.text(
            0.5, 0.5, "Back Exp:", color="white", ha="center", va="center",
            fontsize=9, fontweight="bold")

        # Back ◀
        self._btn_back_prev = Button(
            plt.axes([0.693, exp_base_y, 0.022, exp_h]), "◀",
            color=BTN_NORM, hovercolor=BTN_HOV)
        self._btn_back_prev.label.set_color("white")
        self._btn_back_prev.label.set_fontsize(9)
        self._btn_back_prev.on_clicked(lambda e: self._shift_back(-1))

        # Back date display (clickable — opens dropdown)
        self._ax_back_date = plt.axes([0.716, exp_base_y, 0.095, exp_h])
        self._ax_back_date.set_facecolor("#1e2e1e")
        self._ax_back_date.tick_params(left=False, bottom=False,
                                       labelleft=False, labelbottom=False)
        for sp in self._ax_back_date.spines.values():
            sp.set_color(COL_GREEN)
            sp.set_linewidth(1.5)
        self._txt_back_date = self._ax_back_date.text(
            0.45, 0.55, self._back_exp, color=COL_GREEN,
            ha="center", va="center", fontsize=9, fontweight="bold")
        self._ax_back_date.text(
            0.92, 0.55, "▾", color=COL_GREEN, ha="right", va="center", fontsize=10)
        self.fig.canvas.mpl_connect("button_press_event",
            lambda e: self._on_date_click(e, "back") \
            if e.inaxes == self._ax_back_date else None)

        # Back DTE display
        self._ax_back_dte = plt.axes([0.812, exp_base_y, 0.028, exp_h])
        self._ax_back_dte.axis("off")
        self._txt_back_dte = self._ax_back_dte.text(
            0.5, 0.5, f"{_dte(self._back_exp)}d",
            color=COL_GREEN, ha="center", va="center", fontsize=8)

        # Back ▶
        self._btn_back_next = Button(
            plt.axes([0.841, exp_base_y, 0.022, exp_h]), "▶",
            color=BTN_NORM, hovercolor=BTN_HOV)
        self._btn_back_next.label.set_color("white")
        self._btn_back_next.label.set_fontsize(9)
        self._btn_back_next.on_clicked(lambda e: self._shift_back(+1))

        # ── Connection status indicator ───────────────────────────────
        # Pulsing circle + text on far right
        self._ax_status = plt.axes([0.866, exp_base_y, 0.13, exp_h])
        self._ax_status.set_facecolor(PANEL_BG)
        self._ax_status.axis("off")
        self._status_dot = self._ax_status.scatter(
            [0.10], [0.5], s=120, zorder=5,
            color=self._status_color(), edgecolors="none")
        self._status_txt = self._ax_status.text(
            0.22, 0.5, self._status_text(),
            color="white", va="center", fontsize=7.5)

    def _status_color(self) -> str:
        if self.provider.is_connected:
            # Pulse between bright and dim green
            return "#00ff66" if self._pulse_state % 2 == 0 else "#00aa44"
        return "#ff3333"

    def _status_text(self) -> str:
        lbl = self.provider.connection_label
        ts  = self.provider.last_update.strftime("%H:%M:%S")
        return f"{lbl}\nLast: {ts}"

    def _update_status_indicator(self):
        self._pulse_state += 1
        try:
            self._status_dot.set_color(self._status_color())
            self._status_txt.set_text(self._status_text())
        except Exception:
            pass

    def _update_expiration_labels(self):
        try:
            self._txt_front_date.set_text(self._front_exp)
            self._txt_front_dte.set_text(f"{_dte(self._front_exp)}d")
            self._txt_back_date.set_text(self._back_exp)
            self._txt_back_dte.set_text(f"{_dte(self._back_exp)}d")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Bottom Toolbar — View buttons + threshold
    # ------------------------------------------------------------------

    def _build_bottom_toolbar(self):
        btn_y = 0.015
        btn_h = 0.045

        views = [
            ("intraday", "Intraday",  0.03),
            ("5day",     "5-Day",     0.14),
            ("20day",    "20-Day",    0.23),
            ("scanner",  "Scanner",   0.32),
        ]
        self._view_btns = {}
        for key, label, x in views:
            color = BTN_ACTV if key == self._view else BTN_NORM
            ax  = plt.axes([x, btn_y, 0.085, btn_h])
            btn = Button(ax, label, color=color, hovercolor=BTN_HOV)
            btn.label.set_color("white")
            btn.label.set_fontsize(9)

            def _on_view(event, k=key):
                self._set_view(k)

            btn.on_clicked(_on_view)
            self._view_btns[key] = (btn, ax)

        # Refresh
        self._btn_refresh = Button(
            plt.axes([0.80, btn_y, 0.085, btn_h]), "⟳ Refresh",
            color="#1a3a1a", hovercolor="#2a5a2a")
        self._btn_refresh.label.set_color("white")
        self._btn_refresh.label.set_fontsize(9)
        self._btn_refresh.on_clicked(self._on_manual_refresh)

        # Threshold box
        self._threshold_box = TextBox(
            plt.axes([0.54, btn_y, 0.055, btn_h]),
            "Signal % ", initial=str(self.entry_threshold_pct),
            color=BTN_NORM, hovercolor="#3a3a6e")
        self._threshold_box.label.set_color("white")
        self._threshold_box.text_disp.set_color("white")
        self._threshold_box.on_submit(self._on_threshold_change)

    # ------------------------------------------------------------------
    # Interaction handlers
    # ------------------------------------------------------------------

    def _on_symbol_change(self, symbol: str):
        self._symbol = symbol
        self.provider.set_symbol(symbol)
        # Update symbol button colors and repaint immediately
        for sym, (btn, ax) in self._sym_buttons.items():
            c = BTN_ACTV if sym == symbol else BTN_NORM
            btn.color = c
            btn.ax.set_facecolor(c)
        self.fig.canvas.draw_idle()
        # Clear intraday data — new symbol
        with self._lock:
            self.times.clear()
            self.front_ivs.clear()
            self.back_ivs.clear()
            self.ratios.clear()
        self._refresh_expirations()
        self._load_historical()
        self._update_expiration_labels()
        self._fetch_and_append()
        self._draw()

    def _shift_front(self, delta: int):
        n = len(self._available_exps)
        new_idx = max(0, min(n - 1, self._front_exp_idx + delta))
        if new_idx == self._back_exp_idx:
            # Don't let front == back
            new_idx = max(0, min(n - 1, new_idx + delta))
        self._front_exp_idx = new_idx
        if self._front_exp_idx >= self._back_exp_idx:
            self._back_exp_idx = min(n - 1, self._front_exp_idx + 1)
        self._apply_expirations()
        self._clear_intraday()
        self._update_expiration_labels()
        self._fetch_and_append()
        self._draw()

    def _shift_back(self, delta: int):
        n = len(self._available_exps)
        new_idx = max(0, min(n - 1, self._back_exp_idx + delta))
        if new_idx == self._front_exp_idx:
            new_idx = max(0, min(n - 1, new_idx + delta))
        self._back_exp_idx = new_idx
        if self._back_exp_idx <= self._front_exp_idx:
            self._front_exp_idx = max(0, self._back_exp_idx - 1)
        self._apply_expirations()
        self._clear_intraday()
        self._update_expiration_labels()
        self._fetch_and_append()
        self._draw()

    def _clear_intraday(self):
        with self._lock:
            self.times.clear()
            self.front_ivs.clear()
            self.back_ivs.clear()
            self.ratios.clear()

    def _on_date_click(self, event, which: str):
        """Show an in-figure dropdown overlay for expiration selection."""
        exps = self._available_exps
        if not exps:
            return
        # Close any existing dropdown first
        self._close_dropdown()
        self._dropdown_which = which
        color = COL_BLUE if which == "front" else COL_GREEN
        current_idx = self._front_exp_idx if which == "front" else self._back_exp_idx

        # How many rows to show at once
        visible = min(len(exps), 12)
        row_h   = 0.040
        pad     = 0.004
        total_h = visible * row_h + pad * 2

        # Position below the clicked date box
        x0 = 0.483 if which == "front" else 0.716
        y0 = 0.928 - total_h - 0.005

        # Backing rectangle (border)
        self._dd_bg = self.fig.add_axes([x0 - 0.002, y0 - 0.002,
                                          0.130, total_h + 0.004])
        self._dd_bg.set_facecolor(color)
        self._dd_bg.axis("off")

        # Inner list area
        self._dd_ax = self.fig.add_axes([x0, y0, 0.126, total_h])
        self._dd_ax.set_facecolor("#0d0d1e")
        self._dd_ax.axis("off")
        self._dd_ax.set_xlim(0, 1)
        self._dd_ax.set_ylim(0, total_h)

        self._dd_exps   = exps
        self._dd_which  = which
        self._dd_scroll = max(0, current_idx - visible // 2)
        self._dd_hover  = current_idx
        self._dd_visible = visible
        self._dd_row_h  = row_h
        self._dd_color  = color
        self._dd_items  = []   # text artists

        self._render_dropdown()

        # Connect click and motion handlers
        self._dd_cid_click  = self.fig.canvas.mpl_connect(
            "button_press_event", self._dd_on_click)
        self._dd_cid_motion = self.fig.canvas.mpl_connect(
            "motion_notify_event", self._dd_on_motion)
        self._dd_cid_scroll = self.fig.canvas.mpl_connect(
            "scroll_event", self._dd_on_scroll)

        self.fig.canvas.draw_idle()

    def _render_dropdown(self):
        """Redraw the dropdown list items."""
        if not hasattr(self, "_dd_ax") or self._dd_ax is None:
            return
        ax      = self._dd_ax
        exps    = self._dd_exps
        scroll  = self._dd_scroll
        visible = self._dd_visible
        row_h   = self._dd_row_h
        hover   = self._dd_hover
        color   = self._dd_color
        total_h = visible * row_h

        # Clear old items
        for art in self._dd_items:
            try:
                art.remove()
            except Exception:
                pass
        self._dd_items = []

        for i in range(visible):
            idx = scroll + i
            if idx >= len(exps):
                break
            exp  = exps[idx]
            d    = _dte(exp)
            y    = total_h - (i + 0.5) * row_h
            bg   = "#5555aa" if idx == hover else ("#1a1a3e" if i % 2 == 0 else "#0d0d1e")
            # Highlight bar
            rect = mpatches.FancyBboxPatch(
                (0.01, y - row_h * 0.45), 0.98, row_h * 0.88,
                boxstyle="round,pad=0.002", linewidth=0,
                facecolor=bg, transform=ax.transData)
            ax.add_patch(rect)
            self._dd_items.append(rect)
            # Text
            fc   = color if idx == hover else "white"
            txt  = ax.text(0.08, y, f"{exp}  ({d}d)",
                           color=fc, va="center", fontsize=9,
                           fontfamily="monospace", fontweight="bold" if idx == hover else "normal")
            self._dd_items.append(txt)

        # Scroll indicators
        if scroll > 0:
            t = ax.text(0.95, total_h - 0.008, "▲", color="#aaaaaa",
                        va="top", ha="right", fontsize=8)
            self._dd_items.append(t)
        if scroll + visible < len(exps):
            t = ax.text(0.95, 0.008, "▼", color="#aaaaaa",
                        va="bottom", ha="right", fontsize=8)
            self._dd_items.append(t)

        self.fig.canvas.draw_idle()

    def _dd_row_at(self, event) -> Optional[int]:
        """Return the expiration index under the mouse, or None."""
        if not hasattr(self, "_dd_ax") or event.inaxes != self._dd_ax:
            return None
        visible = self._dd_visible
        row_h   = self._dd_row_h
        total_h = visible * row_h
        # y in data coords
        y       = event.ydata
        if y is None:
            return None
        i = int((total_h - y) / row_h)
        idx = self._dd_scroll + i
        if 0 <= idx < len(self._dd_exps):
            return idx
        return None

    def _dd_on_motion(self, event):
        idx = self._dd_row_at(event)
        if idx is not None and idx != self._dd_hover:
            self._dd_hover = idx
            self._render_dropdown()

    def _dd_on_scroll(self, event):
        if not hasattr(self, "_dd_ax") or event.inaxes != self._dd_ax:
            return
        delta = -1 if event.button == "up" else 1
        max_scroll = max(0, len(self._dd_exps) - self._dd_visible)
        self._dd_scroll = max(0, min(max_scroll, self._dd_scroll + delta))
        self._render_dropdown()

    def _dd_on_click(self, event):
        idx = self._dd_row_at(event)
        if idx is not None:
            # Selection made
            n = len(self._dd_exps)
            if self._dd_which == "front":
                self._front_exp_idx = idx
                if self._front_exp_idx >= self._back_exp_idx:
                    self._back_exp_idx = min(n - 1, idx + 1)
            else:
                self._back_exp_idx = idx
                if self._back_exp_idx <= self._front_exp_idx:
                    self._front_exp_idx = max(0, idx - 1)
            self._apply_expirations()
            self._clear_intraday()
            self._update_expiration_labels()
            self._fetch_and_append()
        # Always close on any click (inside or outside)
        self._close_dropdown()
        if idx is not None:
            self._draw()

    def _close_dropdown(self):
        """Remove the dropdown overlay and disconnect its event handlers."""
        for attr in ("_dd_ax", "_dd_bg"):
            ax = getattr(self, attr, None)
            if ax is not None:
                try:
                    ax.remove()
                except Exception:
                    pass
                setattr(self, attr, None)
        for cid_attr in ("_dd_cid_click", "_dd_cid_motion", "_dd_cid_scroll"):
            cid = getattr(self, cid_attr, None)
            if cid is not None:
                try:
                    self.fig.canvas.mpl_disconnect(cid)
                except Exception:
                    pass
                setattr(self, cid_attr, None)
        self._dd_items = []
        self.fig.canvas.draw_idle()

    def _set_view(self, view: str):
        self._view = view
        for key, (btn, ax) in self._view_btns.items():
            c = BTN_ACTV if key == view else BTN_NORM
            btn.color = c
            btn.ax.set_facecolor(c)
        # Draw immediately so the user sees the loading state right away
        self._draw()
        # Then kick off background fetch only if data is missing
        if view == "scanner" and (self._scanner_df is None or self._scanner_df.empty):
            threading.Thread(target=self._bg_fetch_scanner, daemon=True).start()
        elif view == "5day" and (self._hist5 is None or self._hist5.empty):
            threading.Thread(target=self._bg_fetch_hist, daemon=True).start()
        elif view == "20day" and (self._hist20 is None or self._hist20.empty):
            threading.Thread(target=self._bg_fetch_hist, daemon=True).start()

    def _bg_fetch_scanner(self):
        sc = self.provider.scanner_data()
        with self._lock:
            self._scanner_df = sc
        if self._view == "scanner":
            self._draw()

    def _bg_fetch_hist(self):
        h5  = self.provider.get_historical(5)
        h20 = self.provider.get_historical(20)
        with self._lock:
            self._hist5  = h5
            self._hist20 = h20
        if self._view in ("5day", "20day"):
            self._draw()

    def _on_manual_refresh(self, event):
        # Force-clear cached data so everything re-fetches
        with self._lock:
            self._hist5      = None
            self._hist20     = None
            self._scanner_df = None
        self._fetch_and_append()
        self._draw()
        # Fetch in background then redraw
        threading.Thread(target=self._bg_fetch_scanner, daemon=True).start()
        threading.Thread(target=self._bg_fetch_hist,    daemon=True).start()

    def _on_threshold_change(self, text: str):
        try:
            self.entry_threshold_pct = max(0.1, min(float(text), 10.0))
        except ValueError:
            pass
        self._draw()

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _sync_button_states(self):
        """Re-apply active/inactive colors to all toggle buttons.
        Must update btn.color (not just ax.set_facecolor) because matplotlib's
        Button._motion() resets facecolor back to btn.color on every mouse move."""
        for sym, (btn, ax) in self._sym_buttons.items():
            c = BTN_ACTV if sym == self._symbol else BTN_NORM
            btn.color = c
            btn.ax.set_facecolor(c)
        for key, (btn, ax) in self._view_btns.items():
            c = BTN_ACTV if key == self._view else BTN_NORM
            btn.color = c
            btn.ax.set_facecolor(c)

    def _draw(self):
        self._update_status_indicator()
        self._sync_button_states()
        if self._view == "intraday":
            self._draw_intraday()
        elif self._view == "5day":
            self._draw_historical(self._hist5, "5-Day")
        elif self._view == "20day":
            self._draw_historical(self._hist20, "20-Day")
        elif self._view == "scanner":
            self._draw_scanner()
        self.fig.canvas.draw_idle()

    def _clear_axes(self):
        self.ax_iv.cla()
        self.ax_ratio.cla()
        self._style_chart_axes()

    def _ensure_chart_axes(self):
        self.ax_iv.set_visible(True)
        self.ax_ratio.set_visible(True)
        if hasattr(self, "_ax_scanner_table"):
            try:
                self._ax_scanner_table.remove()
                del self._ax_scanner_table
            except Exception:
                pass

    # ── Intraday ──────────────────────────────────────────────────────

    def _draw_intraday(self):
        self._ensure_chart_axes()
        self._clear_axes()

        with self._lock:
            times     = list(self.times)
            front_ivs = list(self.front_ivs)
            back_ivs  = list(self.back_ivs)
            ratios    = list(self.ratios)

        fe   = self._front_exp
        be   = self._back_exp
        fdte = _dte(fe)
        bdte = _dte(be)
        sym  = self._symbol

        if not times:
            self.ax_iv.text(0.5, 0.5, "Waiting for data…", color="white",
                            ha="center", va="center", transform=self.ax_iv.transAxes,
                            fontsize=13)
            return

        t = [mdates.date2num(ts) for ts in times]

        # ── Top: IV lines ──
        self.ax_iv.plot(t, [v * 100 for v in front_ivs],
                        "-", color=COL_BLUE, linewidth=1.8,
                        label=f"Front IV  {fe}  ({fdte}d)")
        self.ax_iv.plot(t, [v * 100 for v in back_ivs],
                        "-", color=COL_GREEN, linewidth=1.8,
                        label=f"Back IV   {be}  ({bdte}d)")
        self.ax_iv.set_ylabel("IV (%)", color=COL_TICK)
        self.ax_iv.legend(loc="upper left", facecolor=BG_DARK,
                          labelcolor="white", fontsize=8, framealpha=0.7)
        self.ax_iv.yaxis.set_major_formatter(
            matplotlib.ticker.FormatStrFormatter("%.1f%%"))

        cur = ratios[-1] if ratios else 1.0
        falling = len(ratios) >= 2 and ratios[-1] < ratios[-2]
        tcol    = "#44ff44" if falling else "#ff5555"
        arrow   = "↓ FALLING — Watch for Entry!" if falling else "↑ RISING — Wait"
        self.ax_iv.set_title(
            f"FLUX  ·  {sym}  ·  Ratio: {cur:.4f}  ·  {arrow}",
            color=tcol, fontsize=11, fontweight="bold", pad=5)

        # ── Bottom: Ratio ──
        self.ax_ratio.plot(t, ratios, "-", color=COL_ORNG,
                           linewidth=2.2, label="F/B Ratio")

        if len(ratios) > 1:
            ra   = np.array(ratios)
            rmn  = ra.mean()
            rstd = ra.std()
            self.ax_ratio.axhline(rmn, color="#777777", linestyle="--",
                                  linewidth=0.8, alpha=0.7,
                                  label=f"Mean  {rmn:.4f}")
            self.ax_ratio.axhline(rmn + rstd, color="#ff4444",
                                  linestyle=":", linewidth=0.8, alpha=0.7,
                                  label=f"+1σ   {rmn + rstd:.4f}")
            hi      = ra.max()
            drop_pct = (hi - ra[-1]) / hi * 100 if hi > 0 else 0
            if drop_pct >= self.entry_threshold_pct:
                self.ax_ratio.axhline(ra[-1], color="#ffff00",
                                      linestyle="-.", linewidth=1.5, alpha=0.95,
                                      label=f"⚡ ENTRY  ({drop_pct:.1f}% drop)")

        self.ax_ratio.set_ylabel("F/B Ratio", color=COL_TICK)
        self.ax_ratio.legend(loc="upper left", facecolor=BG_DARK,
                             labelcolor="white", fontsize=7, framealpha=0.7)
        self.ax_ratio.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax_ratio.set_xlabel("Time (ET)", color=COL_TICK)

        # Market open/close reference
        if times:
            day      = times[0].date()
            open_dt  = datetime.datetime.combine(day, MARKET_OPEN)
            close_dt = datetime.datetime.combine(day, MARKET_CLOSE)
            for ax in [self.ax_iv, self.ax_ratio]:
                ax.axvline(mdates.date2num(open_dt),  color="#6666aa",
                           linestyle=":", linewidth=0.8, alpha=0.5)
                ax.axvline(mdates.date2num(close_dt), color="#6666aa",
                           linestyle=":", linewidth=0.8, alpha=0.5)

    # ── Historical ────────────────────────────────────────────────────

    def _draw_historical(self, df: pd.DataFrame, label: str):
        self._ensure_chart_axes()
        self._clear_axes()

        if df is None or df.empty:
            self.ax_iv.text(0.5, 0.5, f"No {label} data available",
                            color="white", ha="center", va="center",
                            transform=self.ax_iv.transAxes, fontsize=13)
            return

        t = [mdates.date2num(ts) for ts in df.index]
        self.ax_iv.plot(t, df["front_iv"] * 100, "-", color=COL_BLUE,
                        linewidth=1.2, label=f"Front IV  {self._front_exp}")
        self.ax_iv.plot(t, df["back_iv"] * 100, "-", color=COL_GREEN,
                        linewidth=1.2, label=f"Back IV   {self._back_exp}")
        self.ax_iv.set_ylabel("IV (%)", color=COL_TICK)
        self.ax_iv.legend(loc="upper left", facecolor=BG_DARK,
                          labelcolor="white", fontsize=8, framealpha=0.7)
        self.ax_iv.set_title(
            f"FLUX  ·  {self._symbol}  ·  {label} View",
            color="white", fontsize=11, fontweight="bold")
        self.ax_iv.yaxis.set_major_formatter(
            matplotlib.ticker.FormatStrFormatter("%.1f%%"))

        self.ax_ratio.plot(t, df["ratio"], "-", color=COL_ORNG,
                           linewidth=1.5, label="F/B Ratio")
        rmn  = df["ratio"].mean()
        rstd = df["ratio"].std()
        self.ax_ratio.axhline(rmn, color="#777777", linestyle="--",
                              linewidth=0.8, alpha=0.7, label=f"Mean  {rmn:.4f}")
        self.ax_ratio.axhline(rmn + rstd, color="#ff4444",
                              linestyle=":", linewidth=0.8, alpha=0.7,
                              label=f"+1σ   {rmn + rstd:.4f}")
        self.ax_ratio.set_ylabel("F/B Ratio", color=COL_TICK)
        self.ax_ratio.legend(loc="upper left", facecolor=BG_DARK,
                             labelcolor="white", fontsize=7, framealpha=0.7)
        self.ax_ratio.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
        self.ax_ratio.set_xlabel("Date/Time (ET)", color=COL_TICK)

    # ── Scanner ───────────────────────────────────────────────────────

    def _draw_scanner(self):
        self.ax_iv.set_visible(False)
        self.ax_ratio.set_visible(False)

        if hasattr(self, "_ax_scanner_table"):
            try:
                self._ax_scanner_table.remove()
            except Exception:
                pass

        self._ax_scanner_table = self.fig.add_axes(
            [0.04, 0.10, 0.92, 0.82], facecolor=BG_CHART)
        self._ax_scanner_table.axis("off")

        df = self._scanner_df
        if df is None or df.empty:
            self._ax_scanner_table.text(
                0.5, 0.5,
                f"Scanning {self._symbol} expiration pairs…\n"
                "(click ⟳ Refresh to load)",
                color="white", ha="center", va="center", fontsize=12)
            return

        # Locate Ratio column index dynamically
        cols = list(df.columns)
        ratio_col_idx = cols.index("Ratio") if "Ratio" in cols else 7
        ts = datetime.datetime.now().strftime("%H:%M:%S")

        self._ax_scanner_table.set_title(
            f"FLUX Scanner  ·  {self._symbol}  ·  Top IV Ratio Pairs  ·  updated {ts}",
            color="white", fontsize=11, fontweight="bold", pad=6)

        tbl = self._ax_scanner_table.table(
            cellText=df.values.tolist(),
            colLabels=cols,
            loc="upper center", cellLoc="center")
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1, 1.55)

        # Header row styling
        for j in range(len(cols)):
            tbl[(0, j)].set_facecolor("#2a2a6a")
            tbl[(0, j)].set_text_props(color="white", fontweight="bold")

        # Data rows — color by ratio tier
        for i, row in enumerate(df.values.tolist()):
            try:
                ratio_val = float(row[ratio_col_idx])
            except (ValueError, IndexError):
                ratio_val = 1.0
            if ratio_val >= 1.20:
                bg = "#0d3d0d"   # bright green  — best setups
            elif ratio_val >= 1.08:
                bg = "#2a3a1a"   # muted green   — good setups
            else:
                bg = "#1e1e30"   # neutral blue  — marginal
            for j in range(len(cols)):
                tbl[(i + 1, j)].set_facecolor(bg)
                tbl[(i + 1, j)].set_text_props(color="white")
            # Highlight the ratio cell itself in gold
            tbl[(i + 1, ratio_col_idx)].set_text_props(
                color="#ffd700", fontweight="bold")

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self):
        self._draw()
        # Pulse the connection dot every ~2 seconds
        self._timer = self.fig.canvas.new_timer(interval=REFRESH_SEC * 1000)
        self._timer.add_callback(self._on_timer_tick)
        self._pulse_timer = self.fig.canvas.new_timer(interval=2000)
        self._pulse_timer.add_callback(self._on_pulse_tick)
        self._timer.start()
        self._pulse_timer.start()
        plt.show()
        self._running = False

    def _on_timer_tick(self):
        self._fetch_and_append()
        self._draw()

    def _on_pulse_tick(self):
        """Just pulse the status dot without redrawing everything."""
        self._pulse_state += 1
        try:
            self._status_dot.set_color(self._status_color())
            self.fig.canvas.draw_idle()
        except Exception:
            pass


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Flux Tool v2 — DC Time Machine")
    parser.add_argument("--demo",      action="store_true", default=True)
    parser.add_argument("--ibkr",      action="store_true")
    parser.add_argument("--host",      default="127.0.0.1")
    parser.add_argument("--port",      type=int, default=7497)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    print("=" * 60)
    print("  FLUX v2 — DC Time Machine IV Ratio Tool")
    print("  Features: Symbol selector · Expiration selectors · Live status")
    print("=" * 60)

    if args.ibkr:
        if not IBKR_AVAILABLE:
            print("ERROR: ib_insync not installed.")
            sys.exit(1)
        print(f"Connecting to IBKR TWS at {args.host}:{args.port}…")
        provider = IBKRIVProvider(host=args.host, port=args.port)
        print("Connected!" if provider.is_connected else "Connection failed — check TWS.")
    else:
        print("DEMO MODE — simulated IV data.")
        print("Connect to live data: python flux_tool.py --ibkr")
        provider = MockIVProvider()

    app = FluxApp(provider, entry_threshold_pct=args.threshold)
    app.run()


if __name__ == "__main__":
    main()
