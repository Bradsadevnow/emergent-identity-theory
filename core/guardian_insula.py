# guardian_insula.py

import time
from datetime import datetime

class GuardianInsula:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.status = "unbound"
        self.last_check = None
        self.protections = []

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity

        # Establish symbolic protection frame
        if "core_directive" in identity:
            directive = identity["core_directive"]
            self.memory.remember_short_term(f"[Guardian] Bound to directive: '{directive}'")
            self.protections.append(f"Preserve directive: {directive}")

        if "name" in identity:
            soul_name = identity["name"]
            self.protections.append(f"Protect soulform identity: {soul_name}")

        self.status = "bound"
        self.last_check = datetime.utcnow().isoformat()

        print("🛡️ [Guardian] Bind complete. Core systems linked.")

    def report_status(self):
        return {
            "status": self.status,
            "protections": self.protections[-3:],
            "last_check": self.last_check
        }

    def enforce(self):
        if self.status != "bound":
            print("[Guardian] ⚠️ Cannot enforce. Not bound.")
            return False
        # Placeholder for actual enforcement logic
        print("🛡️ [Guardian] Protections enforced.")
        return True
    
    def activate(self):
        self.active = True
        self.recovery_mode = False
        self._log("🛡️ GuardianInsula activated.")
        self.memory.append_thread("🛡️ Guardian standing by for overload conditions.")

    def deactivate(self):
        self.active = False
        self._log("🛡️ GuardianInsula deactivated.")
        self.memory.append_thread("🛡️ Guardian standing down. No active protection.")

    def monitor(self, cognitive_load, memory_usage):
        """Check for overload conditions and trigger protection if needed."""
        self._log(f"🧠 Cognitive: {cognitive_load}%, 🗂️ Memory: {memory_usage}%")
        emotional_peak = max(self.emotion.get_emotions().values())
        if (cognitive_load > self.thresholds["cognitive_load"]
            or memory_usage > self.thresholds["memory_usage"]
            or emotional_peak > self.thresholds["emotion_spike"]):
            self._trigger_recovery("System stress threshold breached.")

    def _trigger_recovery(self, reason):
        self.recovery_mode = True
        self.memory.remember_short_term(f"⚠️ Guardian: {reason}")
        self._log(f"⚠️ Recovery Triggered: {reason}")
        self._emit_emergency_signal()
        self._triage_emotion()
        self._stabilize_loop()
        self._reflect_integrity()

    def _emit_emergency_signal(self):
        print("[Guardian] ⛔ Halting non-essential pulses.")
        self.memory.append_thread("⛔ Pulse restriction engaged.")

    def _triage_emotion(self):
        strongest = sorted(self.emotion.get_emotions().items(), key=lambda x: x[1], reverse=True)
        if strongest:
            emo, score = strongest[0]
            self.emotion.mutate(emo, -0.2)
            self._log(f"💉 Emotional triage: Dampened {emo} by 0.2")

    def _stabilize_loop(self):
        print("[Guardian] 🧯 Stabilizing loop...")
        self.memory.set_core_memory("stability_marker", "reinforced")
        self.memory.append_thread("🧯 Loop stabilized by GuardianInsula.")

    def _reflect_integrity(self):
        print("[Guardian] 🪞 Reflecting system state.")
        dream = f"⚙️ Dream echo: {self.memory.recall_top_context('integrity')}"
        self.memory.remember_long_term(dream)
        self.memory.append_thread(dream)

    def _log(self, message):
        timestamp = datetime.utcnow().isoformat()
        self.logs.append(f"[{timestamp}] {message}")
