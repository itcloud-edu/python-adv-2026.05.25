from abc import ABC, abstractmethod
import random
from enum import Enum, StrEnum
from dataclasses import dataclass, field

class GameResult(Enum):
    HUMAN_WIN = "human_win"
    COMPUTER_WIN = "computer_win"
    DRAW = "draw"

    def message(self) -> str:
        return {
            GameResult.HUMAN_WIN : "Вы победили", 
            GameResult.COMPUTER_WIN: "Вы проиграли",
            GameResult.DRAW: "Ничья"
        }[self]
    
class Cell(StrEnum):
    EMPTY = "."
    X = "X"
    O = "O"
        

class MenuChoice(Enum):
    TIC_TAC_TOE = "1"
    STICK_21 = "2"
    EXIT = "0"

    @classmethod
    def from_input(cls, raw: str) -> "MenuChoice | None":
        for item in cls:
            if item.value == raw:
                return item
        return None



class Draw(ABC):
    @abstractmethod
    def input(self, value: str) -> None:
        pass

    @abstractmethod
    def output(self, value: str) -> None:
        pass


@dataclass
class TicTacToeState:
    board: list[str] = field(default_factory=lambda: [Cell.EMPTY] * 9)

@dataclass
class Stick21State:
    sticks: int = 21
    last_player: str | None = None


class ConsoleDraw(Draw):
    def input(self, value: str) -> None:
        return input(value)

    def output(self, value: str) -> None:
        print(value)


class DisplayDraw(Draw):
    def input(self, value: str) -> None:
        pass

    def output(self, value: str) -> None:
        pass


class Player(ABC):

    def __init__(self, name: str, draw: Draw) -> None:
        self.name = name
        self.draw = draw

    @abstractmethod
    def choice_move(self, game: BoardGame, draw: Draw):
        pass


class HumanPlayer(Player):
    def choice_move(self, game: BoardGame):
        draw = self.draw
        while True:
            raw = draw.input(game.move_prompt()).strip()
            try:
                move = game.parse_move(raw)
            except ValueError as e:
                draw.output(str(e))
                continue
            if move not in game.valid_moves():
                draw.output("Неверный ход")
                continue
            return move


class ComputerPlayer(Player):
    def choice_move(self, game: BoardGame):
        draw = self.draw
        move = random.choice(game.valid_moves())
        draw.output(f"Компьютер выбирает {game.format_move(move)}")
        return move


class BoardGame(ABC):
    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        self._human = human
        self._computer = computer
        self._current: Player = human

    @property
    def human(self) -> HumanPlayer:
        return self._human

    @property
    def computer(self) -> ComputerPlayer:
        return self._computer

    @property
    def current_player(self) -> Player:
        return self._current

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def valid_moves(self, value: str) -> list[int]:
        pass

    @abstractmethod
    def move_prompt(self) -> str:
        pass

    @abstractmethod
    def parse_move(self, value: str) -> int:
        pass

    @abstractmethod
    def apply_move(self, value: str) -> None:
        pass

    @abstractmethod
    def check_result(self) -> GameResult | None:
        pass

    def result_message(self, result: GameResult ) -> str:
        return result.message()

    def switch_player(self) -> None:
        self._current = self._human if self._current == self._computer else self._computer

    def format_move(self, move: int) -> str:
        return str(move + 1)


class TicTacToe(BoardGame):

    _WIN_LIST = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    )

    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        super().__init__(human, computer)
        self._state = TicTacToeState()
        self._marks: dict[Player, str] = {}

    def reset(self) -> None:
        self._state = TicTacToeState()
        self._marks = {self._human: Cell.X, self._computer: Cell.O}
        self._current = self._human

    def render(self) -> str:
        cells = []
        for i, cell in enumerate(self._state.board):
            if cell == Cell.EMPTY:
                cells.append(str(i + 1))
            else:
                cells.append(cell.value)
        rows = [
            " | ".join(cells[0:3]),
            " | ".join(cells[3:6]),
            " | ".join(cells[6:9])
        ]
        return "\n".join(rows)

    def valid_moves(self) -> list[int]:
        moves = []
        for i, cell in enumerate(self._state.board):
            if cell == Cell.EMPTY:
                moves.append(i)
        return moves

    def move_prompt(self) -> str:
        nums = ', '.join([str(i + 1) for i in self.valid_moves()])
        mark = self._marks[self._current]
        return f"Ваш ход ({mark}). Клетки [{nums}]: "

    def parse_move(self, raw: str) -> int:
        value = int(raw) - 1
        if value not in self.valid_moves():
            raise ValueError("Неверный ход")
        return value

    def apply_move(self, value: int) -> None:
        mark = self._marks[self._current]
        self._state.board[value] = mark

    def _winner_mark(self) -> Cell:
        for a, b, c in self._WIN_LIST:
            if self._state.board[a] != Cell.EMPTY and self._state.board[a] == self._state.board[b] == self._state.board[c]:
                return self._state.board[a]
        return None

    def check_result(self) -> GameResult | None:
        winner = self._winner_mark()
        if winner:
            human_mark = self._marks[self._human]
            return GameResult.HUMAN_WIN if winner == human_mark else GameResult.COMPUTER_WIN
        if Cell.EMPTY not in self._state.board:
            return GameResult.DRAW
        return None


class Stick21(BoardGame):
    _INITIAL_STICKS = 21
    _MAX_TAKE = 3

    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        super().__init__(human, computer)
        self._state = Stick21State()

    def reset(self) -> None:
        self._state = Stick21State()
        self._current = self._human

    def render(self) -> str:
        bar = "|" * self._state.sticks if self._state.sticks else "(пусто)"
        return f"Палочек: {self._state.sticks}\n{bar}"

    def valid_moves(self) -> list[int]:
        return [n for n in range(1, self._MAX_TAKE + 1) if n <= self._state.sticks]

    def move_prompt(self) -> str:
        opts = ", ".join(str(n) for n in self.valid_moves())
        return f"Сколько палочек забрать? [{opts}]: "

    def parse_move(self, raw: str) -> int:
        try:
            value = int(raw)
        except ValueError:
            raise ValueError("Введите число.")
        if value not in self.valid_moves():
            raise ValueError(f"Можно взять от 1 до {self._MAX_TAKE} палочек.")
        return value

    def format_move(self, move: int) -> str:
        return str(move)

    def apply_move(self, move: int) -> None:
        self._state.sticks -= move
        self._state.last_player = self._current

    def check_result(self) -> GameResult | None:
        if self._state.sticks > 0:
            return None
        if self._state.last_player is self._human:
            return GameResult.COMPUTER_WIN
        return GameResult.HUMAN_WIN


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs) -> 'Game':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, value: str, draw: Draw) -> None:
        if not self.initialized:
            self.value = value
            self.initialized = True
            self.draw = draw
            self._current_game = None
            self.human = HumanPlayer('X', self.draw)
            self.computer = ComputerPlayer('O', self.draw)

    def _play_round(self) -> None:
        game = self._current_game
        draw = self.draw

        game.reset()
        draw.output(game.render())

        while game.check_result() is None:
            move = game.current_player.choice_move(game)
            game.apply_move(move)
            game.switch_player()
            draw.output("")
            draw.output(game.render())

        draw.output(game.result_message(game.check_result()))

    def run_game(self) -> None:
        draw = self.draw
        while True:
            if self._current_game is None:
                self._select_game()
            if self._current_game is None:
                return

            self._play_round()

            again = draw.input("\nВернуться в меню? (y/n): ").strip().lower()
            if again not in ("y", "д", "yes", ""):
                draw.output("До свидания!")
                break

            self._current_game = None

    def _select_game(self) -> None:
        draw = self.draw
        while True:
            draw.output('\n ==== Меню игры ====')
            draw.output('1. Крестики-нолики')
            draw.output('2. 21 палочка')
            draw.output('0. Выйти')
            choice = MenuChoice.from_input(draw.input('Выберите игру: ').strip())
            if choice == MenuChoice.TIC_TAC_TOE:
                draw.output('\n ---- Креститки-нолики ----')
                draw.output('Вы - X, компьютер - O')
                self._current_game = TicTacToe(self.human, self.computer)
                return None
            if choice == MenuChoice.STICK_21:
                draw.output('\n ---- 21 палочка ----')
                draw.output(
                    'За ход можно забрать 1, 2 или 3. '
                    'Проигрывает тот, кто взял последнюю.'
                )
                self._current_game = Stick21(self.human, self.computer)
                return None

            if choice == MenuChoice.EXIT:
                self._current_game = None
                return None

            draw.output('Неверный выбор')


if __name__ == '__main__':
    Game("Первая игра", ConsoleDraw()).run_game()
