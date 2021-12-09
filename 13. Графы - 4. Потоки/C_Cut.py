"""
C. Разрез

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 1024 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Найдите минимальный разрез между вершинами 1 и 𝑛 в заданном неориентированном графе.

Входные данные
На первой строке входного файла содержится 𝑛 (2≤𝑛≤100) — число вершин в графе и 𝑚 (0≤𝑚≤400) — количество ребер.
На следующих 𝑚 строках входного файла содержится описание ребер.
Ребро описывается номерами вершин, которые оно соединяет,
и его пропускной способностью (положительное целое число, не превосходящее 10000000),
при этом никакие две вершины не соединяются более чем одним ребром.

Выходные данные
На первой строке выходного файла должны содержаться количество ребер в минимальном разрезе
и их суммарная пропускная способность.
На следующей строке выведите возрастающую последовательность номеров ребер
(ребра нумеруются в том порядке, в каком они были заданы во входном файле).

Примеры
входные данные
3 3
1 2 3
1 3 5
3 2 7
выходные данные
2 8
1 2

Умеем искать поток, умеем искать разрез
"""
import sys
from collections import defaultdict, deque


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
    def __init__(self, n, m):
        self.size = n
        self.edges_cnt = m
        self.edges = defaultdict(list)
        self.real_edges = []
        self.max_flow = 0
        self.start_vertex = START_VERTEX
        self.target_vertex = n - 1
        self.used = [0 for _ in range(n)]
        self.max_capacity = 0

    def add_edge(self, a, b, c):
        edge = Edge(a, b, c)
        back_edge = Edge(b, a, c)

        back_edge.set_back_edge(edge)
        edge.set_back_edge(back_edge)

        self.edges[a].append(edge)
        self.edges[b].append(back_edge)

        self.real_edges.append(edge)
        self.max_capacity = max(self.max_capacity, c)

    def bfs(self, v, delta):
        queue = deque([v])
        current_flow = INF
        while queue:
            current_v = queue.popleft()
            for edge in self.edges[current_v]:
                if not self.used[edge.end] and edge.flow < edge.capacity and delta <= edge.capacity - edge.flow:
                    self.used[edge.end] = edge
                    current_flow = min(current_flow, edge.capacity - edge.flow)
                    queue.append(edge.end)

                    if self.target_vertex == edge.end:
                        return current_flow
        return 0

    def get_deltas_array(self):
        deltas = []
        delta = 1
        deltas.append(delta)
        while 2 * delta <= self.max_capacity:
            delta *= 2
            deltas.append(delta)
        return deltas[::-1]

    def edmonds_karp(self):
        deltas = self.get_deltas_array()
        for delta in deltas:
            current_flow = 1
            while current_flow:
                self.used = [0 for _ in range(self.size)]
                current_flow = self.bfs(self.start_vertex, delta)
                if current_flow:
                    v = self.target_vertex
                    while self.start_vertex != v:
                        u = self.used[v]
                        u.flow += current_flow
                        u.back_edge.flow -= current_flow
                        v = u.start
                self.max_flow += current_flow
        return self.max_flow

    def get_min_cut(self):
        self.edmonds_karp()
        edges_sequence = []
        flow_sum = 0
        if not self.used[0]:
            self.used[0] = 1
        for i in range(self.edges_cnt):
            edge = self.real_edges[i]
            if (self.used[edge.start] and not self.used[edge.end]) \
                    or (not self.used[edge.start] and self.used[edge.end]):
                flow_sum += edge.capacity
                edges_sequence.append(str(i + 1))

        return flow_sum, edges_sequence


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    graph = Graph(n, m)
    for row in data[1:]:
        a, b, c = map(int, row.split())
        graph.add_edge(a - 1, b - 1, c)
    flow_sum, edges_sequence = graph.get_min_cut()
    print(len(edges_sequence), flow_sum)
    print(' '.join(edges_sequence))


if __name__ == "__main__":
    main()
