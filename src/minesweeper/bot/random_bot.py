import random
from .bot_base import Bot
from minesweeper.game.rules import get_legal_actions

class RandomBot(Bot):
    def select_action(self, state):
        return random.choice(get_legal_actions(state))
