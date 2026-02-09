from .actions import FlagAction, OpenAction
import random
from .gamestate import GameState, CellState

def get_legal_actions(gamestate):
    legalActions = []
    
    # if all fields are opened, no more moves allowed
    if gamestate.openedcount + gamestate.minecount == gamestate.size[0] * gamestate.size[1]:
        return legalActions
    
    
    for field, value in gamestate:
        if value == CellState.CLOSED:
            legalActions.append(FlagAction(field))  
            legalActions.append(OpenAction(field, False))
        elif value >= 0:
            
            # check if right amoutn of neighbours are flagged
            flagged = 0
            closed = 0
            for neighbour, neighbourValue in gamestate.get_neighbours(field):
                if neighbourValue == CellState.FLAGGED or neighbourValue == CellState.MINE:
                    flagged += 1
                elif neighbourValue == CellState.CLOSED:
                    closed += 1
                    
            if value <= flagged and closed > 0:
                legalActions.append(OpenAction(field, True))

        elif value == CellState.FLAGGED:
            legalActions.append(FlagAction(field))
             
        
    return legalActions

def apply_action(board, gamestate, action):

    if isinstance(action, OpenAction):
        board = click_field(board, gamestate, action.field)
    
    elif isinstance(action, FlagAction):
        flag_field(board, gamestate, action.field)        
        
    return gamestate.copy(), board

def click_field(board, gamestate, field):
        if not board:
            board = generate_board(gamestate, field)
        
        elif gamestate[field] >= 0:
            multi_open(board, gamestate, field)
            gamestate.movecount += 1
            return board
        
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

    # check if right amoutn of neighbours are flagged
    flagged = 0
    closed = 0
    for neighbour, neighbourValue in gamestate.get_neighbours(field):
        if neighbourValue == CellState.FLAGGED or neighbourValue == CellState.MINE:
            flagged += 1
        elif neighbourValue == CellState.CLOSED:
            closed += 1
    
    # TODO remove should not happen        
    if gamestate[field] > flagged:
        raise ValueError("Number of flagged neighbours is insufficient")
    if closed == 0:
        raise ValueError("No fields to open")
    
    for neighbour, neighbourValue in gamestate.get_neighbours(field):
        if neighbourValue == CellState.CLOSED:
            open_field(board, gamestate, neighbour)
    
def open_field(board, gamestate, field):
    
    if gamestate[field] != CellState.CLOSED:
        return
    
    # open neighbours if no mines
    if board[field[0]][field[1]] == 0 and gamestate[field] != 0:
        gamestate[field] = board[field[0]][field[1]]
        gamestate.openedcount += 1
        for neighbour, _ in gamestate.get_neighbours(field):
            open_field(board, gamestate, neighbour)
        return
                        
    gamestate[field] = board[field[0]][field[1]]
    gamestate.openedcount += 1
    
    if board[field[0]][field[1]] == CellState.MINE:
        gamestate.openedmines += 1
        gamestate.lost = True
        return

    # print(f"Fehlende Felder {gamestate.size[0]*gamestate.size[1]-gamestate.flaggedcount-gamestate.openedcount}")
        
def generate_board(gamestate, field):
        
        board = [[0]  * gamestate.size[0] for _ in range(gamestate.size[1])]
        
        mines = random.sample([(x, y) for x in range(gamestate.size[0]) for y in range(gamestate.size[1]) if (x, y) != field], gamestate.minecount)
        for mine in mines:
            for neighbour, _ in gamestate.get_neighbours(mine):
                if board[neighbour[0]][neighbour[1]] != CellState.MINE: 
                    board[neighbour[0]][neighbour[1]] += 1
            
            board[mine[0]][mine[1]] = CellState.MINE
        
        return board