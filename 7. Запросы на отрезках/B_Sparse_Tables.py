"""
B. Разреженные таблицы

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан массив из 𝑛 чисел.
Требуется написать программу, которая будет отвечать на запросы следующего вида:
найти минимум на отрезке между u и v включительно.

Входные данные
В первой строке заданы три натуральных числа n, m (1⩽n⩽10^5, 1⩽m⩽10^7) и a_1 (0⩽a_1<16714589) —
количество элементов в массиве, количество запросов и первый элемент массива соответственно.
Вторая строка содержит два натуральных числа u_1 и v_1 (1⩽u_1,v_1⩽n) — первый запрос.

Для того, чтобы размер ввода был небольшой, массив и запросы генерируются.

Элементы a_2,a_3,…,a_n задаются следующей формулой:
a_{i+1}=(23⋅a_i+21563)mod16714589.
Например, при n=10, a_1=12345 получается следующий массив:
a = (12345, 305498, 7048017, 11694653, 1565158, 2591019, 9471233, 570265, 13137658, 1325095).

Запросы генерируются следующим образом:

u_{i+1}=((17⋅u_i+751+r_i+2i)mod n)+1, v_{i+1}=((13⋅v_i+593+r_i+5i)mod n)+1,
где r_i — ответ на запрос номер i.
Обратите внимание, что u_i может быть больше, чем v_i.

Выходные данные
В выходной файл выведите u_m, v_m и r_m (последний запрос и ответ на него).

Пример
входные данные
10 8 12345
3 9
выходные данные
5 3 1565158

Примечание
Можно заметить, что массивы 𝑢, 𝑣 и 𝑟 можно не сохранять в памяти полностью.

Эта задача скорее всего не решается стандартными интерпретаторами Python 2 и Python 3.
Используйте соответствующие компиляторы PyPy.
"""
MOD = 16714589
CONST_A1 = 23
CONST_A2 = 21563
CONST_U1 = 17
CONST_U2 = 751
CONST_U3 = 2
CONST_V1 = 13
CONST_V2 = 593
CONST_V3 = 5
INF = float('inf')


def get_k_power_of_two(k):
    return 1 << k


def get_next_a(prev_a):
    return (CONST_A1 * prev_a + CONST_A2) % MOD


def get_next_u(prev_u, prev_res, query_num, n):
    return ((CONST_U1 * prev_u + CONST_U2 + prev_res + CONST_U3 * query_num) % n) + 1


def get_next_v(prev_v, prev_res, query_num, n):
    return ((CONST_V1 * prev_v + CONST_V2 + prev_res + CONST_V3 * query_num) % n) + 1


def get_array_of_k(n):
    k = [None] * (n + 1)
    k[1] = 0
    for i in range(2, n + 1):
        k[i] = k[i - 1]
        if get_k_power_of_two(k[i] + 1) <= i:
            k[i] += 1
    return k


def sparse_tables_solution(n, m, a1, u, v):
    array_of_k = get_array_of_k(n)

    a = [0] * n
    dp = [[INF] * (array_of_k[n] + 1) for _ in range(n)]
    a[0] = a1
    dp[0][0] = a1
    for i in range(1, n):
        a[i] = get_next_a(a[i - 1])
        dp[i][0] = a[i]

    for j in range(1, array_of_k[n] + 1):
        for i in range(n):
            if (i + get_k_power_of_two(j - 1)) < n:
                dp[i][j] = min(dp[i][j - 1], dp[i + get_k_power_of_two(j - 1)][j - 1])

    for q in range(1, m + 1):
        left, right = min(u, v), max(u, v)
        k = array_of_k[right - left + 1]
        res = min(dp[left - 1][k], dp[right - get_k_power_of_two(k)][k])
        if q != m:
            u = get_next_u(u, res, q, n)
            v = get_next_v(v, res, q, n)

    return str(u), str(v), str(res)


def main():
    n, m, a1 = map(int, input().split())
    u1, v1 = map(int, input().split())
    print(' '.join(sparse_tables_solution(n, m, a1, u1, v1)))


if __name__ == "__main__":
    main()
