from .ui_base import UI
from typing import Tuple
from ..game.actions import OpenAction, FlagAction
from ..game.rules import get_legal_actions
from ..game.gamestate import GameState, CellState
import tkinter as tk


class HumanUI(UI):
    CELL_SIZE = 25  # Pixel per field
    state = None
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        # Statusleiste
        self.statusFraame = tk.Frame(self.root)
        self.statusFraame.pack(fill="x")

        self.minesLabel = tk.Label(self.statusFraame, anchor="w")
        self.minesLabel.pack(side="left", padx=10)

        self.movesLabel = tk.Label(self.statusFraame, anchor="w")
        self.movesLabel.pack(side="left", padx=10)

        self.flaggedLabel = tk.Label(self.statusFraame, anchor="w")
        self.flaggedLabel.pack(side="left", padx=10)
        
        self.canvas = None
        self.pending_action = None
    
    def render(self, state):
        self.state = state
        rows, cols = state.size

        # Status aktualisieren
        self.minesLabel.config(text=f"Mines: {state.minecount}")
        self.movesLabel.config(text=f"Moves: {state.movecount}")
        self.flaggedLabel.config(text=f"Unflagged Mines: {state.minecount - state.flaggedcount - state.openedmines}")
        
        if self.canvas is None:
            self.canvas = tk.Canvas(
                self.root,
                width=cols * self.CELL_SIZE,
                height=rows * self.CELL_SIZE
            )
            self.canvas.pack()

            # Maus-Events
            self.canvas.bind("<Button-1>", self._on_left_click)
            self.canvas.bind("<Button-3>", self._on_right_click)

        self.canvas.delete("all")

        for r in range(rows):
            for c in range(cols):
                x1 = c * self.CELL_SIZE
                y1 = r * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                cell = state.opened[r][c]

                # Hintergrund
                if cell == CellState.CLOSED:  # geschlossen
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
                elif cell == CellState.FLAGGED:  # Flag
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                    self.canvas.create_text(
                        (x1+x2)//2, (y1+y2)//2,
                        text="F"
                    )
                elif cell == CellState.MINE:  # offene Mine
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                    self.canvas.create_text(
                        (x1+x2)//2, (y1+y2)//2,
                        text="M"
                    )
                else:  # offen
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                    if cell > 0:
                        self.canvas.create_text(
                            (x1+x2)//2, (y1+y2)//2,
                            text=str(cell)
                        )

        self.root.update()

    def get_action(self, state):
        self.pendingAction = None
        legalActions = get_legal_actions(state)
        while True:
            while self.pendingAction is None:
                self.root.update()
                
            if self.pendingAction in legalActions:
                return self.pendingAction
            
            print("Action nicht möglich")
            self.pendingAction = None
            

    def _event_to_cell(self, event):
        return (event.y // self.CELL_SIZE, event.x // self.CELL_SIZE)

    def _on_left_click(self, event):
        field = self._event_to_cell(event)
        self.pendingAction = OpenAction(field, self.state[field] >= 0)

    def _on_right_click(self, event):
        row, col = self._event_to_cell(event)
        self.pendingAction = FlagAction((row, col))