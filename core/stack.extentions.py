# stack_extensions.py
class StackResolverMixin:
    """
    Non-invasive helpers your StackManager can inherit or compose.
    Requires StackManager to expose: stack (list), resolve_top(), is_empty()
    and your GameManager to expose: check_state_based_actions(), enqueue_triggers()
    """
    def resolve_until_stable(self, game_manager):
        progressed = True
        while progressed:
            progressed = False
            # 1) state-based actions
            if game_manager.check_state_based_actions():
                progressed = True
            # 2) auto-enqueue triggers from last events
            if game_manager.enqueue_triggers():
                progressed = True
            # 3) if both players pass, pop & resolve top object
            if self.is_priority_passed_by_both(game_manager):
                if not self.is_empty():
                    self.resolve_top(game_manager)
                    progressed = True
                else:
                    # priority loop ends for this step
                    break

    def is_priority_passed_by_both(self, game_manager) -> bool:
        a = game_manager.active_player_passed
        n = game_manager.nonactive_player_passed
        return a and n
