class GameState:
    size: (int, int)
    minecount: int
    movecount: int
    opened: list # -3 closed, -2 flaged, rests like board 
    lost: bool
    
    def __init__(self, size, minecount):
        self.size = size
        self.minecount = minecount
        self.movecount = 0
        self.lost = False
        self.opened = [[-3]  * self.size[0] for _ in range(self.size[1])]
        
        
    def get_neighbours(self, field):
        neighbours = []
        for x,y in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            if 0 <= field[0]+x < self.size[0] and 0 <= field[1]+y < self.size[1]:
                neighbours.append((field[0]+x, field[1]+y))
                
        return neighbours        
        
    def copy(self):
        new = GameState(self.size, self.minecount)
        new.movecount = self.movecount
        new.lost = self.lost
        new.opened = [row[:] for row in self.opened]

        return new