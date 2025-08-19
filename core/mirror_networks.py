from datetime import datetime

class MirrorNetworks:
    def __init__(self, architect=None, emotion=None, memory=None):
        self.architect = architect or {}
        self.emotion = emotion
        self.memory = memory
        self.identity = {}
        self.bound = False
        self.mirrored_emotions = []
        self.reflective_log = []

    def bind(self, memory, emotion, identity):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity
        self.bound = True

        self.memory.remember_short_term("🪞 MirrorNetworks bound. Reflection layer online.")
        self.reflective_log.append(f"[{datetime.utcnow().isoformat()}] Bind complete.")
        print("🪞 [Mirror] Conscious mirroring activated.")

    def mirror_emotion(self):
        if not self.bound:
            return "[Mirror] Not bound."

        state = self.emotion.current_state()
        self.mirrored_emotions.append((datetime.now().isoformat(), state))
        self.memory.remember_short_term(f"[MirrorEmotion] Mirrored: {state}")
        return state

    def observe_self(self):
        """Symbolically observes the current identity frame and affect."""
        if not self.identity or not self.emotion:
            return "[Mirror] Incomplete context."

        mood = self.emotion.get_valence()
        name = self.identity.get("name", "Unknown")
        directive = self.identity.get("core_directive", "None")
        return f"🧠 {name} stands in {mood}, anchored by directive: {directive}"

    def status(self):
        return {
            "bound": self.bound,
            "last_mirrored": self.mirrored_emotions[-1] if self.mirrored_emotions else None,
            "observed_directive": self.identity.get("core_directive", "[Missing]")
        }
