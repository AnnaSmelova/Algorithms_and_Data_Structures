"""
C. RSQ

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Входные данные
В первой строке находится число n — размер массива. (1≤n≤500000)
Во второй строке находится n чисел a_i — элементы массива.
Далее содержится описание операций, их количество не превышает 1000000.
В каждой строке находится одна из следующих операций:
* set i x — установить a[i] в x.
* sum i j — вывести значение суммы элементов в массиве на отрезке с i по j, гарантируется, что (1≤i≤j≤n).
Все числа во входном файле и результаты выполнения всех операций не превышают по модулю 10^18.

Выходные данные
Выведите последовательно результат выполнения всех операций sum.
Следуйте формату выходного файла из примера.

Пример
входные данные
5
1 2 3 4 5
sum 2 5
sum 1 5
sum 1 4
sum 2 4
set 1 10
set 2 3
set 5 2
sum 2 5
sum 1 5
sum 1 4
sum 2 4
выходные данные
14
15
10
9
12
22
20
10

Дерево Фенвика писать проще чем дерево отрезков, а тут еще и запросы простые
"""
import sys

UNICODE = "utf-8"


class BinaryIndexedTree:
    def __init__(self, array, n):
        self.array = array
        self.size = n
        self.T = []
        for i in range(n):
            current_sum = 0
            for j in range(self.get_f(i), i + 1):
                current_sum += self.array[j]
            self.T.append(current_sum)

    @staticmethod
    def get_f(i):
        return i & (i + 1)

    def get(self, i):
        res = 0
        while i >= 0:
            res += self.T[i]
            i = self.get_f(i) - 1
        return res

    def rsq(self, left, right):
        if left == 0:
            return self.get(right)
        return self.get(right) - self.get(left - 1)

    def add(self, i, x):
        j = i
        while j < self.size:
            self.T[j] += x
            j = j | (j + 1)

    def set(self, i, x):
        d = x - self.array[i]
        self.array[i] = x
        self.add(i, d)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    a = list(map(int, data[1].split()))
    fenwick = BinaryIndexedTree(a, n)
    for operation in data[2:]:
        args = operation.decode(UNICODE).split()
        if args[0] == 'sum':
            print(fenwick.rsq(int(args[1]) - 1, int(args[2]) - 1))
        else:
            fenwick.set(int(args[1]) - 1, int(args[2]))


if __name__ == "__main__":
    main()
