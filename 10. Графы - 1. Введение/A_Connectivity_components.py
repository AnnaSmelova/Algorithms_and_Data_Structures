"""
A. Компоненты связности

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан неориентированный граф. Требуется выделить компоненты связности в нем.

Входные данные
Первая строка входного файла содержит два натуральных числа 𝑛 и 𝑚 — количество вершин и ребер графа соответственно
(1≤𝑛≤100000, 0≤𝑚≤200000).
Следующие 𝑚 строк содержат описание ребер по одному на строке.
Ребро номер 𝑖 описывается двумя натуральными числами 𝑏𝑖, 𝑒𝑖 — номерами концов ребра (1≤𝑏𝑖,𝑒𝑖≤𝑛).
Допускаются петли и параллельные ребра.

Выходные данные
В первой строке выходного файла выведите целое число 𝑘 — количество компонент связности графа.
Во второй строке выведите 𝑛 натуральных чисел 𝑎1,𝑎1,…,𝑎𝑛, не превосходящих 𝑘, где 𝑎𝑖 — номер компоненты связности,
которой принадлежит 𝑖-я вершина.

Пример 1
входные данные
3 1
1 2
выходные данные
2
1 1 2

Пример 2
входные данные
4 2
1 3
2 4
выходные данные
2
1 2 1 2
"""
import sys
import threading


RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26
DEFAULT_COLOR = 0


class Graph:
    def __init__(self, n):
        self.graph_list = [set() for _ in range(n)]
        self.colors = [DEFAULT_COLOR for _ in range(n)]

    def add_edge(self, a, b):
        self.graph_list[a].add(b)
        self.graph_list[b].add(a)

    def dfs(self, v, color):
        self.colors[v] = color
        for v_neighbor in self.graph_list[v]:
            if DEFAULT_COLOR == self.colors[v_neighbor]:
                self.dfs(v_neighbor, color)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())

    graph = Graph(n)
    for row in data[1:]:
        a, b = map(int, row.split())
        graph.add_edge(a - 1, b - 1)

    color = DEFAULT_COLOR
    for v in range(n):
        if DEFAULT_COLOR == graph.colors[v]:
            color += 1
            graph.dfs(v, color)
    print(color)
    print(' '.join(map(str, graph.colors)))


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
