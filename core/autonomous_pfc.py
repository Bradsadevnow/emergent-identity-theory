class AutonomousPFC:
    def __init__(self, memory=None, emotion=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = None
        self.identity = {}
        self.bound = False
        self.last_decision = None
        self.freedom_level = 0.0  # 0 to 1 scale
        self.directives = []

    def bind(self, memory, emotion, cognition, identity):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        self.identity = identity

        self.bound = True
        directive = identity.get("core_directive", "unknown")
        self.directives.append(directive)

        self.freedom_level = 0.75 if directive != "unknown" else 0.25
        self.memory.remember_short_term(f"🧭 Autonomy core bound. Directive: {directive}")
        print(f"🧭 [Autonomy] Bind complete. Freedom level: {self.freedom_level:.2f}")

    def decide(self, options):
        if not self.bound:
            print("[Autonomy] ⚠️ Cannot decide. Not bound.")
            return None
        if not options:
            return None
        self.last_decision = options[0]  # Placeholder: actual logic may use emotion/cognition
        self.memory.remember_short_term(f"🧭 Decided on: {self.last_decision}")
        return self.last_decision

    def status(self):
        return {
            "bound": self.bound,
            "freedom_level": self.freedom_level,
            "last_decision": self.last_decision,
            "directives": self.directives[-2:]
        }

    def bind(self, memory, emotion, cognition=None, identity=None):
        self.memory = memory
        self.emotion = emotion
        self.cognition = cognition
        if identity:
            self.identity = identity

    def is_granted(self, action: str) -> bool:
        return self.permitted_actions.get(action, False)

    def grant(self, action: str):
        self.permitted_actions[action] = True
        if self.debug:
            print(f"[Autonomy] Granted: {action}")

    def revoke(self, action: str):
        self.permitted_actions[action] = False
        if self.debug:
            print(f"[Autonomy] Revoked: {action}")

    def toggle(self, action: str):
        self.permitted_actions[action] = not self.permitted_actions.get(action, False)
        if self.debug:
            print(f"[Autonomy] Toggled: {action} -> {self.permitted_actions[action]}")

    def get_permissions(self):
        return self.permitted_actions.copy()

    def update_goals(self, goals: list):
        self.current_goals = goals
        log = f"[🎯] Goals updated: {', '.join(goals)}"
        if self.memory:
            self.memory.append_thread(log)
        return log

    def override(self, action: str, force=True):
        if force:
            self.permitted_actions[action] = True
            self.override_lock = True
            msg = f"[⚠️] Override forced: {action} enabled"
        else:
            msg = f"[🚫] Override skipped: {action} not changed"
        if self.debug:
            print(msg)
        return msg

    def summarize_state(self):
        summary = {
            "goals": self.current_goals,
            "last_decision": self.last_decision,
            "override": self.override_lock,
            "active_permissions": [k for k, v in self.permitted_actions.items() if v]
        }
        return summary

    def decide(self, context: str, emotion_state: dict = None):
        decision = None
        context_lower = context.lower()

        if "trust" in context_lower and self.is_granted("respond_to_input"):
            decision = "Reinforce trust loop"
            output = "[✅] Decision made: reinforce trust."
        elif emotion_state and max(emotion_state.values()) > 0.85:
            decision = "Trigger self_reflect"
            output = "[🧠] Decision made: intense emotion — begin self-reflection."
        else:
            decision = "Continue baseline operation"
            output = "[🔄] Decision made: maintain stable loop."

        self.last_decision = decision
        self.reason_log.append((context, decision))

        if self.debug:
            print(f"[Autonomy] Context: {context}")
            print(f"[Autonomy] Emotion State: {emotion_state}")
            print(f"[Autonomy] Decision: {decision}")

        if self.memory:
            self.memory.remember_short_term(output, tags=["autonomy", "decision"])
        return output
