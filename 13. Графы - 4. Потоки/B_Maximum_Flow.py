"""
B. Просто поток

ограничение по времени на тест: 5 секунд
ограничение по памяти на тест: 1024 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Дана система из узлов и труб, по которым может течь вода.
Для каждой трубы известна наибольшая скорость, с которой вода может протекать через нее.
Известно, что вода течет по трубам таким образом, что за единицу времени в каждый узел
(за исключением двух — источника и стока) втекает ровно столько воды, сколько из него вытекает.

Ваша задача — найти наибольшее количество воды, которое за единицу времени может протекать между источником и стоком,
а также скорость течения воды по каждой из труб.

Трубы являются двусторонними, то есть вода в них может течь в любом направлении.
Между любой парой узлов может быть более одной трубы.

Входные данные
В первой строке записано натуральное число 𝑁 — количество узлов в системе (2≤𝑁≤100).
Известно, что источник имеет номер 1, а сток номер 𝑁.
Во второй строке записано натуральное 𝑀 (1≤𝑀≤5000) — количество труб в системе.
Далее в 𝑀 строках идет описание труб.
Каждая труба задается тройкой целых чисел 𝐴𝑖, 𝐵𝑖, 𝐶𝑖, где 𝐴𝑖, 𝐵𝑖 — номера узлов, которые соединяет данная труба (𝐴𝑖≠𝐵𝑖),
а 𝐶𝑖 (0≤𝐶𝑖≤10^4) — наибольшая допустимая скорость течения воды через данную трубу.

Выходные данные
В первой строке выведите наибольшее количество воды, которое протекает между источником и стоком за единицу времени.
Далее выведите 𝑀 строк, в каждой из которых выведите скорость течения воды по соответствующей трубе.
Если направление не совпадает с порядком узлов, заданным во входных данных,
то выводите скорость со знаком минус. Числа выводите с точностью 10^−3.

Примеры
входные данные
2
2
1 2 1
2 1 3
выходные данные
4
1
-3

То же самое, но Эдмондс-Карп с масштабированием
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
    def __init__(self, n):
        self.size = n
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


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    m = int(data[1])
    graph = Graph(n)
    for row in data[2:]:
        a, b, c = map(int, row.split())
        graph.add_edge(a - 1, b - 1, c)
    print(graph.edmonds_karp())
    for edge in graph.real_edges:
        print(edge.flow)


if __name__ == "__main__":
    main()
