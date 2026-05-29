from dataclasses import dataclass, field

class TicTacToeState1:
    def __init__(self) -> None:
        self.board = []
        self.current_player = None


@dataclass
class TicTacToeState:
    board : list[str] = field(default_factory= list)

print(TicTacToeState1().board) 
print(TicTacToeState().board) 