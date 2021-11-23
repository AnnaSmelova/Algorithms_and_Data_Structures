"""
E. RMQ наоборот

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: rmq.in
вывод: rmq.out

Рассмотрим массив a[1..n]. Пусть Q(i,j) — ответ на запрос о нахождении минимума среди чисел a[i],...,a[j].
Вам даны несколько запросов и ответы на них. Восстановите исходный массив.

Входные данные
Первая строка входного файла содержит число n — размер массива, и m — число запросов (1≤n,m≤100000).
Следующие m строк содержат по три целых числа i, j и q, означающих, что Q(i,j)=q (1≤i≤j≤n, -2^31≤q≤2^31-1).

Выходные данные
Если искомого массива не существует, выведите строку «inconsistent».

В противном случае в первую строку выходного файла выведите «consistent».
Во вторую строку выходного файла выведите элементы массива.
Элементами массива должны быть целые числа в интервале от -2^31 до 2^31-1 включительно.
Если решений несколько, выведите любое.

Пример 1
входные данные
3 2
1 2 1
2 3 2
выходные данные
consistent
1 2 2

Пример 2
входные данные
3 3
1 2 1
1 1 2
2 3 2
выходные данные
inconsistent

Ну это чисто дичь какая-то для тех, кому первых четырех не хватило для веселья:)
"""
INF = float('inf')
MAX_VAL = ((1 << 31) - 1)


class SegmentTree:
    def __init__(self, n):
        self.full_array_size = self.get_k_power_of_two(self.get_k(n)) - 1
        self.tree_size = self.get_k_power_of_two(self.get_k(n) + 1) - 1
        self.tree = [INF] * self.tree_size

    @staticmethod
    def get_k_power_of_two(k):
        return 1 << k

    def get_k(self, n):
        k = 0
        while self.get_k_power_of_two(k) < n:
            k += 1
        return k

    def set(self, v, left, right, a, b, x):
        if left > b or right < a:
            return
        if a <= left and right <= b:
            if self.tree[v] != INF:
                self.tree[v] = max(x, self.tree[v])
            else:
                self.tree[v] = x
            return
        if self.tree[v] != INF and self.tree[v] >= x:
            return
        m = (left + right) // 2
        self.set(2 * v + 1, left, m, a, b, x)
        self.set(2 * v + 2, m + 1, right, a, b, x)
        if self.tree[2 * v + 1] != INF and self.tree[2 * v + 2] != INF:
            if self.tree[v] == INF:
                self.tree[v] = min(self.tree[2 * v + 1], self.tree[2 * v + 2])
            else:
                self.tree[v] = max(self.tree[v], min(self.tree[2 * v + 1], self.tree[2 * v + 2]))

    def check_query(self, v, left, right, a, b, q):
        if left > b or right < a:
            return False
        if left >= a and right <= b:
            return self.tree[v] == q
        if self.tree[v] != INF and self.tree[v] > q:
            return False
        m = (left + right) // 2
        return self.check_query(2 * v + 1, left, m, a, b, q) or self.check_query(2 * v + 2, m + 1, right, a, b, q)

    def push(self):
        h = self.tree_size - self.full_array_size - 1
        for i in range(h):
            if self.tree[i] != INF:
                if self.tree[2 * i + 1] == INF:
                    self.tree[2 * i + 1] = self.tree[i]
                else:
                    self.tree[2 * i + 1] = max(self.tree[2 * i + 1], self.tree[i])
                if self.tree[2 * i + 2] == INF:
                    self.tree[2 * i + 2] = self.tree[i]
                else:
                    self.tree[2 * i + 2] = max(self.tree[2 * i + 2], self.tree[i])
        self.array = self.tree[h:]


def main():
    in_file = open('rmq.in', 'r')
    out_file = open('rmq.out', 'w')

    data = in_file.read().splitlines()
    n, m = map(int, data[0].split())

    tree = SegmentTree(n)
    for query in range(1, m + 1):
        i, j, q = map(int, data[query].split())
        tree.set(0, 0, tree.full_array_size, i - 1, j - 1, q)
    tree.push()

    inconsistent = False
    for query in range(1, m + 1):
        i, j, q = map(int, data[query].split())
        result = tree.check_query(0, 0, tree.full_array_size, i - 1, j - 1, q)
        if not result:
            inconsistent = True
            break
    if inconsistent:
        out_file.write('inconsistent')
    else:
        out_file.write('consistent\n')

        h = tree.tree_size - tree.full_array_size - 1
        full_array = tree.tree[h:]
        array = [MAX_VAL if x == INF else x for x in full_array[:n]]
        array = map(str, array)
        out_file.write(' '.join(array))

    in_file.close()
    out_file.close()


if __name__ == "__main__":
    main()
