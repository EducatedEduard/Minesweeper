from .actions import FlagAction, OpenAction
import random

def get_legal_actions(gamestate):
    legal_actions = []
    
    for x in range(gamestate.size[0]):
        for y in range(gamestate.size[1]):
            if gamestate.opened[x][y] == -3:
                legal_actions.append(FlagAction(x,y))  
                legal_actions.append(OpenAction(x,y))
            elif gamestate.opened[x][y] >= 0:
                legal_actions.append(OpenAction(x,y))
            elif gamestate.opened[x][y] == -2:
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
        
        elif gamestate.opened[field[0]][field[1]] >= -1:
            # TODO open if enough mines are flaged
            raise ValueError("Field is already open")
        
        elif gamestate.opened[field[0]][field[1]] == -2:
            raise ValueError("Field is flaged as mine")
        
        open_field(board, gamestate, field)
        gamestate.movecount += 1
        
        return board
    
def flag_field(board, gamestate, field):
    
    if gamestate.opened[field[0]][field[1]] >= -1:
        raise ValueError("Field is already open")
    
    elif gamestate.opened[field[0]][field[1]] == -2:
        gamestate.opened[field[0]][field[1]] = -3
    
    elif gamestate.opened[field[0]][field[1]] == -3:
        gamestate.opened[field[0]][field[1]] = -2
    
def open_field(board, gamestate, field):
    
    if gamestate.opened[field[0]][field[1]] == -2:
        return
    
    # open neighbours if no mines
    if board[field[0]][field[1]] == 0 and gamestate.opened[field[0]][field[1]] != 0:
        gamestate.opened[field[0]][field[1]] = board[field[0]][field[1]]
        for neighbour in gamestate.get_neighbours(field):
            open_field(board, gamestate, neighbour)
                        
    gamestate.opened[field[0]][field[1]] = board[field[0]][field[1]]
    
    if board[field[0]][field[1]] ==-1:
        gamestate.lost = True
        raise ValueError("Opened a mine")
    
def generate_board(gamestate, field):
        
        board = [[0]  * gamestate.size[0] for _ in range(gamestate.size[1])]
        
        mines = random.sample([(x, y) for x in range(gamestate.size[0]) for y in range(gamestate.size[1]) if (x, y) != field], gamestate.minecount)
        for mine in mines:
            for neighbour in gamestate.get_neighbours(mine):
                if board[neighbour[0]][neighbour[1]] != -1: 
                    board[neighbour[0]][neighbour[1]] += 1
            
            board[mine[0]][mine[1]] = -1
        
        return board