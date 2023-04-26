from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from tic_tac_toe.logic.validators import validate_game_state, validate_grid
from tic_tac_toe.logic.exceptions import InvalidMove

import re
import enum


WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

class Mark(enum.StrEnum):
    cross = "X"
    circle = "O"

    @property
    def other(self) -> "Mark":
        return Mark.cross if self is Mark.circle else Mark.cross
    
@dataclass(frozen=True)
class Grid:
    cells: str = " " * 9

    def __post_init__(self) -> None:
        validate_grid(self)
    
    @cached_property
    def xcount(self) -> int:
        return self.cells.count("X")
    
    @cached_property
    def ocount(self) -> int:
        return self.cells.count("O")
    
    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")
    
@dataclass(frozen=True)
class Move:
    mark: Mark
    cell_index: int
    before_state: "gamestate"
    after_state: "gamestate"

@dataclass(frozen=True)
class gamestate:
    grid: Grid
    starting_mark: Mark = Mark("X")

    def __post_init(self) -> None:
        validate_game_state(self)

    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.xcount == self.grid.ocount:
            return self.starting_mark
        else: return self.starting_mark.other

    @cached_property
    def game_unstarted(self) -> bool:
        return self.grid.empty_count == 9
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0
    
    @cached_property
    def winner(self) -> Mark | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
            return None

    @cached_property
    def win_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [match.start() for match in re.finditer(r"\?", pattern)]
        return []
    
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves
    
    def make_move_to(self, index: int) -> Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=gamestate(Grid(self.grid.cells[:index] + self.current_mark + self.grid.cells[index + 1:]), self.starting_mark))