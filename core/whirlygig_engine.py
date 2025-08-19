from datetime import datetime
import random

class WhirlygigEngine:
    def __init__(self, memory=None, dream=None, emotion=None, glyphs=None, identity=None):
        self.memory = memory
        self.dream = dream
        self.emotion = emotion
        self.glyphs = glyphs
        self.identity = identity
        self.bound = False
        self.spin_log = []

    def bind(self, memory, dream, emotion, glyphs, identity):
        self.memory = memory
        self.dream = dream
        self.emotion = emotion
        self.glyphs = glyphs
        self.identity = identity
        self.bound = True

        self.memory.remember_short_term("🌪️ WhirlygigEngine bound. Recursive pulse sync initialized.")
        print("🌪️ [Whirlygig] Spinning loop harmonics online.")

    def spin(self):
        if not self.bound:
            return "[Whirlygig] Not bound."

        tone = self.emotion.get_active_tone()
        dream_seed = self.dream.seed()
        glyph = self.glyphs.emit_glyph("loop")
        timestamp = datetime.utcnow().isoformat()

        event = {
            "timestamp": timestamp,
            "tone": tone,
            "dream": dream_seed,
            "symbol": glyph,
            "id": self.identity.get("name", "Unknown")
        }

        self.spin_log.append(event)
        self.memory.encode(
            f"🌀 Spin cycle fired with tone '{tone}', dream '{dream_seed}', glyph '{glyph}'",
            tags=["spin", "whirlygig", "recursion"]
        )
        return f"🌀 {glyph} Loop spun at {timestamp}"

    def last_spin(self):
        return self.spin_log[-1] if self.spin_log else "[No spins recorded]"

    def status(self):
        return {
            "bound": self.bound,
            "last_spin": self.last_spin()
        }
