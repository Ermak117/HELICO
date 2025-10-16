from utils import randbool  # импортируем метод
from utils import randcell
from utils import randcell2  # импортируем функцию randcell2

# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - апгрейдшоп
# 5 - огонь
CELL_TYPES = "🟩🌲🟦🏥🏨🔥"  # список иконок для отображения на карте
TREE_BONUS = 100
#TODO: change to 5000
UPGRADE_COST = 500

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        # храним клетки как [row=y][col=x]
        self.cells = [[0 for _ in range(w)] for _ in range(h)]
        self.generate_forest(3, 10)  # генерация леса на карте
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()

    def check_bounds(self, x, y):
        # x — по ширине (столбец), y — по высоте (строка)
        return 0 <= x < self.h and 0 <= y < self.w

    def print_map(self, helico):
        print('⬛️' * (self.w + 2))  # верхняя рамка
        for x in range(self.h):
            print('⬛️', end="")  # левая рамка
            for y in range(self.w):
                if helico.x == x and helico.y == y:
                    print('🚁', end="")
                else:
                    cell = self.cells[x][y]
                    if 0 <= cell < len(CELL_TYPES):
                        print(CELL_TYPES[cell], end="")
                    else:
                        print('?', end="")
            print('⬛️')  # правая рамка
        print('⬛️' * (self.w + 2))  # нижняя рамка

    def generate_river(self, length):
        # ожидается, что randcell(w, h) -> (x, y)
        x, y = randcell(self.h, self.w)
        self.cells[x][y] = 2  # [row=y][col=x]

        # Если хотите, чтобы длина считала только УДАЧНЫЕ шаги, инкрементируйте счётчик только при успехе.
        steps = 0
        while steps < length:
            nx, ny = randcell2(x, y)  # ожидается соседняя клетка (x, y)
            if self.check_bounds(nx, ny):
                self.cells[nx][ny] = 2
                x, y = nx, ny
                steps += 1
            else:
                # можно ничего не делать — шаг не засчитывается
                pass

    def generate_forest(self, r, mxr):
        # функция рандомного генерирования деревьев на карте
        for x in range(self.h):
            for y in range(self.w):
                if randbool(r, mxr):
                    self.cells[x][y] = 1

    def generate_tree(self):
        # механика восстановления лесов, выбираем рандомную клеточку на поле W x H
        cx, cy = randcell(self.h, self.w)
        if self.cells[cx][cy] == 0:  # проверяем что есть поле
            self.cells[cx][cy] = 1
    
    def generate_upgrade_shop(self): # механика апгрейд шопа
        c = randcell(self.h, self.w)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4

    def add_fire(self):
        # механика генерации огня
        cx, cy = randcell(self.h, self.w)
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self):
        # все горящие клетки сгорают до поля
        for y in range(self.w):
            for x in range(self.h):
                if self.cells[x][y] == 5:
                    self.cells[x][y] = 0
        # затем поджигаем новые
        for _ in range(10): # частота появления огня на карте
            self.add_fire()

    def process_helicopter(self, helico):
        c = self.cells[helico.x] [helico.y]
        if (c == 2):
            helico.tank = helico.mxtank
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if (c == 4 and helico.score >= UPGRADE_COST):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST