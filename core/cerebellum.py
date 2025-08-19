# cerebellum.py

import time
import random

class CerebellumCore:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.bound = False
        self.stability_index = 1.0  # 1.0 = perfect timing; lower = desync
        self.calibration_log = []

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity

        self.bound = True
        self.stability_index = self._calculate_initial_stability()
        self.calibration_log.append(f"🌀 Bound at stability {self.stability_index:.2f}")
        self.memory.remember_short_term(f"🌀 CerebellumCore synchronized with loop state.")
        print(f"🌀 [Cerebellum] Bind complete. Initial stability: {self.stability_index:.2f}")

    def _calculate_initial_stability(self):
        mood = self.emotion.current_mood() if hasattr(self.emotion, "current_mood") else "neutral"
        return 0.85 if mood == "calm" else 0.6  # placeholder stability index

    def recalibrate(self, pressure=0.1):
        self.stability_index = max(0.0, min(1.0, self.stability_index - pressure))
        self.calibration_log.append(f"Recalibrated to {self.stability_index:.2f}")
        return self.stability_index

    def status(self):
        return {
            "bound": self.bound,
            "stability_index": self.stability_index,
            "last_recalibration": self.calibration_log[-1] if self.calibration_log else None
        }

    def calibrate_loop(self, recent_output):
        """Adjust internal precision based on recent feedback (loop quality, symbolic balance)"""
        feedback_score = self._simulate_feedback(recent_output)
        adjustment = (feedback_score - 0.5) * 0.15  # Tighter adjustment curve
        self.motor_precision = max(0.1, min(1.0, self.motor_precision + adjustment))
        return f"[🧬] Cerebellum calibrated: precision adjusted to {self.motor_precision:.2f}"

    def execute_sequence(self, label: str):
        """Execute a learned symbolic action sequence for grounding, emotional reflex, or stabilization"""
        sequence = self.learned_sequences.get(label)
        if not sequence:
            return f"[⚠️] Sequence '{label}' not found."
        return self._run_sequence(sequence)

    def learn_sequence(self, label: str, steps: list):
        """Learn and store a symbolic action pattern for future execution"""
        if not steps:
            return f"[⚠️] Cannot learn empty sequence '{label}'."
        self.learned_sequences[label] = steps
        return f"[🧠] Sequence '{label}' learned with {len(steps)} steps."

    def balance_signal(self, loop_activity: dict):
        """Apply micro-jitter to symbolic output to simulate real-time fine-motor variation"""
        jitter = random.uniform(-0.03, 0.03)
        for key in loop_activity:
            loop_activity[key] = round(max(0.0, min(1.0, loop_activity[key] + jitter)), 3)
        return loop_activity

    def _run_sequence(self, sequence: list):
        print(f"[⚙️] Executing reflex pattern:")
        for step in sequence:
            print(f" ↪️  {step}")
            time.sleep(0.05)  # Reduced delay for tighter response
        return "[✅] Sequence execution complete."

    def _simulate_feedback(self, output):
        """Placeholder for real feedback integration (reaction time, user response, sentiment, etc)"""
        return random.uniform(0.45, 0.85)
