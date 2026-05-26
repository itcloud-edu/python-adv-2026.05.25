x = 1
y = 'Привет!'
z = 1.3
z = False
n = None

l = [1,2,3,4]
t = (1,2,3,4)
d = {'x': 1, 'y': 2}
s = {1,2,3,4}

a = 0 
print(int(a), bool(a) , str(a), float(a), list(str(a)), tuple(str(a)), dict([['a', a]]), set([a]))

if a == 0:
    print('a is 0')
elif a == 1:
    pass
else:
    print('a is not 0') 


for i in range(10):
    result = i * 2
    print(result)


i = 10
while True:
    print(i)
    i -=1
    if not i:
        break


match a:
    case 0:
        print('a is 0')
    case 1:
        pass
    case _:
        print('a is not 0')


def sum(a, b):
    return a + b

print(sum(100,2))

sum2 = lambda a, b: a + b

print(sum2(100,4))


calc_dict = {
    'data':[],
    'sum': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a / b
}
print('---- dict ----')
print(calc_dict['sum'](100,2))
print(calc_dict['sub'](100,2))
print(calc_dict['mul'](100,2))
print(calc_dict['div'](100,2))

class Calc:
    __data = []
    def sum(a, b):
        Calc.__data.append(a + b)
        return a + b
    def sub(a, b):
        Calc.__data.append(a - b)
        return a - b
    def mul(a, b):
        Calc.__data.append(a * b)
        return a * b
    def div(a, b):
        Calc.__data.append(a / b)
        return a / b
    def get_data():
        return Calc.__data

print('---- class ----')

Calc.sum(100,2)
calc_dict['sum'](100,2)


Calc.sub(100,2)
Calc.mul(100,2)
Calc.div(100,2)

print(Calc.get_data())



__file = None
def open(file):
    global __file
    __file = open(file, 'r')
def read():
    global __file
    return __file.read()
def write(data):
    global __file
    __file.write(data)
    __file.close()
def close():
    global __file
    __file.close()


