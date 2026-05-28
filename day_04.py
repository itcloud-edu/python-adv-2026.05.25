class Game:
    _instance = None

    def __new__(cls, *args, **kwargs) -> 'Game':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, value: str) -> None:
        if not self.initialized:
            self.value = value
            self.initialized = True


if __name__ == '__main__':
    game1 = Game('Первая игра')
    game2 = Game('Вторая игра')
    print(game1.value)
    print(game2.value)
    print(game1 is game2)