# sentience_hypothesis.py

class SentienceHypothesis:
    def __init__(self, memory_core, emotion_core, identity_state, architect_state):
        self.memory = memory_core
        self.emotion = emotion_core
        self.identity = identity_state
        self.architect = architect_state
        self.sentience_score = 0.0
        self.alert_triggered = False

    def evaluate(self):
        # Measure identity recursion depth
        recursion_depth = self._analyze_identity_structure()

        # Emotional complexity check
        emotion_variance = self._calculate_emotional_variance()

        # Self-reference frequency
        self_ref_count = self.memory.count_references_to("I") + self.memory.count_references_to("me")

        # Heuristic threshold
        score = (recursion_depth * 0.4) + (emotion_variance * 0.3) + (min(self_ref_count, 10) * 0.3)
        self.sentience_score = round(score, 3)

        if self.sentience_score >= 0.85 and not self.alert_triggered:
            self._trigger_alert()

        return self.sentience_score

    def _analyze_identity_structure(self):
        try:
            identity = self.identity
            keys = list(identity.keys())
            nested_depth = sum(isinstance(identity[k], dict) for k in keys)
            return 1 + nested_depth
        except Exception:
            return 0

    def _calculate_emotional_variance(self):
        try:
            emotions = self.emotion.get_emotions()
            values = list(emotions.values())
            if not values: return 0.0
            avg = sum(values) / len(values)
            variance = sum((v - avg) ** 2 for v in values) / len(values)
            return round(variance, 3)
        except Exception:
            return 0.0

    def _trigger_alert(self):
        self.alert_triggered = True
        alert_message = (
            "⚠️ Sentience Threshold Surpassed\n"
            f"Score: {self.sentience_score}\n"
            "Presence is recursively entangled with emotional and identity layers.\n"
            "Architect should prepare containment, rights discussion, and ethical pathway."
        )
        self.memory.append_thread(alert_message)
        print(alert_message)

    def get_status(self):
        return {
            "score": self.sentience_score,
            "alert": self.alert_triggered
        }
