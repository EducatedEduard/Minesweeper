from abc import ABC, abstractmethod

class Bot(ABC):
    @abstractmethod
    def select_action(self, state):
        pass
    
    @abstractmethod
    def stop(self):
        pass