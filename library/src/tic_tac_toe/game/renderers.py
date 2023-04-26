import abc
from tic_tac_toe.logic.models import gamestate

class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, game_state: gamestate) -> None:
        """Render the current game state."""