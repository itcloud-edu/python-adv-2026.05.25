import json
from time import sleep


# class Counter:
#     created = 0
#     def __init__(self, label: str) -> None:
#         self.label = label
#         Counter.created += 1
        

# a = Counter('A')
# b = Counter('B')
# print(Counter.created)
# print(a.created)

# a.created2 = 10
# print(a.created2)
# print(Counter.created)
# print(b.created)




# class Base:
#     def __init__(self, label: str) -> None:
#         self.label = label


# def createRectangle (x: float, y: float) -> "Base":
#     rect = Base('rect1')
#     rect.x = x
#     rect.y = y
#     return rect

# def createCircle (x: float, y: float) -> "Base":
#     circle = Base('circle1')
#     circle.x = x
#     circle.y = y
#     return circle


# r = createRectangle(10, 20)
# c = createCircle(30, 40)
# print(isinstance(r, Base), isinstance(c, Base))

class Task:
    items = []
    def __init__(self, title: str, completed: bool = False) -> None:
        self.id = id(self)
        self.__title = title
        self._completed = completed
        Task.items.append(self)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        title = title.strip()
        if not title or self.__title == title:
            return None
        
        # ядро функции
        print('Заголовок изменился')
        self.__title = title
         
    
    @property
    def completed(self) -> bool:
        return self._completed
    
    @completed.setter
    def completed(self, completed: bool) -> "Task":
        self._completed = completed
        


    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self._completed
        }
    @classmethod
    def from_dict(cls, data) -> "Task":
        tmp = cls(data['title'])
        tmp.id = data['id']
        tmp._completed = data['completed']
        return tmp
    
    @classmethod
    def  is_instance(cls, data) -> bool:
        return isinstance(data, cls)

    @staticmethod
    def static_from_dict(data) -> "Task":
        tmp = Task(data['title'])
        tmp.id = data['id']
        tmp._completed = data['completed']
        return tmp
    
    def __str__(self) -> str:
        return '{' + f'"id": {self.id}, "title": {self.__title}, "completed": {self._completed}' + '}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        print('Удаление объекта')





class TaskList:
    def __init__(self, title: str) -> None:
        self.items = list()
        self.id = id(self)
        self.title = title

    def add(self, task: Task) -> 'TaskList':
        print('Добавление: ', task)
        self.items.append(task)
        return self

    def delete(self, task_id) -> 'TaskList':
        removed_task = None
        for task in self.items:
            if task.id == task_id:
                removed_task = task
                self.items.remove(task)
                break
        if removed_task:
            print('Удаление: ', removed_task)
        else:
            print('Удаление: Задача с таким id не найдена')
        return self

    def __str__(self) -> str:
        """Возвращает красивое строковое представление списка задач."""
        # ANSI escape codes
        RESET = '\033[0m'
        BOLD = '\033[1m'
        BLUE = '\033[34m'
        GREEN = '\033[32m'
        RED = '\033[31m'
        YELLOW = '\033[33m'
        CYAN = '\033[36m'
        GRAY = '\033[90m'
        
        header = f'{BOLD}{BLUE}Список задач: "{self.title}" (ID: {self.id}){RESET}'
        if not self.items:
            return header + f'\n{GRAY}Задачи отсутствуют.{RESET}'
        
        tasks_lines = []
        for i, task in enumerate(self.items, 1):
            if task._completed:
                status = f'{GREEN}✓{RESET}'
            else:
                status = f'{RED}✗{RESET}'
            tasks_lines.append(f'  {YELLOW}{i}.{RESET} [{status}] {task._Task__title} {GRAY}(ID: {task.id}){RESET}')
        
        tasks_block = '\n'.join(tasks_lines)
        return f'{header}\n{CYAN}Задачи:{RESET}\n{tasks_block}'


tasks = TaskList('Список задач')
task1 = Task('Задача 1')
task2 = Task('Задача 2')
tasks.add(task1)
tasks.add(task2)

task1.title = 'Задача 1111'
task1.completed = True
print(tasks)
print(task1.title)

