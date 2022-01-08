"""
E. Периметр выпуклой оболочки

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дано N точек на плоскости.
Нужно вычислить периметр выпуклой оболочки данных точек.
Гарантируется, что выпуклая оболочка не вырождена.

Входные данные
В первой строке число N (3≤N≤10^5).
Следующие N строк содержат пары целых чисел x и y (-10^9≤x,y≤10^9) — точки.
Будьте аккуратны! Точки произвольны. Бывают совпадающие, бывают лежащие на одной прямой в большом количестве.

Выходные данные
Одно вещественное число — периметр выпуклой оболочки. Выводите число с максимально возможной точностью.

Пример
входные данные
5
0 0
2 0
0 2
1 1
2 2
выходные данные
8

Любым, из рассмотренных, методом строите выпуклую оболочку, а перемиметр искать легко
"""
import sys
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, start, end):
        self.x = end.x - start.x
        self.y = end.y - start.y

    def get_lng(self):
        lng = self.x ** 2 + self.y ** 2
        return math.sqrt(lng)

    def cross_product(self, other_vector):
        return self.x * other_vector.y - self.y * other_vector.x


class Polygon:
    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.size = len(vertexes)
        self.perimeter = 0

    def get_perimeter(self):
        vertexes = self.vertexes + [self.vertexes[0]]
        self.perimeter = 0
        for i in range(self.size):
            point_1 = vertexes[i]
            point_2 = vertexes[i + 1]
            vector = Vector(point_1, point_2)
            self.perimeter += vector.get_lng()
        return self.perimeter


class SetOfPoints:
    def __init__(self):
        self.points = []
        self.size = 0
        self.points_dict = {}

    def filter_points(self, point):
        point_ys = self.points_dict.get(point.x, [])
        if point.y in point_ys:
            return False
        point_ys.append(point.y)
        self.points_dict[point.x] = point_ys
        return True

    def add_point(self, x, y):
        point = Point(x, y)
        if self.filter_points(point):
            self.points.append(point)
            self.size += 1

    @staticmethod
    def sort_points(points, desc=False):
        if not desc:
            points = sorted(points, key=lambda p: p.y)
            points = sorted(points, key=lambda p: p.x)
        else:
            points = sorted(points, key=lambda p: p.y, reverse=True)
            points = sorted(points, key=lambda p: p.x, reverse=True)
        return points

    def build_convex_hull(self):
        point_a = self.points[0]
        point_b = self.points[-1]
        upper_set = [point_a, point_b]
        lower_set = [point_a, point_b]

        vector_ab = Vector(point_a, point_b)
        for i in range(1, self.size - 1):
            vector_ai = Vector(point_a, self.points[i])
            if vector_ab.cross_product(vector_ai) >= 0:
                upper_set.append(self.points[i])
            else:
                lower_set.append(self.points[i])

        upper_part = self.build_part_hull(upper_set)
        lower_part = self.build_part_hull(lower_set, desc=True)
        convex_hull_points = upper_part + lower_part[1: -1]
        return convex_hull_points

    def build_part_hull(self, points, desc=False):
        points = self.sort_points(points, desc=desc)
        stack = [points[0]]
        for i in range(1, len(points)):
            right_turn = False
            point_2 = points[i]
            while not right_turn:
                if len(stack) == 1:
                    stack.append(point_2)
                    right_turn = True
                else:
                    point_0 = stack[-2]
                    point_1 = stack[-1]
                    vector_01 = Vector(point_0, point_1)
                    vector_12 = Vector(point_1, point_2)
                    if vector_01.cross_product(vector_12) <= 0:
                        stack.append(point_2)
                        right_turn = True
                    else:
                        del stack[-1]
        return stack


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    points = SetOfPoints()
    for i in range(1, n + 1):
        x, y = map(int, data[i].split())
        points.add_point(x, y)
    points.points = points.sort_points(points.points)
    convex_hull_points = points.build_convex_hull()
    polygon = Polygon(convex_hull_points)
    print(polygon.get_perimeter())


if __name__ == "__main__":
    main()
