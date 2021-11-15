"""
D. Конденсация графа

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Конденсацией графа 𝐺 называется новый граф 𝐻, где каждой компоненте сильной связности в графе 𝐺
соответствует вершина из графа 𝐻.
Ребро 𝑣𝑢 в графе 𝐻 есть тогда и только тогда, когда в графе 𝐺 существует хотя бы одно ребро из
соответствующей 𝑣 компоненте сильной связности, в компоненту, соответствующую 𝑢.

Требуется найти количество ребер в конденсации ориентированного графа.
Примечание: конденсация графа не содержит кратных ребер.

Входные данные
Первая строка входного файла содержит два натуральных числа 𝑛 и 𝑚 — количество вершин и ребер графа
соответственно (𝑛≤10000, 𝑚≤100000).
Следующие 𝑚 строк содержат описание ребер, по одному на строке.
Ребро номер 𝑖 описывается двумя натуральными числами 𝑏𝑖, 𝑒𝑖 — началом и концом ребра соответственно (1 ≤ 𝑏𝑖, 𝑒𝑖 ≤ 𝑛).
В графе могут присутствовать кратные ребра и петли.

Выходные данные
Единственная строка выходного файла должна содержать одно число — количество ребер в конденсации графа.

Пример
входные данные
4 4
2 1
3 2
2 3
4 3
выходные данные
2
"""
import sys
import threading


RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26
WHITE_COLOR = 0
GREY_COLOR = 1


class Graph:
    def __init__(self, n):
        self.graph_list = [[] for _ in range(n)]
        self.colors = [WHITE_COLOR for _ in range(n)]
        self.sorted_vs = []

    def add_edge(self, a, b):
        self.graph_list[a].append(b)

    def dfs(self, v, color):
        self.colors[v] = color
        for v_neighbor in self.graph_list[v]:
            if WHITE_COLOR == self.colors[v_neighbor]:
                self.dfs(v_neighbor, color)
        self.sorted_vs.append(v)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())

    graph = Graph(n)
    graph_back = Graph(n)
    for row in data[1:]:
        a, b = map(int, row.split())
        a, b = a - 1, b - 1
        graph.add_edge(a, b)
        graph_back.add_edge(b, a)

    for v in range(n):
        if WHITE_COLOR == graph.colors[v]:
            graph.dfs(v, GREY_COLOR)

    color = WHITE_COLOR
    for v in graph.sorted_vs[::-1]:
        if WHITE_COLOR == graph_back.colors[v]:
            color += 1
            graph_back.dfs(v, color)

    cond_graph_edges = set()
    for v in range(n):
        for v_neighbor in graph.graph_list[v]:
            c_1, c_2 = graph_back.colors[v], graph_back.colors[v_neighbor]
            if c_1 != c_2:
                cond_graph_edges.add(f'{c_1}_{c_2}')
    print(len(cond_graph_edges))


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
