"""
D. Кратчайшие пути
ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод
Вам дан взвешенный ориентированный граф и вершина s в нём.
Для каждой вершины графа u выведите длину кратчайшего пути от вершины s до вершины u.

Входные данные
Первая строка входного файла содержит три целых числа n, m, s — количество вершин и ребёр в графе
и номер начальной вершины соответственно (2≤n≤2000, 1≤m≤5000).

Следующие m строчек описывают рёбра графа. Каждое ребро задаётся тремя числами — начальной вершиной,
конечной вершиной и весом ребра соответственно.
Вес ребра — целое число, не превосходящее 10^15 по абсолютной величине. В графе могут быть кратные рёбра и петли.

Выходные данные
Выведите n строчек — для каждой вершины u выведите длину кратчайшего пути из s в u.
Если не существует пути между s и u, выведите «*».
Если не существует кратчайшего пути между s и u, выведите «-».

Пример
входные данные
6 7 1
1 2 10
2 3 5
1 3 100
3 5 7
5 4 10
4 3 -18
6 1 -1
выходные данные
0
10
-
-
-
*

Моя любимая задача на кратчайшие пути Форд-Белман настало твое время!
Дополнительно нужно еще осознать, что значит "путь между вершинами есть, а кратчайшего пути нет"
"""
import sys
import threading


INF = float('inf')
RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26
GOOD_COLOR = 0
BAD_COLOR = 1


class Edge:
    def __init__(self, a, b, w):
        self.start = a
        self.end = b
        self.weight = w


class Graph:
    def __init__(self, n, s):
        self.size = n
        self.edges = set()
        self.shortest_paths = [INF for _ in range(n)]
        self.shortest_paths[s] = 0
        self.prev = [-1 for _ in range(n)]
        self.graph_list = [set() for _ in range(n)]
        self.colors = [GOOD_COLOR for _ in range(n)]

    def add_edge(self, a, b, w):
        self.graph_list[a].add(b)
        self.edges.add(Edge(a, b, w))

    def ford_bellman(self):
        for _ in range(self.size):
            for edge in self.edges:
                if self.shortest_paths[edge.start] != INF:
                    if self.shortest_paths[edge.end] > self.shortest_paths[edge.start] + edge.weight:
                        self.shortest_paths[edge.end] = self.shortest_paths[edge.start] + edge.weight
                        self.prev[edge.end] = edge.start

    def get_negative_cycles(self):
        negative_cycles_vs = set()
        for edge in self.edges:
            if self.shortest_paths[edge.start] != INF:
                if self.shortest_paths[edge.end] > self.shortest_paths[edge.start] + edge.weight:
                    v = edge.end
                    for _ in range(self.size):
                        v = self.prev[v]
                    current = v
                    while self.prev[current] != v:
                        negative_cycles_vs.add(current)
                        current = self.prev[current]
                    negative_cycles_vs.add(current)
        return negative_cycles_vs

    def dfs(self, v, color):
        self.colors[v] = color
        for v_neighbor in self.graph_list[v]:
            if GOOD_COLOR == self.colors[v_neighbor]:
                self.dfs(v_neighbor, color)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m, s = map(int, data[0].split())
    graph = Graph(n, s - 1)
    for row in data[1:]:
        u, v, w = map(int, row.split())
        graph.add_edge(u - 1, v - 1, w)
    graph.ford_bellman()

    negative_cycles_vs = graph.get_negative_cycles()

    for v in negative_cycles_vs:
        if GOOD_COLOR == graph.colors[v]:
            graph.dfs(v, BAD_COLOR)

    for i in range(n):
        if INF == graph.shortest_paths[i]:
            print("*")
        else:
            if BAD_COLOR == graph.colors[i]:
                print("-")
            else:
                print(graph.shortest_paths[i])


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
