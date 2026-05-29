"""
Учебный проект: консольные настольные игры «человек против компьютера».

Это закомментированная копия game_base.py — логика та же, добавлены пояснения.
Запуск: python game_base_commented.py

Архитектура (три слоя + фасад):

1. Draw      — ввод/вывод (консоль сегодня, GUI завтра)
2. Player    — кто делает ход (человек или компьютер)
3. BoardGame — правила конкретной игры (крестики, 21 палочка)
4. Game      — меню, цикл партии, Singleton

Подробнее: lectures/01_base.md
"""

from abc import ABC, abstractmethod
import random


# =============================================================================
# Слой отображения (Draw) — Strategy / Adapter для ввода-вывода
# =============================================================================

class Draw(ABC):
    """
    Абстрактный интерфейс ввода-вывода.

    Игра не вызывает print()/input() напрямую — только draw.output() и draw.input().
    Так можно подменить ConsoleDraw на DisplayDraw (окно) без переписывания правил.
    """

    @abstractmethod
    def input(self, value: str) -> None:
        """Показать подсказку и получить строку от пользователя."""

    @abstractmethod
    def output(self, value: str) -> None:
        """Вывести текст (поле, ошибки, результат)."""


class ConsoleDraw(Draw):
    """Реализация для терминала: input() и print()."""

    def input(self, value: str) -> None:
        return input(value)

    def output(self, value: str) -> None:
        print(value)


class DisplayDraw(Draw):
    """
    Заглушка для будущего графического интерфейса.
    Методы пустые — достаточно подставить этот класс в Game вместо ConsoleDraw.
    """

    def input(self, value: str) -> None:
        pass

    def output(self, value: str) -> None:
        pass


# =============================================================================
# Слой игроков (Player) — кто и как выбирает ход
# =============================================================================

class Player(ABC):
    """
    Абстрактный игрок: имя + ссылка на Draw.
    Не хранит состояние доски — только умеет получить ход через game.valid_moves() и т.д.
    """

    def __init__(self, name: str, draw: Draw) -> None:
        self.name = name
        self.draw = draw

    @abstractmethod
    def choice_move(self, game: BoardGame, draw: Draw):
        """Вернуть один ход в формате, который понимает game.apply_move()."""


class HumanPlayer(Player):
    """
    Живой игрок: цикл ввода до корректного хода.
    1) подсказка move_prompt → 2) parse_move → 3) проверка valid_moves
    """

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
    """ИИ: случайный допустимый ход. format_move() — как показать ход пользователю."""

    def choice_move(self, game: BoardGame):
        draw = self.draw
        move = random.choice(game.valid_moves())
        draw.output(f"Компьютер выбирает {game.format_move(move)}")
        return move


# =============================================================================
# Слой игровой логики (BoardGame) — Template Method для любой настольной игры
# =============================================================================

class BoardGame(ABC):
    """
    Абстрактная «доска»: human, computer, очередь хода (_current).
    TicTacToe и Stick21 реализуют правила в абстрактных методах ниже.

    Цикл одного хода (в Game._play_round):
        reset → render → [choice_move → apply_move → switch_player] → check_result
    """

    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        self._human = human
        self._computer = computer
        self._current: Player = human  # первым ходит человек

    @property
    def human(self) -> HumanPlayer:
        return self._human

    @property
    def computer(self) -> ComputerPlayer:
        return self._computer

    @property
    def current_player(self) -> Player:
        """Кто ходит сейчас — используется в цикле партии."""
        return self._current

    @abstractmethod
    def reset(self) -> None:
        """Новая партия: очистить поле, ход человека."""

    @abstractmethod
    def render(self) -> str:
        """Текстовое представление состояния для консоли."""

    @abstractmethod
    def valid_moves(self, value: str) -> list[int]:
        """Список допустимых ходов (формат зависит от игры)."""

    @abstractmethod
    def move_prompt(self) -> str:
        """Подсказка перед вводом хода человека."""

    @abstractmethod
    def parse_move(self, value: str) -> int:
        """Строка → ход; ValueError при ошибке."""

    @abstractmethod
    def apply_move(self, value: str) -> None:
        """Применить ход текущего игрока."""

    @abstractmethod
    def check_result(self) -> bool:
        """
        None — игра продолжается;
        "human_win" | "computer_win" | "draw" — код для result_message().
        """

    def result_message(self, code) -> str:
        """Перевод кода результата в фразу на русском."""
        messages = {
            "human_win": "Вы победили",
            "computer_win": "Вы проиграли",
            "draw": "Ничья"
        }
        return messages[code]

    def switch_player(self) -> None:
        """Передать ход другому игроку."""
        self._current = self._human if self._current == self._computer else self._computer

    def format_move(self, move: int) -> str:
        return str(move)


# =============================================================================
# Игра 1: Крестики-нолики (3×3)
# =============================================================================

class TicTacToe(BoardGame):
    """
    Поле 3×3, индексы клеток 0–8.
    '.' — пусто; человек X, компьютер O.
    Победа — три в ряд (строка, столбец, диагональ).
    """

    # Восемь выигрышных линий (индексы клеток, 0 — левый верхний угол)
    _WIN_LIST = (
        (0, 1, 2),  # верхняя строка
        (3, 4, 5),  # средняя
        (6, 7, 8),  # нижняя
        (0, 3, 6),  # левый столбец
        (1, 4, 7),  # средний
        (2, 5, 8),  # правый
        (0, 4, 8),  # главная диагональ
        (2, 4, 6)   # побочная диагональ
    )

    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        super().__init__(human, computer)
        self._board: list[str] = []
        self._marks: dict[Player, str] = {}  # какой символ у какого игрока

    def reset(self) -> None:
        self._board = ['.'] * 9
        self._marks = {self._human: 'X', self._computer: 'O'}
        self._current = self._human

    def render(self) -> str:
        # Пустые клетки — номера 1–9, занятые — X или O
        cells = []
        for i, cell in enumerate(self._board):
            if cell == '.':
                cells.append(str(i + 1))
            else:
                cells.append(cell)
        rows = [
            " | ".join(cells[0:3]),
            " | ".join(cells[3:6]),
            " | ".join(cells[6:9])
        ]
        return "\n".join(rows)

    def valid_moves(self) -> list[int]:
        return [i for i, cell in enumerate(self._board) if cell == '.']

    def move_prompt(self) -> str:
        nums = ', '.join([str(i + 1) for i in self.valid_moves()])
        mark = self._marks[self._current]
        return f"Ваш ход ({mark}). Клетки [{nums}]: "

    def parse_move(self, raw: str) -> int:
        value = int(raw) - 1  # пользователь вводит 1–9, внутри 0–8
        if value not in self.valid_moves():
            raise ValueError("Неверный ход")
        return value

    def apply_move(self, value: int) -> None:
        mark = self._marks[self._current]
        self._board[value] = mark

    def _winner_mark(self) -> str:
        """Символ победителя ('X'/'O') или None."""
        for a, b, c in self._WIN_LIST:
            if self._board[a] != '.' and self._board[a] == self._board[b] == self._board[c]:
                return self._board[a]
        return None

    def check_result(self) -> bool:
        winner = self._winner_mark()
        if winner:
            human_mark = self._marks[self._human]
            return "human_win" if winner == human_mark else "computer_win"
        if '.' not in self._board:
            return "draw"
        return None
    
    def format_move(self, move: int) -> str:
        """
        Как показать ход в сообщении (по умолчанию +1 для клеток 1–9).
        Stick21 переопределяет: там ход уже 1, 2 или 3.
        """
        return str(move + 1)


# =============================================================================
# Игра 2: «21 палочка» (misère Nim)
# =============================================================================

class Stick21(BoardGame):
    """
    21 палочка: за ход берут 1–3, проигрывает тот, кто забрал последнюю.
    _last_player нужен, чтобы при sticks == 0 знать, кто проиграл.
    """

    _INITIAL_STICKS = 21
    _MAX_TAKE = 3

    def __init__(self, human: HumanPlayer, computer: ComputerPlayer) -> None:
        super().__init__(human, computer)
        self._sticks = self._INITIAL_STICKS
        self._last_player: Player | None = None

    def reset(self) -> None:
        self._sticks = self._INITIAL_STICKS
        self._last_player = None
        self._current = self._human

    def render(self) -> str:
        bar = "|" * self._sticks if self._sticks else "(пусто)"
        return f"Палочек: {self._sticks}\n{bar}"

    def valid_moves(self) -> list[int]:
        # 1, 2, 3 — но не больше остатка
        return [n for n in range(1, self._MAX_TAKE + 1) if n <= self._sticks]

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
        return str(move)  # ход уже 1–3, без +1

    def apply_move(self, move: int) -> None:
        self._sticks -= move
        self._last_player = self._current

    def check_result(self) -> str | None:
        if self._sticks > 0:
            return None
        # Кто взял последнюю — проиграл
        if self._last_player is self._human:
            return "computer_win"
        return "human_win"


# =============================================================================
# Фасад приложения: меню, цикл партий, Singleton
# =============================================================================

class Game:
    """
    Связывает Draw, игроков и выбранную BoardGame.

    Singleton (__new__): повторный Game(...) возвращает тот же объект.
    initialized — чтобы __init__ не сбрасывал настройки при втором вызове.
    """

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
            self._current_game: BoardGame = None
            self.human = HumanPlayer('X', self.draw)
            self.computer = ComputerPlayer('O', self.draw)

    def _play_round(self) -> None:
        """Одна партия: reset → цикл ходов → сообщение о результате."""
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
        """Главный цикл: меню → партия → «Вернуться в меню?»."""
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
        """Меню: 1 — крестики, 2 — палочки, 0 — выход."""
        draw = self.draw
        while True:
            draw.output('\n ==== Меню игры ====')
            draw.output('1. Крестики-нолики')
            draw.output('2. 21 палочка')
            draw.output('0. Выйти')
            choice = draw.input('Выберите игру: ')
            if choice == '1':
                draw.output('\n ---- Креститки-нолики ----')
                draw.output('Вы - X, компьютер - O')
                self._current_game = TicTacToe(self.human, self.computer)
                return None
            if choice == '2':
                draw.output('\n ---- 21 палочка ----')
                draw.output(
                    'За ход можно забрать 1, 2 или 3. '
                    'Проигрывает тот, кто взял последнюю.'
                )
                self._current_game = Stick21(self.human, self.computer)
                return None

            if choice == '0':
                self._current_game = None
                return None

            draw.output('Неверный выбор')


if __name__ == '__main__':
    Game("Первая игра", ConsoleDraw()).run_game()
