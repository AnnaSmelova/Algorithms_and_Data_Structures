"""
A. Приближенный двоичный поиск

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Даны два массива. Первый массив отсортирован по неубыванию,
второй массив содержит запросы — целые числа.

Для каждого запроса выведите число из первого массива наиболее близкое (то есть с минимальным модулем разности)
к числу в этом запросе .
Если таких несколько, выведите меньшее из них.

Входные данные
В первой строке входных данных содержатся числа n и k (0<n,k≤10^5).
Во второй строке задаются n чисел первого массива, отсортированного по неубыванию,
а в третьей строке — k чисел второго массива.
Каждое число в обоих массивах по модулю не превосходит 2·10^9 .

Выходные данные
Для каждого из k чисел выведите в отдельную строку число из первого массива, наиболее близкое к данному.
Если таких несколько, выведите меньшее из них.

Пример
входные данные
5 5
1 3 5 7 9
2 4 8 1 6
выходные данные
1
3
7
1
5
"""
import sys


def upper_bound(a: list, n: int, x: int) -> int:
    left_index = 0
    right_index = n - 1

    while left_index < right_index - 1:
        m = (left_index + right_index) // 2
        if x < a[m]:
            right_index = m
        else:
            left_index = m

    return right_index


def approximate_binary_search(a: list, n: int, x: int) -> int:
    right_index = upper_bound(a, n, x)
    left_index = right_index - 1
    if left_index != -1 and abs(a[left_index] - x) <= abs(a[right_index] - x):
        return a[left_index]
    else:
        return a[right_index]


def main():
    n, k = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    q = list(map(int, sys.stdin.readline().split()))
    for i in range(k):
        print(approximate_binary_search(a, n, q[i]))


if __name__ == "__main__":
    main()
