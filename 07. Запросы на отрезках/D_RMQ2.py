"""
D. RMQ2

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Входные данные
В первой строке находится число n — размер массива. (1≤𝑛≤10^5)
Во второй строке находится n чисел a_i — элементы массива.
Далее содержится описание операций, их количество не превышает 2⋅10^5.
В каждой строке находится одна из следующих операций:
* set i j x — установить все a[k], i≤k≤j в x.
* add i j x — увеличить все a[k], i≤k≤j на x.
* min i j — вывести значение минимального элемента в массиве на отрезке с i по j, гарантируется, что (1≤i≤j≤n).
Все числа во входном файле и результаты выполнения всех операций не превышают по модулю 10^18.

Выходные данные
Выведите последовательно результат выполнения всех операций min.
Следуйте формату выходного файла из примера.

Пример
входные данные
5
1 2 3 4 5
min 2 5
min 1 5
min 1 4
min 2 4
set 1 3 10
add 2 4 4
min 2 5
min 1 5
min 1 4
min 2 4
выходные данные
2
1
1
2
5
5
8
8

Тут уже придется написать дерево отрезков, еще и с групповыми операциями,
еще и нетривиальными, надо подумать, как именно эти операции "стакаются"
"""
import sys

UNICODE = "utf-8"
INF = float('inf')


class SegmentTree:
    def __init__(self, array, n):
        self.full_array_size = self.get_k_power_of_two(self.get_k(n)) - 1
        self.tree_size = self.get_k_power_of_two(self.get_k(n) + 1) - 1
        self.tree = [INF] * self.tree_size
        self.build_tree(array, n)

        self.adds = [0] * self.tree_size
        self.sets = [None] * self.tree_size

    def build_tree(self, a, n):
        x = 1
        while x < n:
            x *= 2
        for i in range(n):
            self.tree[i + x - 1] = a[i]
        for v in range(x - 2, -1, -1):
            self.tree[v] = min(self.tree[2 * v + 1], self.tree[2 * v + 2])

    @staticmethod
    def get_k_power_of_two(k):
        return 1 << k

    def get_k(self, n):
        k = 0
        while self.get_k_power_of_two(k) < n:
            k += 1
        return k

    def set(self, v, left, right, a, b, x):
        self.push(v, left, right)
        if left > b or right < a:
            return
        if left >= a and right <= b:
            self.sets[v] = x
            return
        m = (left + right) // 2
        self.set(2 * v + 1, left, m, a, b, x)
        self.set(2 * v + 2, m + 1, right, a, b, x)
        self.tree[v] = min(self.get_node_value(2 * v + 1), self.get_node_value(2 * v + 2))

    def add(self, v, left, right, a, b, x):
        self.push(v, left, right)
        if left > b or right < a:
            return
        if left >= a and right <= b:
            self.adds[v] += x
            return
        m = (left + right) // 2
        self.add(2 * v + 1, left, m, a, b, x)
        self.add(2 * v + 2, m + 1, right, a, b, x)
        self.tree[v] = min(self.get_node_value(2 * v + 1), self.get_node_value(2 * v + 2))

    def rmq(self, v, left, right, a, b):
        self.push(v, left, right)
        if left > b or right < a:
            return INF
        if left >= a and right <= b:
            return self.tree[v]
        m = (left + right) // 2
        return min(self.rmq(2 * v + 1, left, m, a, b), self.rmq(2 * v + 2, m + 1, right, a, b))

    def get_node_value(self, v):
        if self.sets[v] is not None:
            return self.sets[v] + self.adds[v]
        else:
            return self.tree[v] + self.adds[v]

    def push(self, v, left, right):
        if left == right:
            if self.sets[v] is not None:
                self.tree[v] = self.sets[v] + self.adds[v]
                self.sets[v] = None
                self.adds[v] = 0
            else:
                self.tree[v] += self.adds[v]
                self.adds[v] = 0
        else:
            if self.sets[v] is not None:
                self.sets[2 * v + 1] = self.sets[v]
                self.sets[2 * v + 2] = self.sets[v]
                self.adds[2 * v + 1] = self.adds[v]
                self.adds[2 * v + 2] = self.adds[v]
            else:
                self.adds[2 * v + 1] += self.adds[v]
                self.adds[2 * v + 2] += self.adds[v]

            self.tree[v] = min(self.get_node_value(2 * v + 1), self.get_node_value(2 * v + 2))
            self.adds[v] = 0
            self.sets[v] = None


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    a = list(map(int, data[1].split()))
    tree = SegmentTree(a, n)
    for operation in data[2:]:
        args = operation.decode(UNICODE).split()
        if args[0] == 'set':
            tree.set(0, 0, tree.full_array_size, int(args[1]) - 1, int(args[2]) - 1, int(args[3]))
        elif args[0] == 'add':
            tree.add(0, 0, tree.full_array_size, int(args[1]) - 1, int(args[2]) - 1, int(args[3]))
        else:
            print(tree.rmq(0, 0, tree.full_array_size, int(args[1]) - 1, int(args[2]) - 1))


if __name__ == "__main__":
    main()

'''
n = 5
a = [1, 2, 3, 4, 5]
tree = SegmentTree(a, n)
print(tree.rmq(0, 0, tree.full_array_size, 1, 4))
print(tree.rmq(0, 0, tree.full_array_size, 0, 4))
print(tree.rmq(0, 0, tree.full_array_size, 0, 3))
print(tree.rmq(0, 0, tree.full_array_size, 1, 3))
tree.set(0, 0, tree.full_array_size, 0, 2, 10)
tree.add(0, 0, tree.full_array_size, 1, 3, 4)
print(tree.rmq(0, 0, tree.full_array_size, 1, 4))
print(tree.rmq(0, 0, tree.full_array_size, 0, 4))
print(tree.rmq(0, 0, tree.full_array_size, 0, 3))
print(tree.rmq(0, 0, tree.full_array_size, 1, 3))

'''


