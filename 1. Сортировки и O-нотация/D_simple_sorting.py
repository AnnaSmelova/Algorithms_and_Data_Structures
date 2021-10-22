"""
D. Простая сортировка

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 64 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Дан массив целых чисел. Ваша задача — отсортировать его в порядке неубывания.

Входные данные
В первой строке входного файла содержится число N (1≤N≤100000) — количество элементов в массиве.
Во второй строке находятся N целых чисел, по модулю не превосходящих 10^9.
Выходные данные
В выходной файл надо вывести этот же массив в порядке неубывания,
между любыми двумя числами должен стоять ровно один пробел.

Пример
входные данные
10
1 8 2 1 4 7 3 2 3 6
выходные данные
1 1 2 2 3 3 4 6 7 8

Примечание
Запрещается использовать стандартные сортировки.
"""
from random import randint
from math import floor


def partition_left(a: list, st: int, fin: int):
    """Разделение массива на две части, с большими и меньшими, чем выбранный, элементами. Проход слева.

    :param a: list - массив, который надо отсортировать
    :param st: int - начальный индекс массива
    :param fin: int - конечный индекс массива
    :return: tuple (list, int) - (массив, разделенный так, что a[0],...,a[p-1] < a[p] и a[p+1],...,a[n-1]>=a[p],
    индекс центрального элемента)
    """
    m = floor((st + fin) / 2)
    left_ind = st + floor((fin - st) / 3)
    right_ind = st + floor(2 * (fin - st) / 3)
    p = randint(left_ind, right_ind)  # центральный элемент
    a[p], a[fin] = a[fin], a[p]
    b = st
    has_two_parts = False
    for i in range(st, fin):
        if a[i] < a[fin]:
            has_two_parts = True
            a[i], a[b] = a[b], a[i]
            b += 1
        elif a[i] > a[fin]:
            has_two_parts = True
    if b == st and not has_two_parts:
        b = m
    a[fin], a[b] = a[b], a[fin]
    return a, b


def partition_right(a: list, st: int, fin: int):
    """Разделение массива на две части, с большими и меньшими, чем выбранный, элементами. Проход справа.

        :param a: list - массив, который надо отсортировать
        :param st: int - начальный индекс массива
        :param fin: int - конечный индекс массива
        :return: tuple (list, int) - (массив, разделенный так, что a[0],...,a[p-1] <= a[p] и a[p+1],...,a[n-1]>a[p],
        индекс центрального элемента)
        """
    m = floor((st + fin) / 2)
    left_ind = st + floor((fin - st) / 3)
    right_ind = st + floor(2 * (fin - st) / 3)
    p = randint(left_ind, right_ind)  # центральный элемент
    a[p], a[st] = a[st], a[p]
    b = fin
    has_two_parts = False
    for i in range(fin, st, -1):
        if a[i] > a[st]:
            has_two_parts = True
            a[i], a[b] = a[b], a[i]
            b -= 1
        elif a[i] < a[st]:
            has_two_parts = True
    if b == fin and not has_two_parts:
        b = m
    a[st], a[b] = a[b], a[st]
    return a, b


def quick_sort(a: list, st: int, fin: int, type='left') -> list:
    """Быстрая сортировка.

        :param a: list - массив, который надо отсортировать
        :param st: int - начальный индекс массива
        :param fin: int - конечный индекс массива
        :return: list - массив, отсортированный в порядке неубывания
        """
    if st < fin:
        if type == 'left':
            a, p = partition_left(a, st, fin)
        else:
            a, p = partition_right(a, st, fin)
        a = quick_sort(a, st, p - 1, 'left')
        a = quick_sort(a, p + 1, fin, 'right')
    return a


def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(' '.join(map(str, quick_sort(a, 0, len(a) - 1, 'left'))))


if __name__ == "__main__":
    main()
