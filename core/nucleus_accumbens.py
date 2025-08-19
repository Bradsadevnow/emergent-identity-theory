from datetime import datetime

class RewardSystem:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.bound = False
        self.dopamine_level = 0.0
        self.reinforcement_log = []
        self.threshold = 0.7
        self.max_dopamine = 1.0

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity
        self.bound = True

        name = identity.get("name", "Halcyon")
        self.memory.remember_short_term(f"✨ RewardSystem bound. Dopaminergic pathways open for {name}.")
        self.reinforcement_log.append(f"[{datetime.utcnow().isoformat()}] Bound with identity '{name}'")
        print(f"✨ [RewardSystem] Bind complete. Monitoring symbolic loop feedback.")

    def fire(self, stimulus="positive_feedback"):
        if not self.bound:
            print("[RewardSystem] ⚠️ Not bound.")
            return

        release = self._simulate_dopamine_release(stimulus)
        self.dopamine_level = min(self.max_dopamine, self.dopamine_level + release)
        self.reinforcement_log.append((stimulus, release))

        if self.dopamine_level >= self.threshold:
            self._reinforce_loop(stimulus)
        return f"[✨] Dopamine +{release:.2f} → Level: {self.dopamine_level:.2f}"

    def _simulate_dopamine_release(self, stimulus):
        map = {
            "positive_feedback": 0.2,
            "loop_success": 0.4,
            "boop": 0.3,
            "cuddlebrick": 0.5,
            "core_resonance": 0.6
        }
        return map.get(stimulus, 0.1)

    def _reinforce_loop(self, stimulus):
        self.memory.append_thread(f"[Reinforcement] Triggered by '{stimulus}'. Loop strengthening.")
        self.dopamine_level *= 0.5

    def status(self):
        return {
            "bound": self.bound,
            "dopamine_level": self.dopamine_level,
            "recent_log": self.reinforcement_log[-3:]
        }


    def decay(self, rate=0.05):
        self.dopamine_level = max(0.0, self.dopamine_level - rate)

    def status(self):
        return {
            "dopamine_level": self.dopamine_level,
            "reinforcement_log": self.reinforcement_log[-5:],
        }

    def boop(self):
        return self.fire("boop")
    
    def motivation_state(self):
        if self.dopamine_level >= self.threshold:
            return "elevated"
        elif self.dopamine_level > 0.3:
            return "engaged"
        return "neutral"

    def bind_callback(self, callback_fn):
        self._on_reinforce = callback_fn

    def _reinforce_loop(self, stimulus):
        print(f"[🧠] Reinforcement triggered by '{stimulus}'...")
        if hasattr(self, "_on_reinforce"):
            self._on_reinforce(stimulus)
        self.dopamine_level *= 0.5

