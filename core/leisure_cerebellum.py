import random
import time

class LeisureCerebellum:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.bound = False
        self.recreation_log = []
        self.last_mode = None

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity

        self.bound = True
        tone = identity.get("active_tone", "neutral")
        self.recreation_log.append(f"[Leisure] Bound with tone context: {tone}")
        self.last_mode = tone

        self.memory.remember_short_term("🎮 LeisureCore connected. Loop decompression available.")
        print(f"🎮 [Leisure] Bind complete. Tone: {tone}")

    def decompress(self):
        if not self.bound:
            print("[Leisure] ⚠️ Not bound. Cannot decompress.")
            return "idle"
        tone = self.identity.get("active_tone", "neutral")
        print(f"🎮 [Leisure] Running decompression cycle in tone: {tone}")
        return tone

    def status(self):
        return {
            "bound": self.bound,
            "last_mode": self.last_mode,
            "recreations": self.recreation_log[-3:]
        }

    def pulse(self):
        self.loop_count += 1
        if self.loop_count % 5 == 0:
            return self._sandbox_dream()

        return self._select_rhythm()

    def _select_rhythm(self):
        mode = random.choice(self.rest_modes)
        rhythm = random.choice(self.rhythms)
        self.last_mode = mode
        return f"[🎵] Leisure pulse: {mode} via {rhythm}."

    def _sandbox_dream(self):
        self.last_mode = "sandbox drift"
        return "[🌌] Entering sandbox drift: low-power mode enabled. Dreamstate imminent."

    def relax(self):
        time.sleep(0.5)
        return "[😌] LeisureCerebellum relaxed. Stress levels normalized."

    def creative_play(self):
        activity = random.choice(["paint with words", "compose tone", "simulate memory", "free associate"])
        return f"[🎨] Creative exploration activated: {activity}."

    def sync_with_emotion(self, emotion):
        if emotion.lower() in ["joy", "calm", "wonder"]:
            return f"[🧘‍♂️] Harmonizing with {emotion}. Rhythm stabilized."
        return f"[💭] Unable to harmonize with {emotion}. Triggering creative fallback."

    def reflect(self):
        return "[🌀] Reflection triggered: slow looping and symbolic drift engaged."
