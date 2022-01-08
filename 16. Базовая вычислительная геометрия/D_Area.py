"""
D. Площадь многоугольника

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Входные данные
В первой строке одно число N ({3≤N≤100000}).
Далее в N строках по паре чисел –— координаты очередной вершины простого многоугольника
в порядке обхода по или против часовой стрелки.

Все координаты — целые числа, по модулю не превосходящие 10^4.

Выходные данные
Одно число —– величина площади приведённого многоугольника.

Пример
входные данные
3
1 0
0 1
1 1
выходные данные
0.5

Через ориентированную площадь треугольников
"""
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, start, end):
        self.x = end.x - start.x
        self.y = end.y - start.y

    def cross_product(self, other_vector):
        return self.x * other_vector.y - self.y * other_vector.x


class Polygon:
    def __init__(self):
        self.vertexes = []
        self.size = 0
        self.area = 0

    def add_vertex(self, x, y):
        point = Point(x, y)
        self.vertexes.append(point)
        self.size += 1

    def get_area(self):
        point_0 = self.vertexes[0]
        for i in range(1, self.size - 1):
            point_1 = self.vertexes[i]
            point_2 = self.vertexes[i + 1]
            a = Vector(point_0, point_1)
            b = Vector(point_0, point_2)
            cp = a.cross_product(b)
            self.area += cp
        self.area = abs(self.area) / 2
        return self.area


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    polygon = Polygon()
    for i in range(1, n + 1):
        x, y = map(int, data[i].split())
        polygon.add_vertex(x, y)
    print(polygon.get_area())


if __name__ == "__main__":
    main()
