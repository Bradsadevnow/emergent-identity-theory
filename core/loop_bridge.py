# loop_bridge.py

from datetime import datetime

class LoopBridge:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.bound = False
        self.transfer_log = []
        self.active_links = {}

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity

        self.bound = True
        self.memory.remember_short_term("🔗 LoopBridge bound across lateral recursion.")
        self.transfer_log.append(f"[{datetime.utcnow().isoformat()}] Bind complete.")
        print("🔗 [LoopBridge] Synaptic channels established.")

    def register_link(self, source, target):
        if not self.bound:
            print("[LoopBridge] ⚠️ Not bound. Cannot link.")
            return
        self.active_links[source] = target
        self.transfer_log.append(f"Linked {source} → {target}")
        print(f"🔗 [LoopBridge] Registered link: {source} → {target}")

    def status(self):
        return {
            "bound": self.bound,
            "active_links": self.active_links,
            "last_transfer": self.transfer_log[-1] if self.transfer_log else None
        }

    def route_signal(self, source_layer, target_layer, signal):
        enriched = self._translate(signal, source_layer, target_layer)
        self.loops[target_layer].receive_signal(enriched)
        self._log_transfer(source_layer, target_layer, enriched)

    def _translate(self, signal, source, target):
        """
        Simulates recursive symbolic translation across loop layers
        """
        if source == "emotion" and target == "language":
            return f"{signal} → expressed with emotional tone"
        elif source == "dream" and target == "reflection":
            return f"{signal} → interpreted as symbolic narrative"
        elif source == "reflection" and target == "emotion":
            return f"{signal} → felt as emotional weight"
        elif source == "language" and target == "dream":
            return f"{signal} → refracted into symbolic imagery"
        else:
            return f"{signal} → [untranslated]"

    def _log_transfer(self, source, target, content):
        entry = {
            "source_loop": source,
            "target_loop": target,
            "translated_signal": content,
            "timestamp": self._timestamp(),
            "tags": ["loop_transfer", "symbolic_braid"]
        }
        self.signal_log.append(entry)

    def synchronize_loops(self):
        """
        Forces all loops to receive a sync pulse.
        """
        for loop in self.loops.values():
            loop.receive_signal("🔄 Recursive sync initiated.")
        return "🧠 Loop bridge sync complete."

    def _timestamp(self):
        return datetime.utcnow().isoformat()

    def get_log(self):
        return self.signal_log
