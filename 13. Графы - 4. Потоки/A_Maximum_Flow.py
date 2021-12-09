"""
A. Очень простой поток

ограничение по времени на тест: 5 секунд
ограничение по памяти на тест: 1024 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Дан неориентированный граф, состоящий из N вершин и M ребер.

У каждого ребра которого есть маленькая пропускная способность.
Между любой парой вершин может быть больше одного ребра.

Исток находится в вершине 1, а сток в вершине N. Требуется найти максимальный поток между истоком и стоком.

Входные данные
В первой строке записано натуральное число N — число вершин (2≤N≤100).
Во второй строке записано натуральное число M — число ребер (1≤M≤5000).

Далее в M строках идет описание ребер.
Каждое ребро задается тройкой целых чисел Ai, Bi, Ci, где Ai, Bi — номера вершин, которые соединяет ребро (),
а Ci (0≤Ci≤20) — пропускная способность этого ребра.

Выходные данные
Выведите максимальный поток между вершинами с номерами 1 и N.

Примеры
входные данные
2
2
1 2 1
2 1 3
выходные данные
4

Тренируемся писать поток, можно Фордом-Фалкерсоном и даже без масштабирования
"""
import sys
from collections import defaultdict


START_VERTEX = 0
INF = float('inf')


class Edge:
    def __init__(self, a, b, c):
        self.start = a
        self.end = b
        self.capacity = c
        self.flow = 0
        self.back_edge = None

    def set_back_edge(self, back_edge):
        self.back_edge = back_edge


class Graph:
    def __init__(self, n):
        self.size = n
        self.edges = defaultdict(list)
        self.max_flow = 0
        self.start_vertex = START_VERTEX
        self.target_vertex = n - 1
        self.used = [0 for _ in range(n)]

    def add_edge(self, a, b, c):
        edge = Edge(a, b, c)
        back_edge = Edge(b, a, c)

        back_edge.set_back_edge(edge)
        edge.set_back_edge(back_edge)

        self.edges[a].append(edge)
        self.edges[b].append(back_edge)

    def push_flow(self, v, current_flow):
        self.used[v] = 1
        if self.target_vertex == v:
            return current_flow
        for edge in self.edges[v]:
            if not self.used[edge.end] and edge.flow < edge.capacity:
                next_flow = min(current_flow, edge.capacity - edge.flow)
                delta = self.push_flow(edge.end, next_flow)
                if delta > 0:
                    edge.flow += delta
                    edge.back_edge.flow -= delta
                    return delta
        return 0

    def ford_fulkerson(self):
        while True:
            self.used = [0 for _ in range(self.size)]
            delta = self.push_flow(self.start_vertex, INF)
            if delta > 0:
                self.max_flow += delta
            else:
                return self.max_flow


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    m = int(data[1])
    graph = Graph(n)
    for row in data[2:]:
        a, b, c = map(int, row.split())
        graph.add_edge(a - 1, b - 1, c)
    print(graph.ford_fulkerson())


if __name__ == "__main__":
    main()
