"""
C. Остовное дерево

ограничение по времени на тест: 4 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Даны точки на плоскости, являющиеся вершинами полного графа.
Вес ребра равен расстоянию между точками, соответствующими концам этого ребра.
Требуется в этом графе найти остовное дерево минимального веса.

Входные данные
Первая строка входного файла содержит натуральное число 𝑛 — количество вершин графа (1≤𝑛≤10000).
Каждая из следующих 𝑛 строк содержит два целых числа 𝑥𝑖, 𝑦𝑖  — координаты 𝑖-й вершины (−10000≤𝑥𝑖,𝑦𝑖≤10000).
Никакие две точки не совпадают.

Выходные данные
Первая строка выходного файла должна содержать одно вещественное число — вес минимального остовного дерева.

Пример
входные данные
2
0 0
1 1
выходные данные
1.4142135624

Вижу полный граф, пишу Прима
"""
import sys
from math import sqrt

INF = float('inf')


class Graph:
    def __init__(self, n, vertexes_list):
        self.size = n
        self.vertexes = vertexes_list
        self.shortest_path = [INF for _ in range(n)]
        self.shortest_path[0] = 0
        self.visited = [0 for _ in range(n)]
        self.path = 0

    @staticmethod
    def get_edge_weight(v1, v2):
        v1_x, v1_y = v1
        v2_x, v2_y = v2
        if v1 == v2:
            return INF
        return sqrt((v1_x - v2_x) ** 2 + (v1_y - v2_y) ** 2)

    def prima(self):
        for i in range(self.size):
            v_next = None
            for v in range(self.size):
                if 1 != self.visited[v] and \
                        (v_next is None or self.shortest_path[v] < self.shortest_path[v_next]):
                    v_next = v
            self.visited[v_next] = 1
            self.path += self.shortest_path[v_next]
            for v in range(self.size):
                if v != v_next and 1 != self.visited[v]:
                    w = self.get_edge_weight(self.vertexes[v], self.vertexes[v_next])
                    self.shortest_path[v] = min(self.shortest_path[v], w)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    vertexes = [None for _ in range(n)]
    for ind, row in enumerate(data[1:]):
        x, y = map(int, row.split())
        vertexes[ind] = [x, y]
    graph = Graph(n, vertexes)
    graph.prima()
    print(graph.path)


if __name__ == "__main__":
    main()
