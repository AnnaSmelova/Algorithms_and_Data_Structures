"""
C. Цифровая сортировка

ограничение по времени на тест: 3 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дано 𝑛 строк, выведите их порядок после 𝑘 фаз цифровой сортировки.
В этой задаче требуется реализовать цифровую сортировку.

Входные данные
В первой строке входного файла содержится число 𝑛 — количество строк, 𝑚 — их длина и
𝑘 – число фаз цифровой сортировки (1≤𝑛≤1000, 1≤𝑘≤𝑚≤1000).
В следующих 𝑛 строках находятся сами строки.
Выходные данные
Выведите строки в порядке в котором они будут после 𝑘 фаз цифровой сортировки.

Пример 1
входные данные
3 3 1
bbb
aba
baa
выходные данные
aba
baa
bbb

Пример 2
входные данные
3 3 2
bbb
aba
baa
выходные данные
baa
aba
bbb

Пример 3
входные данные
3 3 3
bbb
aba
baa
выходные данные
aba
baa
bbb
"""
FIRST_LETTER = ord('a')
LAST_LETTER = ord('z')
CNT_ARRAY_LEN = LAST_LETTER - FIRST_LETTER + 1


def count_sort(a: list, n: int, digit: int) -> list:
    """Сортировка подсчетом

    :param a: list - массив, который надо отсортировать
    :param n: int - длина массива a
    :param digit: int - разряд с конца, по которому сортируем
    :return: list - массив, отсортированный по разряду digit в порядке неубывания
    """
    cnt_a = [0] * CNT_ARRAY_LEN
    for el in a:
        cnt_a[ord(el[-digit]) - FIRST_LETTER] += 1

    pos_a = [0]
    for k in range(1, CNT_ARRAY_LEN):
        pos_a.append(pos_a[k - 1] + cnt_a[k - 1])

    res_a = [''] * n
    for el in a:
        j = ord(el[-digit]) - FIRST_LETTER
        res_a[pos_a[j]] = el
        pos_a[j] += 1

    return res_a


def radix_sort(a: list, n: int, k: int) -> list:
    """Цифровая сортировка

    :param a: list - массив, который надо отсортировать
    :param n: int - длина массива a
    :param k: int - число фаз цифровой сортировки
    :return: list - массив, отсортированный за k фаз в порядке неубывания
    """
    for i in range(1, k + 1):
        a = count_sort(a, n, i)

    return a


def main():
    a = []
    n, m, k = map(int, input().split())
    for _ in range(n):
        a.append(input())
    a_sorted = radix_sort(a, n, k)
    for el in a_sorted:
        print(el)


if __name__ == "__main__":
    main()
