"""
A. Сумма простая

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Вам нужно научиться отвечать на запрос «сумма чисел на отрезке».

Массив не меняется. Запросов много. Отвечать на каждый запрос следует за O(1).

Входные данные
Размер массива — n и числа x, y, a_0, порождающие массив a: a_i=(x⋅a_{i−1}+y)mod2^16
Далее следует количество запросов m и числа z, t, b_0, порождающие массив b: b_i=(z⋅b_{i−1}+t)mod2^30.

Массив c строится следующим образом: c_i=b_i mod n.

Запросы: i-й из них — найти сумму на отрезке от min(c_{2i},c_{2i+1}) до max(c_{2i},c_{2i+1}) в массиве a.

Ограничения: 1≤n≤10^7, 0≤m≤10^7. Все числа целые от 0 до 2^16. t может быть равно −1.

Выходные данные
Выведите сумму всех сумм.

Пример
входные данные
3 1 2 3
3 1 -1 4
выходные данные
23

Примечание
𝑎={3,5,7},𝑏={4,3,2,1,0,230−1},𝑐={1,0,2,1,0,0},
запросы = {[0,1],[1,2],[0,0]}, суммы = {8,12,3}.

Префиксные суммы, как на лекции
"""
MOD_1 = (1 << 16)
MOD_2 = (1 << 30)


def simple_sum_solution(n, x, y, a0, m, z, t, b0):
    if m == 0:
        return 0

    a = [0] * n
    a_sum = [0] * n
    a[0] = a0
    a_sum[0] = a0
    for i in range(1, n):
        a[i] = (x * a[i - 1] + y) % MOD_1
        a_sum[i] = a_sum[i - 1] + a[i]

    b = [0] * 2 * m
    c = [0] * 2 * m
    b[0] = b0
    c[0] = b0 % n
    for j in range(1, 2 * m):
        b[j] = (z * b[j - 1] + t) % MOD_2
        c[j] = b[j] % n

    common_sum = 0
    for query_num in range(m):
        left = min(c[2 * query_num], c[2 * query_num + 1])
        right = max(c[2 * query_num], c[2 * query_num + 1])
        if left == 0:
            query_sum = a_sum[right]
        else:
            query_sum = a_sum[right] - a_sum[left - 1]
        common_sum += query_sum

    return common_sum


def main():
    n, x, y, a0 = map(int, input().split())
    m, z, t, b0 = map(int, input().split())
    print(simple_sum_solution(n, x, y, a0, m, z, t, b0))


if __name__ == "__main__":
    main()
