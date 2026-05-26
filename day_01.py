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

    


task1 = Task('Задача 1')


print(task1.title, task1.completed)

task1.set_completed().set_title('Задача 1')


print(task1.title, task1.completed)

