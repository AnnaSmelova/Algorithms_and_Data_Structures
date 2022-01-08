"""
Требования к выполнению домашнего задания:
Структуры данных для вектора и точки должны быть реализованы через принципы ООП
Все операции: методы

A. Принадлежность точки отрезку

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Входные данные
Шесть чисел — координаты точки и координаты концов отрезка.

Выходные данные
Одна строка YES, если точка принадлежит отрезку, и NO в противном случае.

Пример 1
входные данные
3 3 1 2 5 4
выходные данные
YES

Пример 2
входные данные
4 2 4 2 4 5
выходные данные
YES

Учимся писать классы и пользоваться произведениями
"""
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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


def main():
    coordinates = sys.stdin.buffer.read().splitlines()
    p_x, p_y, a_x, a_y, b_x, b_y = map(int, coordinates[0].split())

    point_p = Point(p_x, p_y)
    point_a = Point(a_x, a_y)
    point_b = Point(b_x, b_y)
    vector_ab = Vector(point_a, point_b)

    if vector_ab.check_point(point_p):
        print("YES")
    else:
        print("NO")


if __name__ == "__main__":
    main()
