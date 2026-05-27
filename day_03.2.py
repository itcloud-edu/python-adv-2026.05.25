from abc import ABC, abstractmethod


class Currency(ABC):
    label = 'CUR'
    convertion_rate: float = 0

    def __init__(self, count: int)-> None:
        self.count = count

    @abstractmethod
    def convert_to(self, carrency_type: type) -> 'Currency':
        pass

    def __add__(self, other) -> 'Currency':
        if not isinstance(other, Currency):
            return NotImplemented
        other = other.convert_to(self.__class__)
        return self.__class__(self.count + other.count)
    
    def __sub__(self, other) -> int | float:
        if not isinstance(other, Currency):
            return NotImplemented
        other = other.convert_to(self.__class__)
        return self.__class__(self.count - other.count)
    
    def __mul__(self, other) -> int | float:
        if not isinstance(other, int | float):
            return NotImplemented
        return self.__class__(self.count * other)

    def __truediv__(self, other) -> int | float:
        if not isinstance(other, int | float):
            return NotImplemented
        return self.__class__(self.count / other)
    
    def __str__(self) -> str:
        return f'{self.count} {self.label}'



class Kopeck(Currency):
    label = 'KOP'
    convertion_rate: float = 0.01
    
    def convert_to(self, carrency_type: type) -> 'Ruble':
        if carrency_type is Kopeck:
            return self
        if carrency_type is Dolar:
            return Dolar(self.count * self.convertion_rate / Dolar.convertion_rate )
        if carrency_type is Ruble:
            return Ruble(self.count * self.convertion_rate)


class Ruble(Currency):
    label = 'RUB'
    convertion_rate: float = 1

    def convert_to(self, carrency_type: type) -> 'Ruble':
        if carrency_type is Kopeck:
            return Kopeck(self.count / Kopeck.convertion_rate)
        if carrency_type is Dolar:
            return Dolar(self.count / Dolar.convertion_rate)
        if carrency_type is Ruble:
            return self
            

class Dolar(Currency):
    label = 'DOL'
    convertion_rate: float = 71.15
    def convert_to(self, carrency_type: type) -> 'Ruble':
        if carrency_type is Kopeck:
            return Kopeck(self.count * self.convertion_rate * Kopeck.convertion_rate)
        if carrency_type is Dolar:
            return self
        if carrency_type is Ruble:
            return Ruble(self.count * self.convertion_rate)
    
    
    



r = Ruble(100)
d = Dolar(100)

print(r - d)
print(d - r)
print(Kopeck(100) + Ruble(10) * 3)