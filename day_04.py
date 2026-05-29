from abc import ABC, abstractmethod
import random

class Draw(ABC):
    @abstractmethod
    def input(self, value: str) -> None:
        pass

    @abstractmethod
    def output(self, value: str) -> None:
        pass
    


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
            return move


class ComputerPlayer(Player):
    def choice_move(self, game: BoardGame):
        draw = self.draw
        move = random.choice(game.valid_moves())
        draw.output(f"Компьютер выбирает {move + 1}")
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
    def render (self) -> str:
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
    def check_result(self)  -> bool:
        pass

    def result_message(self, code) -> str:
        messages = {
            "human_win": "Вы победили",
            "computer_win": "Вы проиграли",
            "draw": "Ничья"
        }
        return messages[code] 
    
    def switch_player(self) -> None:
        self._current = self._human if self._current == self._computer else self._computer
        

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
        self._board: list[str] = []
        self._marks: dict[Player, str] = {}

    def reset(self) -> None:
        self._board = ['.'] * 9
        self._marks = {self._human: 'X', self._computer: 'O'}
        self._current = self._human

    def render(self) -> str:
        cells = []
        for i, cell in enumerate(self._board):
            if  cell == '.':
                cells.append(str(i+1))
            else:
                cells.append(cell)
        rows =[
            " | ".join(cells[0:3]),
            " | ".join(cells[3:6]),
            " | ".join(cells[6:9])
        ]
        return "\n".join(rows)
    
    def valid_moves(self) -> list[int]:
        moves = []
        for i, cell in enumerate(self._board):
            if cell == '.':
                moves.append(i)
        return moves
    
    def move_prompt(self) -> str:
        nums = ', '.join([str(i+1) for i in self.valid_moves()])
        mark = self._marks[self._current]
        return f"Ваш ход ({mark}). Клетки [{nums}]: "
    
    def parse_move(self, raw: str) -> int:
        value = int(raw)-1
        if value not in self.valid_moves():
            raise ValueError("Неверный ход")
        return value
    
    def apply_move(self, value: int) -> None:
        mark = self._marks[self._current]
        self._board[value] = mark

    def _winner_mark(self) -> str:
        for a,b,c in self._WIN_LIST:
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
    
class Stick21(BoardGame):
    pass


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



    def run_game(self) -> None:
        if self._current_game is None:
            self._select_game()
        
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

        result = game.check_result()
        draw.output(game.result_message(result))

    
    def _select_game(self) -> None:
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
                continue

            if choice == '0':
                return None

            draw.output('Неверный выбор')






if __name__ == '__main__':
    Game("Первая игра", ConsoleDraw()).run_game()
    

