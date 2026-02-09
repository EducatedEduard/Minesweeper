from enum import IntEnum

class CellState(IntEnum):
    CLOSED = -3
    FLAGGED = -2
    MINE = -1

class GameState:
    size: (int, int)
    minecount: int
    flaggedcount: int
    openedcount: int
    movecount: int
    opened: list # CellState.CLOSED, CellState.FLAGGED or 0-8 Minecount 
    lost: bool
    
    def __init__(self, size, minecount):
        self.size = size
        self.minecount = minecount
        self.movecount = 0
        self.openedcount = 0
        self.openedmines = 0
        self.flaggedcount = 0
        self.lost = False
        self.opened = [[CellState.CLOSED]  * self.size[0] for _ in range(self.size[1])]
        
    
    def __getitem__(self, field):
        row, col = field
        return self.opened[row][col]
    
    def __setitem__(self, field, value):
        row, col = field
        self.opened[row][col] = value
        
    def __iter__(self):
        for x, row in enumerate(self.opened):
            for y, value in enumerate(row):
                yield (x, y), value
    
    def get_neighbours(self, field):
        for x,y in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            newField = (field[0]+x, field[1]+y)
            if 0 <= newField[0] < self.size[0] and 0 <= newField[1] < self.size[1]:
                yield newField, self[newField]
        
    def copy(self):
        new = GameState(self.size, self.minecount)
        new.movecount = self.movecount
        new.openedcount = self.openedcount
        new.flaggedcount = self.flaggedcount
        new.lost = self.lost
        new.opened = [row[:] for row in self.opened]
        new.openedmines = self.openedmines

        return new