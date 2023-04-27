import argparse
from tic_tac_toe.game.players import RandomComputerPlayer, Player
from .players import ConsolePlayer
from tic_tac_toe.logic.models import Mark
from typing import NamedTuple

PLAYER_CLASSES = {
    "human": ConsolePlayer,
    "random": RandomComputerPlayer,
    "minimax": MinimaxComputerPlayer,
}

class Args(NamedTuple):
    player1: Player
    player2: Player
    starting_mark: Mark

def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-X",
        dest="player_x",
        choices=PLAYER_CLASSES.keys(),
        default="human",
    )
    parser.add_argument(
        "-O",
        dest="player_o",
        choices=PLAYER_CLASSES.keys(),
        default="minimax",
    )
    parser.add_argument(
        "--starting",
        dest="starting_mark",
        choices=Mark,
        type=Mark,
        default="X",
    )
    args = parser.parse_args()

    player1 = PLAYER_CLASSES[args.player_x](Mark("X"))
    player2 = PLAYER_CLASSES[args.player_o](Mark("O"))

    if args.starting_mark == "O":
        player1, player2 = player2, player1

    return Args(player1, player2, args.starting_mark)

from tic_tac_toe.game.players import (
    Player,
    RandomComputerPlayer,
    MinimaxComputerPlayer,
)