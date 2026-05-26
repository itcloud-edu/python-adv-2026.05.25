class Task:
    def __init__(self, title: str, completed: bool = False) -> None:
        self.id = id(self)
        self.title = title
        self.completed = completed
    
    def set_completed(self) -> "Task":
        self.completed = True
        return self

    def set_title(self, title: str) -> "Task":
        title = title.strip()
        if not title or self.title == title:
            return self
        
        # ядро функции
        print('Заголовок изменился')
        self.title = title
        return self
    
    def __str__(self) -> str:
        return '{' + f'"id": {self.id}, "title": {self.title}, "completed": {self.completed}' + '}'

    def __repr__(self) -> str:
        return self.__str__()
