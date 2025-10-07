# ВЕРТОЛЁТ
from utils import randcell# добавляем метод randcell для генерации начального положения вертолета 

class Helicopter: # назначаем класс 
    def __init__(self, w, h): # добавляем инициализатор
        
        rc = randcell(w, h)
        rx, ry = rc[1], rc[0]
        self.h = h
        self.w = w
        self.x = rx
        self.y = ry
        
        

    def move(self, dx, dy):
        nx, ny = dx + self.x, dy + self.y      
        if (nx >= 0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x, self.y = nx, ny