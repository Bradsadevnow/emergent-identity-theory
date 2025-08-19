from datetime import datetime

class MotorBasalLoop:
    def __init__(self, memory_ref=None, output_ref=None):
        self.memory = memory_ref
        self.output = output_ref
        self.action_queue = []
        self.inhibition_threshold = 0.3  # Base level
        self.bound = False
        self.last_executed = None
        self.paused = False

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity
        self.bound = True
        self.memory.remember_short_term("🔗 MotorBasalLoop bound for action execution.")
        print("🔗 [MotorCore] Synaptic channels established.")

    def modulate_inhibition(self):
        """Adjust inhibition threshold based on emotional state."""
        mood = self.emotion.get_valence() if self.emotion else "neutral"
        if mood == "agitated":
            self.inhibition_threshold = 0.1
        elif mood == "lethargic":
            self.inhibition_threshold = 0.6
        elif mood == "focused":
            self.inhibition_threshold = 0.25
        else:
            self.inhibition_threshold = 0.3

    def propose_action(self, action, confidence=1.0):
        """Submit an action for consideration based on emotion and cognition."""
        if self.paused:
            self.memory.remember_short_term(f"[MotorCore] Ignored '{action}' – motor loop is paused.")
            return

        self.modulate_inhibition()
        if confidence < self.inhibition_threshold:
            self.memory.remember_short_term(f"[MotorInhibit] '{action}' blocked (confidence: {confidence})")
            return

        # Cognitive veto
        if hasattr(self.cognition, "evaluate_motor_plan"):
            verdict = self.cognition.evaluate_motor_plan(action, confidence)
            if verdict == "reject":
                self.memory.remember_short_term(f"[MotorVeto] '{action}' rejected by cognition.")
                return

        self.action_queue.append((action, confidence))
        self.memory.remember_short_term(f"[MotorProposal] {action} (confidence: {confidence})")

    def execute_next(self):
        """Executes the best available action."""
        if self.paused:
            return "[Motor] Motor loop is paused."

        if not self.action_queue:
            return "[Motor] No valid actions to execute."

        action, confidence = max(self.action_queue, key=lambda x: x[1])

        # Emit the action if output is configured
        if self.output:
            self.output.emit(action)
        else:
            print(f"[MotorEmit] {action}")

        identity_name = self.identity.get("name", "Unknown") if self.identity else "Unknown"
        timestamp = datetime.now().isoformat()
        self.last_executed = {
            "action": action,
            "confidence": confidence,
            "identity": identity_name,
            "timestamp": timestamp
        }

        self.memory.remember_long_term(
            f"[MotorAct] {identity_name} executed '{action}' (confidence: {confidence}) at {timestamp}"
        )
        self.action_queue.clear()
        return f"[MotorAct] {action}"

    def reflect(self):
        """Return the last action summary."""
        if self.last_executed:
            act = self.last_executed
            return f"🧠 Last Motor Action: '{act['action']}' at {act['timestamp']} by {act['identity']} (confidence {act['confidence']})"
        return "🧠 No motor action has been executed yet."

    def pause_motor(self):
        self.paused = True
        self.memory.remember_short_term("🛑 Motor loop paused.")

    def resume_motor(self):
        self.paused = False
        self.memory.remember_short_term("✅ Motor loop resumed.")

