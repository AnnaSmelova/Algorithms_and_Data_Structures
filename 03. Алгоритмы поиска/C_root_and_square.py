"""
C. Квадратный корень и квадратный квадрат

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Найдите такое число x, что x**2+sqrt(x)=C, с точностью не менее 6 знаков после точки.

Входные данные
В единственной строке содержится вещественное число 1.0≤C≤10^10.
Выходные данные
Выведите одно число — искомый x.

Пример 1
входные данные
2.0000000000
выходные данные
1.0

Пример 2
входные данные
18.0000000000
выходные данные
4.0
"""
import sys
from math import ceil, log2


EPS = 10**(-6)
MAX_X = (10**10)**0.5
MIN_X = 0
ITN = ceil(log2((MAX_X - MIN_X) / EPS))


def get_func(x: float) -> float:
    return x**2 + x**0.5


def bin_search(c: float) -> float:
    left_val = MIN_X
    right_val = MAX_X
    for i in range(ITN):
        m = (left_val + right_val) / 2
        if get_func(m) < c:
            left_val = m
        else:
            right_val = m

    return right_val


def main():
    c = float(sys.stdin.readline())
    print(bin_search(c))


if __name__ == "__main__":
    main()
