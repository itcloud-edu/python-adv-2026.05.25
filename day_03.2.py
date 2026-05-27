class Currency:
    label = 'CUR'

    def __init__(self, count: int)-> None:
        self.count = count

    def __add__(self, other) -> int | float:
        return (self.count + other.count)
    
    def __sub__(self, other) -> int | float:
        return (self.count - other.count)

    def __mul__(self, other) -> int | float:
        return (self.count * other)
    
    def __truediv__(self, other) -> int | float:
        return (self.count / other)
    
    def __str__(self) -> str:
        return f'{self.count} {self.label}'



class Kopeck(Currency):
    label = 'KOP'


    def __add__(self, other) -> 'Kopeck':
        return Kopeck(super().__add__(other))
    
    def __sub__(self, other) -> 'Kopeck':
        return Kopeck(super().__sub__(other))
    
    def __mul__(self, other) -> 'Kopeck':
        return Kopeck(super().__mul__(other))
        
    def __truediv__(self, other) -> 'Kopeck':
        return Kopeck(super().__truediv__(other))




class Ruble(Currency):
    label = 'RUB'
    @classmethod
    def form_kopeck(cls, kopeck: Kopeck) -> 'Ruble':
        return cls(kopeck.count / 100)
    
    def __add__(self, other) -> 'Ruble':
        return Ruble(super().__add__(other))
    
    def __sub__(self, other) -> 'Ruble':
        return Ruble(super().__sub__(other))
    
    def __mul__(self, other) -> 'Ruble':
        return Ruble(super().__mul__(other))
    
    def __truediv__(self, other) -> 'Ruble':
        return Ruble(super().__truediv__(other))

    

        

 

k1 = Kopeck(100) 

r1 = Ruble(100)
r2 = Ruble(200)
print(type(r2))


print(type(r1 + r2))