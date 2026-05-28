def init_matrix(m=5):
    matrix = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(None)
        matrix.append(row)
    return matrix    

def step(matrix, a, b, player):
    # Проверка на выход за границы

    matrix[a-1][b-1] = player
    return matrix

a, b = map(int, input("Введите два числа через запятую: ").split(','))

matrix = init_matrix()
matrix = step(matrix, a, b, 'X')
print(matrix)

'''
| 1  | 2  | 3  |  4  | 5 |
---------------------
| 6  | 7  | 8  | 9  |  10  |
--------------------
|   |   |   |   |   |
---------------------
|   |   |   |  9;9 |   |


'''