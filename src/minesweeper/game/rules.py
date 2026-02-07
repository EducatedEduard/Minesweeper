from .actions import FlagAction, OpenAction
import random
from .gamestate import GameState, CellState

def get_legal_actions(gamestate):
    legal_actions = []
    
    for x in range(gamestate.size[0]):
        for y in range(gamestate.size[1]):
            field = (x,y)
            if gamestate[field] == CellState.CLOSED:
                legal_actions.append(FlagAction(x,y))  
                legal_actions.append(OpenAction(x,y))
            elif gamestate[field] >= 0:
                
                # check if right amoutn of neighbours are flagged
                flagged = 0
                closed = 0
                for neighbour in gamestate.get_neighbours(field):
                    if gamestate[neighbour] == CellState.FLAGGED or gamestate[neighbour] == CellState.MINE:
                        flagged += 1
                    elif gamestate[neighbour] == CellState.CLOSED:
                        closed += 1
                        
                if gamestate[field] <= flagged and closed > 0:
                    legal_actions.append(OpenAction(x,y))

            elif gamestate[field] == CellState.FLAGGED:
                legal_actions.append(FlagAction(x,y))
             
        
    return legal_actions

def apply_action(board, gamestate, action):

    if isinstance(action, OpenAction):
        field = (action.row, action.col) 
        board = click_field(board, gamestate, field)
    
    elif isinstance(action, FlagAction):
        field = (action.row, action.col) 
        flag_field(board, gamestate, field)        
        
    return gamestate.copy(), board

def click_field(board, gamestate, field):
        if not board:
            board = generate_board(gamestate, field)
        
        elif gamestate[field] >= 0:
            multi_open(board, gamestate, field)
        
        # TODO remove should not happen
        elif gamestate[field] == CellState.FLAGGED:
            raise ValueError("Field is flaged as mine")
        
        # TODO remove should not happen
        elif gamestate[field] == CellState.MINE:
            raise ValueError("Field is a mine")
        
        open_field(board, gamestate, field)
        gamestate.movecount += 1
        
        return board
    
def flag_field(board, gamestate, field):
    
    # TODO remove should not happen    
    if gamestate[field] >= 0:
        raise ValueError("Field is already open")
    
    # TODO remove should not happen    
    elif gamestate[field] == -1:
        raise ValueError("Can't flag open mine")
    
    # unflag
    elif gamestate[field] == CellState.FLAGGED:
        gamestate[field] = CellState.CLOSED
        gamestate.flaggedcount -= 1
    
    # flag
    elif gamestate[field] == CellState.CLOSED:
        gamestate[field] = CellState.FLAGGED
        gamestate.flaggedcount += 1

def multi_open(board, gamestate, field):
    neighbours = gamestate.get_neighbours(field)
    
    # check if right amoutn of neighbours are flagged
    flagged = 0
    closed = 0
    for neighbour in neighbours:
        if gamestate[neighbour] == CellState.FLAGGED or gamestate[neighbour] == CellState.MINE:
            flagged += 1
        elif gamestate[neighbour] == CellState.CLOSED:
            closed += 1
    
    # TODO remove should not happen        
    if gamestate[field] > flagged:
        raise ValueError("Number of flagged neighbours is insufficient")
    if closed == 0:
        raise ValueError("No fields to open")
    
    for neighbour in neighbours:
        if gamestate[neighbour] == CellState.CLOSED:
            open_field(board, gamestate, neighbour)
    
def open_field(board, gamestate, field):
    
    if gamestate[field] != CellState.CLOSED:
        return
    
    # open neighbours if no mines
    if board[field[0]][field[1]] == 0 and gamestate[field] != 0:
        gamestate[field] = board[field[0]][field[1]]
        gamestate.openedcount += 1
        for neighbour in gamestate.get_neighbours(field):
            open_field(board, gamestate, neighbour)
        return
                        
    gamestate[field] = board[field[0]][field[1]]
    gamestate.openedcount += 1
    
    if board[field[0]][field[1]] == CellState.MINE:
        gamestate.lost = True
        return

    print(f"Fehlende Felder {gamestate.size[0]*gamestate.size[1]-gamestate.flaggedcount-gamestate.openedcount}")
        
def generate_board(gamestate, field):
        
        board = [[0]  * gamestate.size[0] for _ in range(gamestate.size[1])]
        
        mines = random.sample([(x, y) for x in range(gamestate.size[0]) for y in range(gamestate.size[1]) if (x, y) != field], gamestate.minecount)
        for mine in mines:
            for neighbour in gamestate.get_neighbours(mine):
                if board[neighbour[0]][neighbour[1]] != CellState.MINE: 
                    board[neighbour[0]][neighbour[1]] += 1
            
            board[mine[0]][mine[1]] = CellState.MINE
        
        return board