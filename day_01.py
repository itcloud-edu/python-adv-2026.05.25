class Info:
    __version = '1.0'
    __author = 'John Doe'

    def get_info():
        print(f'Version: {Info.__version}')
        print(f'Author: {Info.__author}')


Info.get_info()

# def info():
#     VERSION = '1.0'
#     AUTHOR = 'John Doe'
#     def get_info():
#         nonlocal VERSION
#         nonlocal AUTHOR
#         print(f'Version: {VERSION}')
#         print(f'Author: {AUTHOR}')
#     return get_info


# get_info = info()
# get_info()


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


task1 = Task('Задача 1')
print(task1.title)


task_dict = {"id": 3423, "title": "Задача 1", "completed": False}
print(task_dict["title"])

def set_title_dict(task_dict: dict, title: str) -> None:
        title = title.strip()
        if not title or task_dict["title"] == title:
            return None
        
        # ядро функции
        print('Заголовок изменился')
        task_dict["title"] = title
    
set_title_dict(task_dict, "Задача 2")


print(task_dict)
print(task1)
print(repr(task1))


