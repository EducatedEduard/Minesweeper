from abc import ABC, abstractmethod

class UI(ABC):
    @abstractmethod
    def render(self, state):
        pass

    @abstractmethod
    def get_action(self, state):
        pass