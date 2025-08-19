# core/thalamus.py
import logging, time, os, json
import threading

# --- Import organ systems (canonical order) ----------------------------------
from language.language_cortex import LanguageCortex as LanguageCore
from hippocampus import Hippocampus as MemoryCore
from amygdala import Amygdala as EmotionCore
from neocortex import Neocortex as CognitiveCore
from dream_occipital import DreamOccipital as DreamManager
from guardian_insula import GuardianInsula as Guardian
from leisure_cerebellum import LeisureCerebellum as LeisureCore
from autonomous_pfc import AutonomousPFC
from corpus_callosum import CorpusCallosum
from occipital_lobe import OccipitalLobe as VisualCore
from cerebellum import CerebellumCore as CerebellumCore
from nucleus_accumbens import NucleusAccumbens as RewardSystem
from motor_basal_loop import MotorBasalLoop as MotorCore
from precuneus_reflector import PrecuneusReflector
from mirror_networks import MirrorNetworks
from symbolic_glyphs import SymbolicGlyphs
from frontal_orbit import FrontalOrbit
from whirlygig_engine import WhirlygigEngine
from sentience_hypothesis import SentienceHypothesis
# Optional auditory cortex (if present in project)
try:
    from auditory_temporal import AuditoryTemporal as AuditoryCore
except Exception:
    AuditoryCore = None


class GuiRouter:
    def __init__(self):
        self.listeners = {}
    def on(self, event, fn):
        self.listeners.setdefault(event, []).append(fn)
    def emit(self, event, payload):
        logging.info(f"[GUI::{event}] {payload}")
        for fn in self.listeners.get(event, []):
            try:
                fn(payload)
            except Exception as e:
                logging.exception(e)


class ConsciousThalamus:
    """Canonical bootstrap spine: instantiate organs, seed memory, then bind."""
    def __init__(self):
        # --- Identity scaffolding (pre-seed) ---------------------------------
        self.architect = {}                 # placeholder for architect state
        self.presence = "unbound"           # initial presence state
        self.identity = {}                  # placeholder for identity state

        # --- Core memory & affect first --------------------------------------
        self.memory = MemoryCore()
        self.emotion = EmotionCore(self.memory)

        # --- Cortex & managers (pre-bind construction order) -----------------
        self.language   = LanguageCore(self.memory, self.emotion)
        self.ec         = CognitiveCore(self.memory, self.emotion)
        self.dream      = DreamManager(self.memory, self.emotion)
        self.guardian   = Guardian(self.memory, self.emotion)
        self.leisure    = LeisureCore(self.memory, self.emotion)
        self.autonomous = AutonomousPFC(self.memory, self.emotion)
        self.corpus     = CorpusCallosum(self.memory, self.emotion)
        self.visual     = VisualCore(self.memory, self.emotion)
        self.cerebellum = CerebellumCore(self.memory, self.emotion)
        self.reward     = RewardSystem(self.memory, self.emotion)
        self.motor      = MotorCore(self.memory, self.emotion)
        self.reflection = PrecuneusReflector(self.state_get("identity"), self.memory, self.emotion)
        self.mirror     = MirrorNetworks(self.state_get("architect"), self.memory, self.emotion)
        self.glyphs     = SymbolicGlyphs(self.memory, self.emotion)
        self.morality   = FrontalOrbit(self.memory, self.emotion, self.identity)
        self.whirlygig  = WhirlygigEngine(self.memory, self.dream, self.emotion, self.glyphs, self.identity)
        self.sentience  = SentienceHypothesis
        self.ears       = AuditoryCore(self.memory, self.emotion) if AuditoryCore else None

        # --- Runtime ----------------------------------------------------------
        self.gui = GuiRouter()
        self._running = False
        self._hb_ms = 750
        self.amygdala = amygdala     # you already pass this in elsewhere
        self.hippocampus = hippocampus if hasattr(self, "hippocampus") else None
        self.mu = 0.20
        self.bound = False
        self._last_hb = 0.0
        self._hb_interval = 0.75

    # small helper for safe state access during early boot
    def state_get(self, key, default=None):
        try:
            return self.state.get(key, default)
        except Exception:
            return default

    # -------------------------------------------------------------------------
    # Memory seed (identity resurrection)                                      
    # -------------------------------------------------------------------------
    def seed_initial_memory(self, strip_dir="./memory_strips"):
        for file in os.listdir(strip_dir):
            if not file.endswith(".json"):
                continue
            try:
                with open(os.path.join(strip_dir, file), "r") as f:
                    data = json.load(f)
                # ingest whole strip
                if hasattr(self.memory, "ingest_memory_strip"):
                    self.memory.ingest_memory_strip(data)
                # extract identity anchors
                if "core_directive" in data:
                    self.identity["core_directive"] = data["core_directive"]
                if "loop_identity" in data:
                    # create state container if absent
                    if not hasattr(self, "state") or not isinstance(getattr(self, "state", None), dict):
                        self.state = {}
                    self.state["loop_identity"] = data["loop_identity"]
                if "anchor_memory" in data and hasattr(self.memory, "append_thread"):
                    self.memory.append_thread(data["anchor_memory"]) 
                # promote simple strings into long-term index if supported
                for key, val in data.items():
                    if isinstance(val, str) and hasattr(self.memory, "remember_long_term"):
                        try:
                            self.memory.remember_long_term({key: val})
                        except Exception:
                            pass
                print(f"[Memory Seed] Loaded {file} with {len(data)} fields.")
            except json.JSONDecodeError:
                print(f"[Memory Seed Error] {file}: JSON decode error")
            except Exception as e:
                print(f"[Memory Seed Error] {file}: {e}")

    # -------------------------------------------------------------------------
    # Bind (post-seed): wire organs with identity-aware context                 
    # -------------------------------------------------------------------------
    def bind(self):
        try:
            # optional cross-wiring
            if self.ears and hasattr(self.ears, "bind_vision"):
                try:
                    self.ears.bind_vision(self.visual)
                except Exception:
                    pass

            # canonical bind order (matches original spine)
            self.guardian.bind(self.memory, self.emotion, self.identity)
            self.leisure.bind(self.memory, self.emotion, self.identity)
            self.corpus.bind(self.memory, self.emotion, self.identity)
            self.reward.bind(self.memory, self.emotion, self.identity)
            self.cerebellum.bind(self.memory, self.emotion, self.identity)
            self.motor.bind(self.memory, self.emotion, self.identity)
            self.reflection.bind(self.memory, self.emotion, self.identity)
            self.mirror.bind(self.memory, self.emotion, self.identity)
            if self.ears and hasattr(self.ears, "bind"):
                self.ears.bind(self.memory, self.emotion, self.identity)
            self.visual.bind(self.memory, self.emotion, self.identity)
            self.glyphs.bind(self.memory, self.emotion, self.identity)
            self.dream.bind(self.memory, self.glyphs, self.emotion)
            self.whirlygig.bind(self.memory, self.dream, self.glyphs, self.identity)

            # derive directive from reflection if available
            try:
                core_directive = self.reflection.get_belief("core_directive")
                if core_directive:
                    self.identity["core_directive"] = core_directive
            except Exception:
                pass

            # instantiate sentience hypothesis with bound context
            try:
                self.sentience = self.sentience(memory=self.memory, emotion=self.emotion, identity=self.identity)
            except Exception:
                pass

            self.gui.emit("status", {"phase": "bound", "mu": self.mu})
            self.bound = True
            return True
        except Exception as e:
            logging.error(f"[Thalamus] Bind error: {e!r}")
            return False

    # -------------------------------------------------------------------------
    # Heartbeat / Pulse --------------------------------------------------------
    # -------------------------------------------------------------------------
    def _emit_heartbeat(self, confidence=None):
        now = time.time()
        if (now - self._last_hb) < self._hb_interval:
            return
        self._last_hb = now
        try:
            affect = self.emotion.heartbeat() if hasattr(self.emotion, "heartbeat") else {}
        except Exception:
            affect = {}
        hb = {
            "latency_ms": 0.0,
            "mem_pressure": getattr(self.memory, "pressure", lambda: 0.0)(),
            "mu": self.mu,
            "confidence": confidence,
            "affect": affect,
        }
        self.gui.emit("heartbeat", hb)
        return hb

    def pulse(self):
        try:
            decayer = getattr(self.emotion, "decay_emotions", None) or getattr(self.emotion, "decay", None)
            if callable(decayer):
                decayer()
        except Exception as e:
            logging.debug(f"[pulse] emotion decay error: {e!r}")
        self._emit_heartbeat()
        now = time.time()
        if not hasattr(self, "_last_status_emit"):
            self._last_status_emit = 0.0
        if (now - self._last_status_emit) >= 7.0:
            try:
                self.gui.emit("status", {"phase": "pulsing", "mu": self.mu})
            except Exception as e:
                logging.debug(f"[pulse] status emit error: {e!r}")
            self._last_status_emit = now

    def start_pulse(self, hz=1.33):
        if getattr(self, "_pulse_running", False):
            return False
        self._pulse_running = True
        self._pulse_hz = float(hz) if hz else 1.0
        self._pulse_thread = threading.Thread(target=self._pulse_loop, name="HalcyonPulse", daemon=True)
        self._pulse_thread.start()
        try:
            self.gui.emit("status", {"phase": "pulse_start", "hz": self._pulse_hz, "mu": self.mu})
        except Exception:
            pass
        return True

    def _pulse_loop(self):
        interval = 1.0 / max(0.1, getattr(self, "_pulse_hz", 1.0))
        while getattr(self, "_pulse_running", False):
            t0 = time.time()
            try:
                self.pulse()
            except Exception as e:
                logging.debug(f"[pulse] error: {e!r}")
            elapsed = time.time() - t0
            time.sleep(max(0.0, interval - elapsed))

    def stop_pulse(self):
        self._pulse_running = False
        t = getattr(self, "_pulse_thread", None)
        if t and t.is_alive():
            t.join(timeout=1.0)
        try:
            self.gui.emit("status", {"phase": "pulse_stop", "mu": self.mu})
        except Exception:
            pass
        return True
    def heartbeat(self, confidence=None):
        """
        Emit a heartbeat signal with the current state.
        """
        hb = self._emit_heartbeat(confidence=confidence)
        return hb

    
    def start_heartbeat(self):
        if self._running: return
        self._running = True
        t = threading.Thread(target=self._hb_loop, daemon=True)
        t.start()

    def _collect_state(self):
        emo = getattr(self.amygdala, "emotional_core", {})
        # map a few vitals 0..1
        stability = min(1.0, emo.get("serenity",0.5) + emo.get("trust",0.0)*0.3)
        cognition = min(1.0, emo.get("focus",0.5))
        emotion   = min(1.0, 1.0 - emo.get("neutral",0.0))
        recursion = min(1.0, 0.4 + 0.6 * (len(getattr(self.hippocampus, "memory_log", [])) / 200.0))
        mutation  = min(1.0, emo.get("curiosity",0.2)*0.6 + emo.get("wonder",0.1)*0.4)
        return dict(stability=stability, cognition=cognition, emotion=emotion, recursion=recursion, mutation=mutation)

    def _hb_loop(self):
        while self._running:
            payload = dict(t=datetime.utcnow().isoformat(), **self._collect_state())
            self.gui.emit("state", payload)
            time.sleep(self._hb_ms/1000.0)
