from abc import ABC, abstractmethod

# def singleton(cls):
#     instances = {} ## ???

#     def wrapper(*args, **kwargs):
#         print(instances)
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]

#     return wrapper



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
            self.draw.output(self.value)
            self.draw.output(self.draw.input("Привет!!!! Как у тебя дела?"))

# Abstract class ??
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



if __name__ == '__main__':
    game1 = Game("Первая игра", ConsoleDraw())
    game2 = Game('Вторая игра', DisplayDraw())
    print(game1.value)
    print(game2.value)
    print(game1 is game2)
 