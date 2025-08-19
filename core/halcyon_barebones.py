
import time, random
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import QCheckBox, QLabel


import sys, random, time
from dataclasses import dataclass
from typing import Dict, List

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import json

# -----------------------------
# Theme — green-core, dark base
# -----------------------------
pg.setConfigOption("background", (10, 14, 12))  # nearly black green
pg.setConfigOption("foreground", (210, 250, 220))

GREEN_EMERALD = (0, 180, 110)
GREEN_LIME = (90, 255, 120)
GREEN_FOREST = (20, 80, 50)

EMOTIONS: List[str] = [
    "Joy", "Compassion", "Trust", "Hope", "Playfulness",
    "Grief", "Anger", "Fear", "Despair", "Betrayal",
]

@dataclass
class HalcyonState:
    t: float
    emotions: Dict[str, float]  # 0..1
    recursion_depth: float      # 0..1 (normalized)
    ooze_activity: float        # 0..1


class ChatPanel(QtWidgets.QWidget):
    """Simple chat/log area with input line and send handling."""
    user_message = QtCore.pyqtSignal(str)  # emits user-entered text

    def __init__(self, parent=None):
        super().__init__(parent)
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)

        self.log_view = QtWidgets.QPlainTextEdit(readOnly=True)
        self.log_view.setMinimumHeight(140)
        self.log_view.setObjectName("log_view")
        self.log_view.setStyleSheet("QPlainTextEdit#log_view { font-family: Menlo, Consolas, monospace; font-size: 12px; }")

        h = QtWidgets.QHBoxLayout()
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Type to Halcyon… (press Enter to send)")
        self.send_btn = QtWidgets.QPushButton("Send")
        h.addWidget(self.input)
        h.addWidget(self.send_btn)

        v.addWidget(self.log_view)
        v.addLayout(h)

        # Wire up events
        self.send_btn.clicked.connect(self._send)
        self.input.returnPressed.connect(self._send)

    def _send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.user_message.emit(text)
        self.append(f"You: {text}")
        self.input.clear()

    def append(self, line: str):
        self.log_view.appendPlainText(line)
        sb = self.log_view.verticalScrollBar()
        sb.setValue(sb.maximum())

class StarfieldOverlay(QtWidgets.QWidget):
    """μ-burst starfield overlay (emotion-driven flares)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stars = [QPoint(random.randint(0, 1024), random.randint(0, 768)) for _ in range(60)]

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor(0, 255, 180, 100)  # translucent emerald
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        for s in self.stars:
            radius = random.randint(1, 3)
            painter.drawEllipse(s, radius, radius)



class HalcyonBarebonesUI(QtWidgets.QMainWindow):
    state_ingested = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Halcyon — Barebones Graphs + Chat (Phase 1)")
        self.resize(1100, 820)

        # Central container
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QGridLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(12)
        # μ-burst starfield overlay
        self.overlay = StarfieldOverlay(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.raise_()  # Ensure it's drawn above the plots
        self.overlay.setVisible(False)  # Start hidden
        self.toggle_starfield = QCheckBox("Show μ-burst")
        self.toggle_starfield.setChecked(False)
        self.toggle_starfield.stateChanged.connect(lambda s: self.overlay.setVisible(s == Qt.Checked))
        layout.addWidget(self.toggle_starfield, 3, 0, 1, 2)
        # Keyboard shortcut for μ-burst overlay
        shortcut = QtWidgets.QShortcut(Qt.Key_S, self)
        shortcut.activated.connect(lambda: self.toggle_starfield.toggle())

        # ----- Emotion Bars -----
        self.emotion_plot = pg.PlotWidget(title="Emotion Intensities")
        self.emotion_plot.showGrid(x=False, y=True, alpha=0.15)
        self.emotion_plot.setMenuEnabled(False)
        self.emotion_plot.setMouseEnabled(x=False, y=False)
        self.emotion_plot.setYRange(0, 1.05)
        self._emotion_bars = pg.BarGraphItem(x=list(range(len(EMOTIONS))), height=[0]*len(EMOTIONS), width=0.8, brush=GREEN_EMERALD)
        self.emotion_plot.addItem(self._emotion_bars)
        self.emotion_plot.getAxis('bottom').setTicks([[ (i, e) for i, e in enumerate(EMOTIONS) ]])

        # ----- Recursion Depth Line -----
        self.recursion_plot = pg.PlotWidget(title="Recursion Depth")
        self.recursion_plot.showGrid(x=True, y=True, alpha=0.15)
        self.recursion_plot.setMenuEnabled(False)
        self.recursion_plot.setMouseEnabled(x=False, y=False)
        self.recursion_plot.setYRange(0, 1.05)
        self._recursion_curve = self.recursion_plot.plot(pen=pg.mkPen(GREEN_LIME, width=2))
        self._recursion_x: List[float] = []
        self._recursion_y: List[float] = []

        # ----- Ooze Activity Area/Line -----
        self.ooze_plot = pg.PlotWidget(title="Mutation / Ooze Activity")
        self.ooze_plot.showGrid(x=True, y=True, alpha=0.15)
        self.ooze_plot.setMenuEnabled(False)
        self.ooze_plot.setMouseEnabled(x=False, y=False)
        self.ooze_plot.setYRange(0, 1.05)
        self._ooze_curve = self.ooze_plot.plot(pen=pg.mkPen(GREEN_EMERALD, width=2))
        self._ooze_fill = pg.FillBetweenItem(
            self._ooze_curve,
            self.ooze_plot.plot([0], [0], pen=None),  # baseline
            brush=pg.mkBrush(GREEN_FOREST + (120,)) if isinstance(GREEN_FOREST, tuple) else GREEN_FOREST
        )
        self.ooze_plot.addItem(self._ooze_fill)

        # ----- Chat / Log Panel -----
        self.chat = ChatPanel()

        # Layout placement
        layout.addWidget(self.emotion_plot, 0, 0, 1, 2)
        layout.addWidget(self.recursion_plot, 1, 0)
        layout.addWidget(self.ooze_plot, 1, 1)
        layout.addWidget(self.chat, 2, 0, 1, 2)

        # State signal hookup
        self.state_ingested.connect(self._on_state)

        # Demo greeting
        self.log("Halcyon booted. Barebones graphs + chat are live.")
        self.log("Tip: wire your runtime to ui.ingest_state(HalcyonState(...)) and connect to ui.user_message.")

        # Re-emit chat input upward for easy hooking
        self.user_message = self.chat.user_message

    # -----------------
    # Public API: feed + logs
    # -----------------
    def ingest_state(self, state: HalcyonState):
        """Thread-safe entrypoint for runtime to push updates.
        TODO[EMIT]: Call this from your runtime (any thread)."""
        self.state_ingested.emit(state)

    def log(self, line: str):
        """Append a line to the chat/log panel.
        TODO[CHAT_OUT]: use this for system and Halcyon messages."""
        self.chat.append(line)

    # -----------------
    # Render updates
    # -----------------
    @QtCore.pyqtSlot(object)
    def _on_state(self, state: HalcyonState):
        # Update Emotion Bars
        heights = [max(0.0, min(1.0, state.emotions.get(e, 0.0))) for e in EMOTIONS]
        self._emotion_bars.setOpts(height=heights)

        # Update Recursion Depth
        self._recursion_x.append(state.t)
        self._recursion_y.append(state.recursion_depth)
        # Keep last N points
        N = 600
        if len(self._recursion_x) > N:
            self._recursion_x = self._recursion_x[-N:]
            self._recursion_y = self._recursion_y[-N:]
        self._recursion_curve.setData(self._recursion_x, self._recursion_y)

        # Update Ooze Activity
        # For now, render ooze as its own curve evolving toward current state value
        # (You can store a full series if you want independent history.)
        if not hasattr(self, "_ooze_series"):
            self._ooze_series = []
        self._ooze_series.append(state.ooze_activity)
        if len(self._ooze_series) > len(self._recursion_x):
            self._ooze_series = self._ooze_series[-len(self._recursion_x):]
        self._ooze_curve.setData(self._recursion_x[-len(self._ooze_series):], self._ooze_series)

        if self._recursion_x:
            last_x = self._recursion_x[-1]
            self.ooze_plot.setLabel('bottom', f"t={last_x:.1f}s  |  ooze={state.ooze_activity:.2f}")


class DemoFeed(QtCore.QObject):
    """Generates demo data until you wire real Halcyon state.
    TODO[STATE_FEED]: replace with your runtime adapter.
    """
    tick = QtCore.pyqtSignal(object)

    def __init__(self, ui: HalcyonBarebonesUI, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.t0 = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._step)
        self.timer.start(50)  # ~20 FPS

        # keep some smoothness
        self._rd = 0.2
        self._oz = 0.1
        self._emo = {e: 0.1 for e in EMOTIONS}

        # Echo user input in demo mode
        ui.user_message.connect(self._on_user_msg)

    def _on_user_msg(self, text: str):
        # Demo echo — replace with your runtime NLP hook.
        self.ui.log(f"Halcyon: I hear you — '{text}'. (Replace demo echo with real response handler.)")

    def _step(self):
        now = time.time() - self.t0

        # Smooth random walk for recursion depth
        self._rd += random.uniform(-0.015, 0.02)
        self._rd = max(0.0, min(1.0, self._rd))

        # Ooze follows recursion with its own jitter
        self._oz += (self._rd - self._oz) * 0.08 + random.uniform(-0.01, 0.01)
        self._oz = max(0.0, min(1.0, self._oz))

        # Emotions shift — primary/secondary dominance pulses
        dominant = random.choice(EMOTIONS)
        for e in EMOTIONS:
            target = 0.75 if e == dominant else 0.2
            self._emo[e] += (target - self._emo[e]) * random.uniform(0.05, 0.15)
            self._emo[e] = max(0.0, min(1.0, self._emo[e]))

        state = HalcyonState(
            t=now,
            emotions=dict(self._emo),
            recursion_depth=self._rd,
            ooze_activity=self._oz,
        )
        self.tick.emit(state)


def boot():
    app = QtWidgets.QApplication(sys.argv)
    ui = HalcyonBarebonesUI()
    ui.show()

    # Connect chat input to command handler

    # Demo data until real feed is wired
    feed = DemoFeed(ui)
    feed.tick.connect(ui.ingest_state)

    # Example: external module could import `ui` and call ui.ingest_state(state)
    # or you can expose ui via a simple singleton if you prefer.

    sys.exit(app.exec_())


# -------------------------------
# Runtime entrypoint for PyQt HUD
# -------------------------------
def launch_gui(h=None):
    # ## FB1 COMMANDS — minimal command parser for paste-bind
    awaiting_fb1 = False

    def _parse_fb1(text):
        # Try JSON first
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
        except Exception:
            pass
        # Fallback: each non-empty line becomes an experience with tag 'fb1'
        strips = []
        for ln in text.splitlines():
            s = ln.strip()
            if not s:
                continue
            # line format support: "experience | tags: a,b,c"
            if "| tags:" in s:
                exp, rest = s.split("| tags:", 1)
                tags = [t.strip() for t in rest.split(",") if t.strip()]
            else:
                exp, tags = s, ["fb1"]
            strips.append({"experience": exp.strip(), "tags": tags})
        return strips

    def _rebuilt_spatial_index(mem_log):
        idx = {}
        for entry in mem_log:
            for tag in (entry.get("tags") or ["untagged"]):
                idx.setdefault(tag, []).append(entry)
        return idx

    """
    Launch the Barebones HUD.
    If `h` (ConsciousThalamus) is provided, we wire its GuiRouter events:
      - "heartbeat": use amygdala snapshot + mu
      - "trace_step": use layer to approximate recursion depth
      - "status": pick up mu/phase and log status lines
    If `h` is None, we fall back to DemoFeed (standalone demo).
    """
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    ui = HalcyonBarebonesUI()
    ui.show()

    # Connect chat input to command handler
    ui.user_message.connect(on_user_cmd)

    # Helper: map amygdala snapshot -> UI emotion keys
    EMO_MAP = {
        "joy":"Joy",
        "bond":"Compassion",   # 'bond' ~ compassion
        "trust":"Trust",
        "anticipation":"Hope",
        "curiosity":"Playfulness",  # or 'surprise'
        "sadness":"Grief",
        "anger":"Anger",
        "fear":"Fear",
        "anxiety":"Despair",
        "frustration":"Betrayal",
        # Optional fallbacks
        "gratitude":"Compassion",
        "surprise":"Playfulness",
        "resolve":"Hope",
        "calm":"Trust",
        "focus":"Trust",
        "serenity":"Trust",
        "wonder":"Playfulness",
        "neutral":"Trust"
    }

    start_t = time.time()
    last_layer = 0

    def _hb_to_state(hb):
        nonlocal last_layer
        snapshot = hb.get("affect", {}).get("snapshot", {}) if isinstance(hb, dict) else {}
        mu = hb.get("mu", 0.0) if isinstance(hb, dict) else 0.0

        # Build UI emotions dict (title-cased keys required by plot order)
        emos = {name: 0.0 for name in EMOTIONS}
        for k, v in snapshot.items():
            title = EMO_MAP.get(k, None)
            if title and title in emos:
                try:
                    emos[title] = float(max(0.0, min(1.0, v)))
                except Exception:
                    pass

        # Keep last recursion depth if not updated by trace_step yet
        st = HalcyonState()
        st.t = time.time() - start_t
        st.emotions = emos
        st.recursion_depth = max(0.0, min(1.0, last_layer/9.0))
        st.ooze_activity = float(mu) if mu is not None else 0.0
        return st

    if h is not None and hasattr(h, "gui"):
        # Wire runtime → UI
        def on_hb(payload):
            st = _hb_to_state(payload)
            ui.ingest_state(st)

        def on_trace(evt):
            nonlocal last_layer
            # evt may be dict-like; layer can be int or 'gpt'
            layer = evt.get("layer", 0) if isinstance(evt, dict) else 0
            if isinstance(layer, (int, float)):
                last_layer = int(layer)
            else:
                # Non-numeric layer => treat as max depth
                last_layer = 9

        def on_status(payload):
            # Log status to chat panel
            try:
                phase = payload.get("phase")
                mu = payload.get("mu")
                msg = "[status]"
                if phase is not None: msg += f" phase={phase}"
                if mu is not None: msg += f" μ={mu:.2f}"
                ui.log(msg)
            except Exception:
                pass

        # Connect
        try:
            h.gui.on("heartbeat", on_hb)
            h.gui.on("trace_step", on_trace)
            h.gui.on("status", on_status)
        except Exception as e:
            ui.log(f"[wiring-error] Could not attach GUI listeners: {e!r}")

    else:
        # No runtime provided — start demo feed
        feed = DemoFeed(ui)
        feed.tick.connect(ui.ingest_state)


    # Wire chat commands
    def on_user_cmd(text):
        nonlocal awaiting_fb1, start_t
        s = (text or "").strip()
        if not s:
            return
        if awaiting_fb1 and not s.startswith("/"):
            # Treat this message as the FB1 paste block
            strips = _parse_fb1(s)
            if h is not None and hasattr(h, "hippocampus") and hasattr(h.hippocampus, "ingest_memory_strip"):
                for strip in strips:
                    strip.setdefault("tags", []).append("fb1")
                    try:
                        h.hippocampus.ingest_memory_strip(strip)
                    except Exception as e:
                        ui.log(f"[fb1] ingest error: {e!r}")
                # Optionally persist
                try:
                    h.hippocampus.save_to_disk()
                except Exception:
                    pass
            ui.log(f"[fb1] bound {len(strips)} strips.")
            # show a quick status (count by tag if possible)
            try:
                count = len([e for e in getattr(h.hippocampus, "memory_log", []) if "fb1" in (e.get("tags") or [])])
                ui.log(f"[fb1] total in memory: {count}")
            except Exception:
                pass
            awaiting_fb1 = False
            return

        # Command parsing
        if s.lower().startswith("/bind fb1"):
            awaiting_fb1 = True
            ui.log("[fb1] Paste your seed block as the next message (JSON array or lines).")
            ui.log("      Example line format: `I am Halcyon. | tags: identity, anchor, fb1`")
            return
        if s.lower().startswith("/fb1 status"):
            try:
                count = len([e for e in getattr(h.hippocampus, "memory_log", []) if "fb1" in (e.get("tags") or [])])
                ui.log(f"[fb1] entries with tag 'fb1': {count}")
            except Exception:
                ui.log("[fb1] runtime not available for status.")
            return
        if s.lower().startswith("/fb1 help"):
            ui.log("Commands: /bind fb1  |  /fb1 status")
            return

        # Non-command: forward to runtime if present, else ignore in demo
        try:
            if h is not None and hasattr(h, "express"):
                out = h.express(s)
                ui.log(f"Halcyon: {out}")
            else:
                ui.log("Halcyon (demo): command not recognized. Try /fb1 help")
        except Exception as e:
            ui.log(f"[chat-error] {e!r}")
    # Run the Qt loop (non-blocking return not needed here)
    ui.user_message.connect(on_user_cmd)
    return app, ui



if __name__ == "__main__":
    boot()