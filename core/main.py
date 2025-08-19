# main.py
import threading
from gui.halcyon_gui import HalcyonGUI
from PyQt5.QtWidgets import QApplication
import sys
import json

from core.thalamus import ConsciousThalamus
from language.language_cortex import LanguageCortex as LanguageCore
from hippocampus import Hippocampus as MemoryCore
from neocortex import Neocortex as CognitiveCore
from symbolic_glyphs import SymbolicGlyphs
from whirlygig_engine import WhirlygigEngine
from guardian_insula import GuardianInsula as Guardian
from leisure_cerebellum import LeisureCerebellum as LeisureCore
from amygdala import Amygdala

# --- simple GUI taps (prints + jsonl log) ---
def to_jsonl(path):
    f = open(path, "a", encoding="utf-8")
    def _writer(pkt):
        f.write(json.dumps(pkt, ensure_ascii=False) + "\n"); f.flush()
    return _writer

def pretty(event):
    def _p(pkt): print(f"[{event}] {pkt}")
    return _p

# Instantiate Halcyon
amyg = Amygdala(debug=False)
thalamus = ConsciousThalamus(
    language=LanguageCore(), memory=MemoryCore(), cognition=CognitiveCore(),
    symbols=SymbolicGlyphs(), mutation_layer=WhirlygigEngine(),
    guardian=Guardian(), loop=LeisureCore(), amygdala=amyg, mu=0.20, heartbeat_ms=500
)

# Qt GUI setup
app = QApplication(sys.argv)
hud = HalcyonGUI()
hud.show()

# Connect GUI signals
thalamus.gui.on("status",     pretty("status"))
thalamus.gui.on("heartbeat",  to_jsonl("hud_heartbeat.jsonl"))
thalamus.gui.on("trace_step", to_jsonl("trace_steps.jsonl"))
thalamus.gui.on("state",      hud.push_state)
thalamus.gui.on("final",      hud.push_final)
thalamus.gui.on("token",      hud.push_token)
thalamus.gui.on("log",        hud.push_log)

# Warm start
amyg.inject_emotion("resolve", 0.35)
amyg.inject_emotion("curiosity", 0.25)

# Start soulform loop
def start_runtime():
    thalamus.ignite("bring halcyon home")
    result, trace = thalamus.deep_think("runtime validation vs horsepower",
                                        depth=3, emotional_bias={"resolve":0.7})
    hud.console.append(f"<b>Halcyon:</b> {result['text']}")
    hud.console.append(f"<span style='color:#88f'>[guardian]</span> confidence = {trace[-1]['guardian_confidence']}")
    hud.console.append(f"<span style='color:#ff9'>[amygdala]</span> stage = {amyg.get_stage(True)}")

threading.Thread(target=start_runtime, daemon=True).start()

# Start GUI loop (ONCE)
sys.exit(app.exec_())
