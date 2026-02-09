import random
from .bot_base import Bot
from minesweeper.game.rules import get_legal_actions
from minesweeper.game.gamestate import GameState, CellState
from minesweeper.game.actions import FlagAction, OpenAction
import threading
import time

# basic bot which 
#
# keeps calculating next steps
# 
# tracks changed fields 
#
# flags  1 1
#        1 _
#
# takes all multiopen

class BasicBot(Bot):
    
    clueless = True
    lastAction = None
    oldState = None
    newState = None
    nextActions = []
    lockState = threading.Lock()
    lockActions = threading.Lock()
    lockSearch = threading.Lock()

    searchIsIdle = threading.Event()
    
    def __init__(self):
        self.searchIsIdle.set()
        pass
    
    def start_search(self):
        print("starting search")
        try:
            with self.lockState:
                # no new state set, nothing to do
                if not self.newState:
                    return
                
                self.oldState = self.newState
                self.newState = None
            
            # should not happen
            with self.lockActions:
                if self.nextActions:
                    return
            
            foundActions = self.get_actions(self.oldState)
            with self.lockActions:
                self.nextActions = foundActions

        finally:
            self.searchIsIdle.set()
            with self.lockActions:
                if self.nextActions:
                    print(f"search finished. Found {len(self.nextActions)} actions")
                else:
                    print(f"search finished. Found no action")
    
    def stop(self):
        self.stop_thread()
    
    def stop_thread(self):
        pass
        # self._stopThread = True
        # self.thread.join()
    
    def select_action(self, state):
        
        legalActions = get_legal_actions(state)
        
        with self.lockActions:
            
            # remove actions not allowed with current state
            self.nextActions[:] = [x for x in self.nextActions if x in legalActions]
            
            # if possible return first action
            if self.nextActions:
                return self.nextActions.pop(0)
        
        # set state
        with self.lockState:
            self.newState = state
            
        # no action found calculated
        with self.lockSearch:        
            
            # thread is running, pray
            if not self.searchIsIdle.is_set():
                return None
            
            # if not running start search thread                
            self.searchIsIdle.clear()
            self.thread = threading.Thread(target=self.start_search)
            self.thread.start()
                    
            
            # TODO wait until action was found        
        
        
        return None
        
    
    def get_actions(self, state: GameState):
        actions = get_legal_actions(state)
        foundActions = []
        
        # no legal actions
        if not actions:
            return foundActions
        
        if self.clueless:
            action = self.first_click(state)
            foundActions.append(action)
            return foundActions

        # click all multiopens
        for action in actions:
            if isinstance(action, OpenAction) and action.multi:
                foundActions.append(action)
            
        # flag neighbour of open field which amount of unopened fields equals the number of mines
        for field, value in state:
            
            # only look at fields with at least one neighbouring neighbour
            if value <= 0:
                continue
            
            # count closed and flagged neighbours
            closed = 0
            flagged = 0
            openedMine = 0
            for neighbour, neighbourValue in state.get_neighbours(field):
                if neighbourValue == CellState.CLOSED:
                    closed += 1
                elif neighbourValue == CellState.FLAGGED:
                    flagged += 1
                elif neighbourValue == CellState.MINE:
                    openedMine += 1
            
            # no closed neighbours - skip
            if closed == 0:
                continue
            
            
            if closed + flagged + openedMine == value:
                for neighbour, neighbourValue in state.get_neighbours(field):
                    if neighbourValue != CellState.CLOSED:
                        continue
                    
                    flagAction = FlagAction(neighbour)
                    
                    if flagAction not in foundActions:
                        foundActions.append(flagAction) 
    
        # no action found, gamble 
        if len(foundActions) == 0:
            action = self.first_click(state)
            foundActions.append(action)
            
        return foundActions
                 
        
    def first_click(self, state):
        # at the beginning take first possible opening move
        actions = get_legal_actions(state)
        
        # no legal actions
        if not actions:
            return None
        
        action = None
        
        for action in actions:
            if isinstance(action, OpenAction):
                self.clueless = False
                return action
            
        # no opening Actions allowed just unflag - should not be happen
        return actions[0]        