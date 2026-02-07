from .gamestate import GameState, CellState
from .rules import get_legal_actions, apply_action

class Game:
    board: list #-1 mine, 0-8 field 
    
    def __init__(self, initial_state: GameState):
        self.gamestate = initial_state
        self.board = None

    def step(self, action):
        if action not in get_legal_actions(self.gamestate):
            raise ValueError("Illegal action")

        self.gamestate, self.board = apply_action(self.board, self.gamestate, action)
        return self.gamestate.copy()

    def reset_gamestate(self):
        self.gamestate.movecount = 0 
        self.gamestate.lost = False
        self.gamestate.opened == [[CellState.CLOSED] * self.gamestate.size[0]] * self.gamestate.size[1]
        self.board = None