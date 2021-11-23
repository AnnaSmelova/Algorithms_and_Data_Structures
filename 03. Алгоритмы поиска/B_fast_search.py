"""
B. Быстрый поиск в массиве

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан массив из 𝑛 целых чисел. Все числа от −10^9 до 10^9.
Нужно уметь отвечать на запросы вида «Cколько чисел имеют значения от 𝑙 до 𝑟»?

Входные данные
Число 𝑛 (1≤𝑛≤10^5). Далее 𝑛 целых чисел.
Затем число запросов 𝑘 (1≤𝑘≤10^5).
Далее 𝑘 пар чисел 𝑙,𝑟 (−10^9≤𝑙≤𝑟≤10^9) — собственно запросы.
Выходные данные
Выведите 𝑘 чисел — ответы на запросы.

Пример
входные данные
5
10 1 10 3 4
4
1 10
2 9
3 4
2 2
выходные данные
5 2 2 0
"""
import sys


def lower_bound(a: list, n: int, x: int) -> int:
    left_index = -1
    right_index = n
    while left_index < right_index - 1:
        m = (left_index + right_index) // 2
        if x <= a[m]:
            right_index = m
        else:
            left_index = m

    return right_index


def fast_search(a: list, n: int, x_min: int, x_max: int) -> int:
    x_min_lb = lower_bound(a, n, x_min)
    x_max_ub = lower_bound(a, n, x_max + 1)

    return x_max_ub - x_min_lb


def main():
    n = int(sys.stdin.readline())
    a = sorted(list(map(int, sys.stdin.readline().split())))
    k = int(sys.stdin.readline())
    for _ in range(k):
        l, r = map(int, sys.stdin.readline().split())
        print(fast_search(a, n, l, r), end=' ')


if __name__ == "__main__":
    main()
