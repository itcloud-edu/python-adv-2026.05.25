class Currency:
    label = 'CUR'

    def __init__(self, count: int)-> None:
        self.count = count

    def __add__(self, other) -> int | float:
        if not isinstance(other, Currency):
            return NotImplemented
        return (self.count + other.count)
    
    def __sub__(self, other) -> int | float:
        if not isinstance(other, Currency):
            return NotImplemented
        return (self.count - other.count)

    def __mul__(self, other) -> int | float:
        if not isinstance(other, int or float):
            return NotImplemented
        return (self.count * other)
    
    def __truediv__(self, other) -> int | float:
        if not isinstance(other, int or float):
            return NotImplemented
        return (self.count / other)
    
    def __str__(self) -> str:
        return f'{self.count} {self.label}'



class Kopeck(Currency):
    label = 'KOP'
    @classmethod
    def form_ruble(cls, ruble: Ruble) -> 'Kopeck':
        return cls(ruble.count * 100)


    def __add__(self, other) -> 'Kopeck':
        if isinstance(other, Ruble):
            other = Kopeck.form_ruble(other)
        return Kopeck(super().__add__(other))
    
    def __sub__(self, other) -> 'Kopeck':
        if isinstance(other, Ruble):
            other = Kopeck.form_ruble(other)
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
        if isinstance(other, Kopeck):
            other = Ruble.form_kopeck(other)
        return Ruble(super().__add__(other))
    
    def __sub__(self, other) -> 'Ruble':
        if isinstance(other, Kopeck):
            other = Ruble.form_kopeck(other)
        return Ruble(super().__sub__(other))
    
    def __mul__(self, other) -> 'Ruble':
        return Ruble(super().__mul__(other))
    
    def __truediv__(self, other) -> 'Ruble':
        return Ruble(super().__truediv__(other))

    

class Dolar(Currency):
    label = 'DOL'
    
    def __add__(self, other) -> 'Dolar':
        return Dolar(super().__add__(other))
    
    def __sub__(self, other) -> 'Dolar':
        return Dolar(super().__sub__(other))
    
    def __mul__(self, other) -> 'Dolar':
        return Dolar(super().__mul__(other))
    
    def __truediv__(self, other) -> 'Dolar':
        return Dolar(super().__truediv__(other))      

