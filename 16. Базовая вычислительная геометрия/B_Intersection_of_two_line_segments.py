"""
B. Пересечение двух отрезков

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Необходимо проверить, пересекаются ли два отрезка.

Входные данные
В двух строках входного файла заданы по четыре целых числа, не превосходящих по модулю 10000,
— координаты концов первого отрезка, затем второго.

Выходные данные
В первой строке выходного файла выведите «YES», если отрезки имеют общие точки, и «NO» в противном случае.

Пример
входные данные
5 1 2 6
1 1 7 8
выходные данные
YES

Если в этой задаче вы используете уравнение прямой, то что-то пошло не так
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
    a_x, a_y, b_x, b_y = map(int, coordinates[0].split())
    c_x, c_y, d_x, d_y = map(int, coordinates[1].split())

    point_a = Point(a_x, a_y)
    point_b = Point(b_x, b_y)
    point_c = Point(c_x, c_y)
    point_d = Point(d_x, d_y)

    vector_ab = Vector(point_a, point_b)
    vector_ac = Vector(point_a, point_c)
    vector_ad = Vector(point_a, point_d)
    vector_ca = Vector(point_c, point_a)
    vector_cb = Vector(point_c, point_b)
    vector_cd = Vector(point_c, point_d)

    if vector_ab.cross_product(vector_ac) == 0 and vector_ab.cross_product(vector_ad) == 0 and \
            vector_cd.cross_product(vector_ca) == 0 and vector_cd.cross_product(vector_cb) == 0:
        if vector_ab.check_point(point_c) or vector_ab.check_point(point_d):
            print("YES")
        else:
            print("NO")
    elif vector_ab.cross_product(vector_ac) * vector_ab.cross_product(vector_ad) <= 0 and \
            vector_cd.cross_product(vector_ca) * vector_cd.cross_product(vector_cb) <= 0:
        print("YES")
    else:
        print("NO")


if __name__ == "__main__":
    main()
