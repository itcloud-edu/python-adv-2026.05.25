messages = {
            "human_win": "Вы победили",
            "computer_win": "Вы проиграли",
            "draw": "Ничья"
        }

from enum import Enum

class GameResult(Enum):
    HUMAN_WIN = "human_win"
    COMPUTER_WIN = "computer_win"
    DRAW = "draw"

    def message(self) -> str:
        return {
            GameResult.HUMAN_WIN : "Вы победили", 
            GameResult.COMPUTER_WIN: "Компьютер победил"
        }[self]

print(GameResult('human_win'))


