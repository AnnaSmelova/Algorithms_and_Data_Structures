"""
C. Точка в многоугольнике

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

В первой строке содержится три числа —– 𝑁 (3⩽𝑁⩽100000) и координаты точки.
Последующие 𝑁 строк содержат координаты углов многоугольника. Координаты — целые, не превосходят 10^6 по модулю.

Входные данные
Одна строка YES, если заданная точка содержится в приведённом многоугольнике или на его границе,
и NO в противном случае.

Пример
входные данные
3 2 3
1 1
10 2
2 8
выходные данные
YES

Можно лучом, можно через полярные углы, как упражнение полезнее луч
"""
import sys
from math import atan2


EPS = 10 ** (-6)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Vector:
    def __init__(self, start, end):
        self.start_point = start
        self.end_point = end
        self.x = end.x - start.x
        self.y = end.y - start.y

    def dot_product(self, other_vector):
        return self.x * other_vector.x + self.y * other_vector.y

    def cross_product(self, other_vector):
        return self.x * other_vector.y - self.y * other_vector.x

    def get_reverse(self):
        return Vector(self.end_point, self.start_point)

    def check_point(self, point):
        point_on_line = (self.cross_product(Vector(self.start_point, point)) == 0)
        start_dot_point = self.dot_product(Vector(self.start_point, point))
        end_dot_point = self.get_reverse().dot_product(Vector(self.end_point, point))
        if point_on_line and start_dot_point >= 0 and end_dot_point >= 0:
            return True
        else:
            return False

    def get_angle(self, other_vector):
        return atan2(self.cross_product(other_vector), self.dot_product(other_vector))


class Polygon:
    def __init__(self):
        self.vertexes = []
        self.segments = []
        self.last_point = None
        self.size = 0

    def add_segment_and_check_point_on_border(self, next_point, check_point):
        if self.last_point is not None:
            segment = Vector(self.last_point, next_point)
            if segment.check_point(check_point):
                return True
            self.segments.append(segment)
            self.last_point = next_point
        else:
            self.last_point = next_point
        return False

    def add_vertex_and_check_point_on_border(self, x, y, check_point):
        point = Point(x, y)
        if check_point == point:
            return True
        self.vertexes.append(point)
        self.size += 1
        return self.add_segment_and_check_point_on_border(point, check_point)

    def check_point_inside(self, check_point):
        total_angle = 0
        for i in range(self.size):
            point_1 = self.vertexes[i]
            point_2 = self.vertexes[(i + 1) % self.size]
            vector_1 = Vector(check_point, point_1)
            vector_2 = Vector(check_point, point_2)
            angle = vector_1.get_angle(vector_2)
            total_angle += angle
        return abs(total_angle) > EPS


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, p_x, p_y = map(int, data[0].split())
    check_point = Point(p_x, p_y)
    polygon = Polygon()
    result = False
    for i in range(1, n + 1):
        x, y = map(int, data[i].split())
        result = polygon.add_vertex_and_check_point_on_border(x, y, check_point)
        if result:
            print("YES")
            break
    if not result:
        result = polygon.check_point_inside(check_point)
        if result:
            print("YES")
        else:
            print("NO")


if __name__ == "__main__":
    main()
