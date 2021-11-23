"""
B. Кратчайший путь – 2
ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод
Дан неориентированный связный взвешенный граф.
Найдите кратчайшее расстояние от первой вершины до всех вершин.

Входные данные
В первой строке входного файла два числа: 𝑛 и 𝑚 (2≤𝑛≤30000,1≤𝑚≤400000),
где 𝑛 — количество вершин графа, а 𝑚 — количество ребер.

Следующие 𝑚 строк содержат описание ребер.
Каждое ребро задается стартовой вершиной, конечной вершиной и весом ребра.
Вес каждого ребра — неотрицательное целое число, не превосходящее 10^4.

Выходные данные
Выведите 𝑛 чисел — для каждой вершины кратчайшее расстояние до нее.

Пример
входные данные
4 5
1 2 1
1 3 5
2 4 8
3 4 1
2 3 3
выходные данные
0 1 4 5

Почекаем дейкстру на приоритетной очереди
"""
import sys
from heapq import heappush, heappop


INF = float('inf')


class Graph:
    def __init__(self, n):
        self.size = n
        self.graph_list = [set() for _ in range(n)]
        self.shortest_path = [INF for _ in range(n)]
        self.shortest_path[0] = 0
        self.visited = [0 for _ in range(n)]

    def add_edge(self, a, b, w):
        self.graph_list[a].add((b, w))
        self.graph_list[b].add((a, w))

    def dijkstra(self):
        heap = []
        heappush(heap, (0, 0))
        for i in range(self.size):
            priority, v = heappop(heap)
            while 1 == self.visited[v]:
                priority, v = heappop(heap)
            self.visited[v] = 1
            for v_neighbor, w in self.graph_list[v]:
                if self.shortest_path[v_neighbor] > self.shortest_path[v] + w:
                    self.shortest_path[v_neighbor] = self.shortest_path[v] + w
                    heappush(heap, (self.shortest_path[v_neighbor], v_neighbor))


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    graph = Graph(n)
    for row in data[1:]:
        a, b, w = map(int, row.split())
        graph.add_edge(a - 1, b - 1, w)

    graph.dijkstra()
    print(' '.join(map(str, graph.shortest_path)))


if __name__ == "__main__":
    main()
