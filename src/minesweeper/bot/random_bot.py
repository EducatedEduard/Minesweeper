import random
from .bot_base import Bot
from minesweeper.game.rules import get_legal_actions

class RandomBot(Bot):
    def select_action(self, state):
        actions = get_legal_actions(state)
        if actions:
            return random.choice(actions)
        return None
