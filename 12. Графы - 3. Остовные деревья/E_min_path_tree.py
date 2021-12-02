"""
E. Минимальное дерево путей

ограничение по времени на тест: 6 секунд
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Вам дан взвешенный ориентированный граф, содержащий 𝑛 вершин и 𝑚 рёбер.
Найдите минимально возможную сумму весов 𝑛−1 ребра, которые нужно оставить в графе,
чтобы из вершины с номером 1 по этим ребрам можно было добраться до любой другой вершины.

Входные данные
В первой строке даны два целых числа 𝑛 и 𝑚 (1≤𝑛≤1000, 0≤𝑚≤10000) — количество вершин и ребер в графе.

В следующих 𝑚 строках даны ребра графа. Ребро описывается тройкой чисел
𝑎𝑖, 𝑏𝑖 и 𝑤𝑖 (1≤𝑎𝑖,𝑏𝑖≤𝑛; −10^9≤𝑤𝑖≤10^9) — номер вершины, из которой исходит ребро, номер вершины,
в которую входит ребро, и вес ребра.

Выходные данные
Если нельзя оставить подмножество ребер так, чтобы из вершины с номером 1 можно было добраться до любой другой,
в единственной строке выведите «NO».

Иначе, в первой строке выведите «YES», а во второй строке выведите минимальную возможную сумму весов ребер,
которых необходимо оставить.

Примеры
входные данные
2 1
2 1 10
выходные данные
NO
входные данные
4 5
1 2 2
1 3 3
1 4 3
2 3 2
2 4 2
выходные данные
YES
6

О, ориентированный граф, выпускайте двух китайцев!
"""
import sys
from collections import defaultdict
from itertools import chain


ROOT = 1
INF = float('inf')
WHITE_COLOR = 0
GREY_COLOR = 1


class Edge:
    def __init__(self, a, b, w):
        self.start = a
        self.end = b
        self.weight = w


class Graph:
    def __init__(self, n):
        self.size = n
        self.edges = defaultdict(list)
        self.edges_min = [INF for _ in range(n)]
        self.path = 0
        self.colors = [WHITE_COLOR for _ in range(n)]
        self.visited = set()
        self.distances = defaultdict(int)

    def add_edge(self, a, b, w):
        self.edges[a].append(Edge(a, b, w))

    def get_back_graph(self):
        back_graph = Graph(self.size)
        for edge in chain.from_iterable(self.edges.values()):
            back_graph.add_edge(edge.end, edge.start, edge.weight)
        return back_graph

    def dfs(self, v, color, zero=False):
        self.colors[v] = color
        for edge in self.edges[v]:
            cond = True
            if zero:
                cond = (0 == edge.weight)
            if cond and WHITE_COLOR == self.colors[edge.end]:
                self.dfs(edge.end, color, zero)

    def check_by_dfs(self, zero=False):
        color = WHITE_COLOR
        for v in range(self.size):
            if WHITE_COLOR == self.colors[v]:
                color += 1
                self.dfs(v, color, zero)
        if color == 1:
            return True
        else:
            return False

    def dfs_find_dist(self, v, dist):
        self.visited.add(v)
        for edge in self.edges[v]:
            if edge.end not in self.visited and 0 == edge.weight:
                dist = self.dfs_find_dist(edge.end, dist)
        self.distances[v] = dist
        dist += 1
        return dist

    def get_sorted_vs(self):
        dist = 0
        for v in list(self.edges.keys()):
            if v not in self.visited:
                dist = self.dfs_find_dist(v, dist)
        return sorted(range(self.size), key=self.distances.__getitem__, reverse=True)

    def get_condensation_graph(self, v_root, sorted_vs):
        color = WHITE_COLOR
        for v in sorted_vs:
            if WHITE_COLOR == self.colors[v]:
                color += 1
                self.dfs(v, color, True)

        condensation_graph = Graph(color)
        v_root = self.colors[v_root] - 1
        for edge in chain.from_iterable(self.edges.values()):
            c_start = self.colors[edge.start]
            c_end = self.colors[edge.end]
            if c_start != c_end and c_start - 1 != v_root:
                condensation_graph.add_edge(c_end - 1, c_start - 1, edge.weight)

        return condensation_graph, v_root

    def find_mst(self, v_root):
        current_graph = self
        while True:
            current_graph.colors = [WHITE_COLOR for _ in range(current_graph.size)]
            for edge in chain.from_iterable(current_graph.edges.values()):
                current_graph.edges_min[edge.end] = min(edge.weight, current_graph.edges_min[edge.end])
            for v in range(current_graph.size):
                if v != v_root:
                    if current_graph.edges_min[v] == INF:
                        return INF
                    self.path += current_graph.edges_min[v]
            for edge in chain.from_iterable(current_graph.edges.values()):
                edge.weight -= current_graph.edges_min[edge.end]

            check = current_graph.check_by_dfs(zero=True)
            if check:
                return self.path

            graph_back = current_graph.get_back_graph()
            sorted_vs = current_graph.get_sorted_vs()

            current_graph, v_root = graph_back.get_condensation_graph(v_root, sorted_vs)

        return self.path


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    if m < n - 1:
        print('NO')
    else:
        graph = Graph(n)
        for row in data[1:]:
            u, v, w = map(int, row.split())
            if u != v and v != ROOT:
                graph.add_edge(u - 1, v - 1, w)
        graph.dfs(ROOT - 1, GREY_COLOR)
        if len(set(graph.colors)) == 1:
            if graph.find_mst(ROOT - 1) != INF:
                print('YES')
                print(graph.path)
            else:
                print('NO')
        else:
            print('NO')


if __name__ == "__main__":
    main()
