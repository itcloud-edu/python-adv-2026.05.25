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
        self.title = title
        self.completed = completed
        Task.items.append(self)
    
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
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }
    @classmethod
    def from_dict(cls, data) -> "Task":
        tmp = cls(data['title'])
        tmp.id = data['id']
        tmp.completed = data['completed']
        return tmp
    
    @classmethod
    def  is_instance(cls, data) -> bool:
        return isinstance(data, cls)

    @staticmethod
    def static_from_dict(data) -> "Task":
        tmp = Task(data['title'])
        tmp.id = data['id']
        tmp.completed = data['completed']
        return tmp
    
    def __str__(self) -> str:
        return '{' + f'"id": {self.id}, "title": {self.title}, "completed": {self.completed}' + '}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        print('Удаление объекта')




# task1 = Task('Задача 1')
# dict_task1 = task1.to_dict()
# print(dict_task1)

# # str_task1 = json.dumps(dict_task1)
# # print(str_task1)

# with open('task1.json', 'w') as f:
#     json.dump(dict_task1, f)


# with open('task1.json', 'r') as f:
#     dict_task1 = json.load(f)
#     print(dict_task1)
#     task1 = Task(dict_task1['title'])
#     print('task1', task1)
#     task2 = Task.static_from_dict(dict_task1)
#     # task2 = Task.from_dict(dict_task1)
#     print('task2', task2)

#     print(Task.is_instance(dict_task1))



Task('Задача 1')
Task('Задача 2')
Task('Задача 3')




sleep(5)

print(Task.items)
    