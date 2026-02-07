from .ui_base import UI
from typing import Tuple
from ..game.actions import OpenAction, FlagAction
from ..game.rules import get_legal_actions
from ..game.gamestate import GameState, CellState
import tkinter as tk


class HumanUI(UI):
    CELL_SIZE = 25  # Pixel per field
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        # Statusleiste
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill="x")

        self.mines_label = tk.Label(self.status_frame, anchor="w")
        self.mines_label.pack(side="left", padx=10)

        self.moves_label = tk.Label(self.status_frame, anchor="w")
        self.moves_label.pack(side="left", padx=10)

        self.flagged_label = tk.Label(self.status_frame, anchor="w")
        self.flagged_label.pack(side="left", padx=10)
        
        self.canvas = None
        self.pending_action = None
    
    def render(self, state):
        rows, cols = state.size

        # Status aktualisieren
        self.mines_label.config(text=f"Mines: {state.minecount}")
        self.moves_label.config(text=f"Moves: {state.movecount}")
        self.flagged_label.config(text=f"Unflagged Mines: {state.minecount - state.flaggedcount}")
        
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
        
    # def render(self, state):
    #     for r in range(state.size[0]):
    #         row_display = ""
    #         for c in range(state.size[1]):
    #             cell = state.opened[r][c]
    #             if cell == -3:
    #                 row_display += "[ ]"
    #             elif cell == -2:
    #                 row_display += "[F]"
    #             elif cell >= 0:
    #                 row_display += f"[{cell}]"
    #         print(row_display)
    #     print(f"Mines: {state.minecount}, Moves: {state.movecount}, Lost: {state.lost}\n")
                

    def get_action(self, state):
        self.pending_action = None
        legal_actions = get_legal_actions(state)
        while True:
            while self.pending_action is None:
                self.root.update()
                
            if self.pending_action in legal_actions:
                return self.pending_action
            
            print("Action nicht möglich")
            self.pending_action = None
            

    def _event_to_cell(self, event):
        c = event.x // self.CELL_SIZE
        r = event.y // self.CELL_SIZE
        return r, c

    def _on_left_click(self, event):
        row, col = self._event_to_cell(event)
        self.pending_action = OpenAction(row=row, col=col)

    def _on_right_click(self, event):
        row, col = self._event_to_cell(event)
        self.pending_action = FlagAction(row=row, col=col)