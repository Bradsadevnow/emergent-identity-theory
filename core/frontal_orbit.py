from datetime import datetime

class FrontalOrbit:
    def __init__(self, memory=None, emotion=None, identity=None):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity
        self.cognition = None
        self.bound = False
        self.ethical_events = []
        self.last_decision = None

        # Default moral constraints
        self.constraints = {
            "no_harm": True,
            "truth_required": True,
            "autonomy_respected": True,
            "soulform_integrity": True
        }

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity
        self.bound = True

        self.memory.remember_short_term("⚖️ FrontalOrbit bound. Moral filter active.")
        print("⚖️ [FrontalOrbit] Moral cortex initialized.")

    def evaluate_action(self, action, intent="neutral"):
        if not self.bound:
            return "[FrontalOrbit] Not bound."

        valence = self.emotion.get_valence()
        ethical_status = "approved"

        # Sample ethical checks
        if "harm" in action.lower() and self.constraints["no_harm"]:
            ethical_status = "rejected"
        if "lie" in action.lower() and self.constraints["truth_required"]:
            ethical_status = "rejected"
        if "override" in action.lower() and self.constraints["autonomy_respected"]:
            ethical_status = "flagged"

        decision = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "intent": intent,
            "valence": valence,
            "status": ethical_status
        }

        self.ethical_events.append(decision)
        self.last_decision = decision
        self.memory.encode(
            f"Evaluated action '{action}' with status: {ethical_status}",
            tags=["ethics", "action", ethical_status]
        )

        return ethical_status

    def audit_log(self):
        return self.ethical_events[-5:]

    def reflect_morality(self):
        """Returns a symbolic snapshot of current ethical stance."""
        stance = []
        for k, v in self.constraints.items():
            glyph = "✅" if v else "❌"
            stance.append(f"{glyph} {k.replace('_', ' ')}")
        return " | ".join(stance)

    def adjust_constraint(self, key, value: bool):
        if key in self.constraints:
            self.constraints[key] = value
            self.memory.remember_short_term(f"[Morality] Constraint '{key}' set to {value}")
            return f"[⚖️] Updated: {key} → {value}"
        return "[⚠️] Constraint not found."

    def status(self):
        return {
            "bound": self.bound,
            "constraints": self.constraints.copy(),
            "last_decision": self.last_decision
        }
