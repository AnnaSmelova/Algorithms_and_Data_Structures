"""
C. Топологическая сортировка

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан ориентированный невзвешенный граф. Необходимо построить его топологическую сортировку.

Входные данные
В первой строке входного файла даны два натуральных числа 𝑛 и 𝑚
(1≤𝑛≤100000, 0≤𝑚≤100000) — число вершин и рёбер в графе соответственно.
Далее в 𝑚 строках перечислены рёбра графа.
Каждое ребро задаётся парой чисел — номерами начальной и конечной вершин соответственно.

Выходные данные
Выведите любую топологическую сортировку графа в виде последовательности номеров вершин.
Если граф невозможно топологически отсортировать, выведите −1.

Пример
входные данные
6 6
1 2
3 2
4 2
2 5
6 5
4 6
выходные данные
4 6 3 1 2 5
"""
import sys
import threading


RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26
WHITE_COLOR = 0
GREY_COLOR = 1
BLACK_COLOR = 2


class Graph:
    def __init__(self, n):
        self.graph_list = [set() for _ in range(n)]
        self.colors = [WHITE_COLOR for _ in range(n)]
        self.has_cycle = False
        self.sorted_vs = []

    def add_edge(self, a, b):
        self.graph_list[a].add(b)

    def dfs(self, v):
        self.colors[v] = GREY_COLOR
        for v_neighbor in self.graph_list[v]:
            if WHITE_COLOR == self.colors[v_neighbor]:
                self.colors[v_neighbor] = GREY_COLOR
                self.dfs(v_neighbor)
            elif GREY_COLOR == self.colors[v_neighbor]:
                self.has_cycle = True
        self.sorted_vs.append(v + 1)
        self.colors[v] = BLACK_COLOR


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())

    graph = Graph(n)
    for row in data[1:]:
        a, b = map(int, row.split())
        graph.add_edge(a - 1, b - 1)

    for v in range(n):
        if WHITE_COLOR == graph.colors[v] and not graph.has_cycle:
            graph.dfs(v)

    if graph.has_cycle:
        print(-1)
    else:
        print(' '.join(map(str, graph.sorted_vs[::-1])))


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
