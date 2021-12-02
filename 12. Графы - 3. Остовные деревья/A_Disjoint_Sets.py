"""
A. Система непересекающихся множеств

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте систему непересекающихся множеств.
Вместе с каждым множеством храните минимальный, максимальный элемент в этом множестве и их количество.

Входные данные
Первая строка входного файла содержит n — количество элементов в носителе (1≤n≤300000).
Далее операций с множеством.
Операция get должна возвращать минимальный, максимальный элемент в соответствующем множестве, а также их количество.

Выходные данные
Выведите последовательно результат выполнения всех операций get.

Пример
входные данные
5
union 1 2
get 3
get 2
union 2 3
get 2
union 1 3
get 5
union 4 5
get 5
union 4 1
get 5
выходные данные
3 3 1
1 2 2
1 3 3
5 5 1
4 5 2
1 5 5

Тренируем СНМ, не забываем обе эвристики
"""
import sys


UNICODE = "utf-8"


class DSU:
    def __init__(self, n):
        self.parents = [i for i in range(n)]
        self.min_elements = [i for i in range(n)]
        self.max_elements = [i for i in range(n)]
        self.sizes = [1 for _ in range(n)]

    def get_parent(self, el):
        if self.parents[el] != el:
            self.parents[el] = self.get_parent(self.parents[el])
        return self.parents[el]

    def get_info(self, el):
        parent = self.get_parent(el)
        return self.min_elements[parent] + 1, self.max_elements[parent] + 1, self.sizes[parent]

    def update_max_and_min(self, el_1, el_2):
        self.min_elements[el_1] = min(self.min_elements[el_1], self.min_elements[el_2])
        self.max_elements[el_1] = max(self.max_elements[el_1], self.max_elements[el_2])

    def union(self, el_1, el_2):
        el_1 = self.get_parent(el_1)
        el_2 = self.get_parent(el_2)
        if el_1 != el_2:
            if self.sizes[el_1] < self.sizes[el_2]:
                el_1, el_2 = el_2, el_1
            self.parents[el_2] = el_1
            self.update_max_and_min(el_1, el_2)
            self.sizes[el_1] += self.sizes[el_2]


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    dsu = DSU(n)
    for row in data[1:]:
        args = row.decode(UNICODE).split()
        if args[0] == 'get':
            print(' '.join(map(str, dsu.get_info(int(args[1]) - 1))))
        elif args[0] == 'union':
            args[1], args[2] = int(args[1]) - 1, int(args[2]) - 1
            if args[1] != args[2]:
                dsu.union(args[1], args[2])


if __name__ == "__main__":
    main()
