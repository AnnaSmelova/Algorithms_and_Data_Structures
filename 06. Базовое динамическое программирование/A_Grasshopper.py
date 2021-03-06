"""
A. Кузнечик собирает монеты

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Кузнечик прыгает по столбикам, расположенным на одной линии на равных расстояниях друг от друга.
Столбики имеют порядковые номера от 1 до 𝑛.
В начале Кузнечик сидит на столбике с номером 1 и хочет добраться до столбика с номером 𝑛.
Он может прыгнуть вперед на расстояние от 1 до 𝑘 столбиков, считая от текущего.

На каждом столбике Кузнечик может получить или потерять несколько золотых монет
(для каждого столбика это число известно).
Определите, как нужно прыгать Кузнечику, чтобы собрать наибольшее количество золотых монет.
Учитывайте, что Кузнечик не может прыгать назад.

Входные данные
В первой строке вводятся два натуральных числа: 𝑛 и 𝑘 (3≤𝑛≤10000, 1≤𝑘≤10000), разделённые пробелом.
Во второй строке записаны через пробел 𝑛−2 целых числа – количество монет, которое Кузнечик получает на каждом столбике,
 от 2-го до 𝑛−1-го. Если это число отрицательное, Кузнечик теряет монеты.
 Гарантируется, что все числа по модулю не превосходят 10000.

Выходные данные
В первой строке программа должна вывести наибольшее количество монет, которое может собрать Кузнечик.
Во второй строке выводится число прыжков Кузнечика, а в третьей строке – номера всех столбиков,
которые посетил Кузнечик (через пробел в порядке возрастания).

Если правильных ответов несколько, выведите любой из них.

Пример 1
входные данные
5 3
2 -3 5
выходные данные
7
3
1 2 4 5

Пример 2
входные данные
10 3
-13 -2 -14 -124 -9 -6 -5 -7
выходные данные
-16
4
1 3 6 8 10

Пример 3
входные данные
12 5
-5 -4 -3 -2 -1 1 2 3 4 5
выходные данные
14
7
1 6 7 8 9 10 11 12
"""


def grasshopper_solution(n, k, costs):
    dp = [0] * (n + 1)
    pr = [0] * (n + 1)
    costs.append(0)
    for i in range(2, n + 1):
        max_cost = dp[i - 1]
        pr[i] = i - 1
        for j in range(2, min(i, k + 1)):
            if max_cost < dp[i - j]:
                max_cost = dp[i - j]
                pr[i] = i - j
        dp[i] = max_cost + costs[i - 2]
    steps = [str(n)]
    i = n
    while i > 1:
        steps.append(str(pr[i]))
        i = pr[i]
    return dp[n], len(steps) - 1, steps[::-1]


def main():
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))
    result = grasshopper_solution(n, k, costs)
    print(result[0])
    print(result[1])
    print(' '.join(result[2]))


if __name__ == "__main__":
    main()
