"""
D. Остовное дерево 2

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Требуется найти в связном графе остовное дерево минимального веса.

Входные данные
Первая строка входного файла содержит два натуральных числа 𝑛 и 𝑚 — количество вершин и ребер графа соответственно.
Следующие 𝑚 строк содержат описание ребер по одному на строке.
Ребро номер 𝑖 описывается тремя натуральными числами 𝑏𝑖, 𝑒𝑖 и 𝑤𝑖 — номера концов ребра
и его вес соответственно (1≤𝑏𝑖,𝑒𝑖≤𝑛, 0≤𝑤𝑖≤100000). 𝑛≤200000,𝑚≤200000.

Граф является связным.

Выходные данные
Первая строка выходного файла должна содержать одно натуральное число — вес минимального остовного дерева.

Пример
входные данные
4 4
1 2 1
2 3 2
3 4 5
4 1 4
выходные данные
7

Напишем Краскала, чтобы потренировать его, плюс это же очень просто
"""
import sys


class DSU:
    def __init__(self, n):
        self.parents = [i for i in range(n)]
        self.sizes = [1 for _ in range(n)]

    def get_parent(self, el):
        if self.parents[el] != el:
            self.parents[el] = self.get_parent(self.parents[el])
        return self.parents[el]

    def union(self, el_1, el_2):
        el_1 = self.get_parent(el_1)
        el_2 = self.get_parent(el_2)
        if el_1 != el_2:
            if self.sizes[el_1] < self.sizes[el_2]:
                el_1, el_2 = el_2, el_1
            self.parents[el_2] = el_1
            self.sizes[el_1] += self.sizes[el_2]


class Edge:
    def __init__(self, a, b, w):
        self.start = a
        self.end = b
        self.weight = w


class Graph:
    def __init__(self, n):
        self.size = n
        self.edges = set()
        self.path = 0

    def add_edge(self, a, b, w):
        self.edges.add(Edge(a, b, w))

    def kruskal(self):
        self.edges = sorted(self.edges, key=lambda edge: edge.weight)
        dsu = DSU(self.size)
        for edge in self.edges:
            start_parent = dsu.get_parent(edge.start)
            end_parent = dsu.get_parent(edge.end)
            if start_parent != end_parent:
                self.path += edge.weight
                dsu.union(start_parent, end_parent)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    graph = Graph(n)
    for row in data[1:]:
        u, v, w = map(int, row.split())
        graph.add_edge(u - 1, v - 1, w)
    graph.kruskal()
    print(graph.path)


if __name__ == "__main__":
    main()
