"""
E. Точки сочленения

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан неориентированный граф. Требуется найти все точки сочленения в нём.

Входные данные
Первая строка входного файла содержит два натуральных числа 𝑛 и 𝑚 — количества вершин и рёбер графа
соответственно (1⩽𝑛⩽20000, 1⩽𝑚⩽200000).
Следующие 𝑚 строк содержат описание рёбер по одному на строке.
Ребро номер 𝑖 описывается двумя натуральными числами 𝑏𝑖, 𝑒𝑖 — номерами концов ребра (1⩽𝑏𝑖,𝑒𝑖⩽𝑛).

Выходные данные
Первая строка выходного файла должна содержать одно натуральное число 𝑏 — количество точек сочленения в заданном графе.
На следующей строке выведите 𝑏 целых чисел — номера вершин, которые являются точками сочленения, в возрастающем порядке.

Пример
входные данные
6 7
1 2
2 3
2 4
2 5
4 5
1 3
3 6
выходные данные
2
2 3
"""
import sys
import threading


RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26


class Graph:
    def __init__(self, n):
        self.graph_list = [set() for _ in range(n)]
        self.visited = [False for _ in range(n)]
        self.tin = [0 for _ in range(n)]
        self.up = [0 for _ in range(n)]
        self.cut_points = set()

    def add_edge(self, a, b):
        self.graph_list[a].add(b)
        self.graph_list[b].add(a)

    def dfs(self, v, time, parent):
        self.visited[v] = True
        time += 1
        self.tin[v] = time
        self.up[v] = time
        children_num = 0
        for v_neighbor in self.graph_list[v]:
            if v == v_neighbor:
                continue
            if self.visited[v_neighbor]:
                self.up[v] = min(self.up[v], self.tin[v_neighbor])
            else:
                self.dfs(v_neighbor, time, v)
                self.up[v] = min(self.up[v], self.up[v_neighbor])
                if self.up[v_neighbor] >= self.tin[v] and parent != -1:
                    self.cut_points.add(v + 1)
                children_num += 1
        if parent == -1 and children_num > 1:
            self.cut_points.add(v + 1)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())

    graph = Graph(n)
    for row in data[1:]:
        a, b = map(int, row.split())
        graph.add_edge(a - 1, b - 1)

    for v in range(n):
        if graph.visited[v] == 0:
            graph.dfs(v, 0, -1)
    print(len(graph.cut_points))
    print(' '.join(map(str, sorted(list(graph.cut_points)))))


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
