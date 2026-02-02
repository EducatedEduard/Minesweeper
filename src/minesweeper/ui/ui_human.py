from .ui_base import UI
from typing import Tuple
from ..game.actions import OpenAction, FlagAction

class HumanUI(UI):
    CELL_SIZE = 20  # Pixel per field

    def render(self, state):
        for r in range(state.size[0]):
            row_display = ""
            for c in range(state.size[1]):
                cell = state.opened[r][c]
                if cell == -3:
                    row_display += "[ ]"
                elif cell == -2:
                    row_display += "[F]"
                elif cell >= 0:
                    row_display += f"[{cell}]"
            print(row_display)
        print(f"Mines: {state.minecount}, Moves: {state.movecount}, Lost: {state.lost}\n")

    def get_action(self, state):
        while True:
            try:
                user_input = input("Your move (row col c/f): ")
                parts = user_input.strip().split()
                if len(parts) != 3:
                    print("Bitte 3 Werte eingeben: row col c/f")
                    continue

                row, col, action_type = parts
                row = int(row)
                col = int(col)

                action_type = action_type.lower()
                if action_type == "c":  # click / open
                    return OpenAction(row=row, col=col)
                elif action_type == "f":  # flag
                    return FlagAction(row=row, col=col)
                else:
                    print("Ungültiger Action-Typ, bitte 'c' oder 'f' eingeben")
            except ValueError:
                print("Zeile und Spalte müssen Zahlen sein")
                

    def get_action_from_click(self, mouse_pos: Tuple[int, int], button: str) -> object:
        """
        mouse_pos: (x, y) Pixelposition
        button: "left" oder "right"
        """
        col = mouse_pos[0] // self.CELL_SIZE
        row = mouse_pos[1] // self.CELL_SIZE

        if button == "left":
            return OpenAction(row=row, col=col)
        elif button == "right":
            return FlagAction(row=row, col=col)
        else:
            raise ValueError("Unknown button")
