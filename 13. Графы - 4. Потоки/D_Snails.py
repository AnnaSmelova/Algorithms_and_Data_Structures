"""
D. Улиточки

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 1024 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Две улиточки Маша и Петя сейчас находятся на лужайке с абрикосами и хотят добраться до своего домика.
Лужайки пронумерованы числами от 1 до n и соединены дорожками (может быть несколько дорожек соединяющих две лужайки,
могут быть дорожки, соединяющие лужайку с собой же).
По соображениям гигиены, если по дорожке проползла улиточка, то вторая по той же дорожке уже ползти не может.
Помогите Пете и Маше добраться до домика.

Входные данные
В первой строке файла записаны четыре целых числа — n, m, s и t
(количество лужаек, количество дорог, номер лужайки с абрикосами и номер домика).
В следующих m строках записаны пары чисел. Пара чисел (x,y) означает, что есть дорожка с лужайки x до лужайки y
(из-за особенностей улиток и местности дорожки односторонние). Ограничения: 2<=n<=10^5, 0<=m<=10^5, s!=t.

Выходные данные
Если существует решение, то выведите YES и на двух отдельных строчках сначала последовательность лужаек для Машеньки
(дам нужно пропускать вперед), затем путь для Пети.
Если решения не существует, выведите NO.
Если решений несколько, выведите любое.

Примеры
входные данные
3 3 1 3
1 2
1 3
2 3
выходные данные
YES
1 3
1 2 3
Примечание
Дан орграф, найти два непересекающихся по ребрам пути из s в t, вывести вершины найденных путей.

Задача сводится к поиску непересекающихся путей
"""
import sys
from collections import defaultdict, deque


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
    def __init__(self, n, s, t):
        self.size = n
        self.edges = defaultdict(list)
        self.real_edges = []
        self.max_flow = 0
        self.start_vertex = s
        self.target_vertex = t
        self.used = [0 for _ in range(n)]
        self.paths = []

    def add_edge(self, a, b, c):
        edge = Edge(a, b, c)
        back_edge = Edge(b, a, 0)

        back_edge.set_back_edge(edge)
        edge.set_back_edge(back_edge)

        self.edges[a].append(edge)
        self.edges[b].append(back_edge)

        self.real_edges.append(edge)

    def bfs(self, v):
        queue = deque([v])
        current_flow = INF
        while queue:
            current_v = queue.popleft()
            for edge in self.edges[current_v]:
                if not self.used[edge.end] and edge.flow < edge.capacity:
                    self.used[edge.end] = edge
                    current_flow = min(current_flow, edge.capacity - edge.flow)
                    queue.append(edge.end)

                    if self.target_vertex == edge.end:
                        return current_flow
        return 0

    def edmonds_karp(self):
        current_flow = 1
        while current_flow:
            self.used = [0 for _ in range(self.size)]
            current_flow = self.bfs(self.start_vertex)
            if current_flow:
                v = self.target_vertex
                while self.start_vertex != v:
                    u = self.used[v]
                    u.flow += current_flow
                    u.back_edge.flow -= current_flow
                    v = u.start
            self.max_flow += current_flow

        for edge in self.real_edges:
            edge.capacity = edge.flow
            edge.flow = 0

        return self.max_flow

    def get_paths_by_bfs(self):
        self.edmonds_karp()

        if self.max_flow < 2:
            return False

        path_cnt = 0
        while path_cnt < 2:
            path_cnt += 1
            self.used = [0 for _ in range(self.size)]
            current_flow = self.bfs(self.start_vertex)
            if current_flow:
                path = []
                v = self.target_vertex
                path.append(str(v + 1))
                while self.start_vertex != v:
                    u = self.used[v]
                    u.flow += current_flow
                    u.back_edge.flow -= current_flow
                    v = u.start
                    path.append(str(v + 1))
                self.paths.append(path[::-1])
            else:
                return False

        return True


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m, s, t = map(int, data[0].split())
    s = s - 1
    t = t - 1
    graph = Graph(n, s, t)
    for row in data[1:]:
        a, b = map(int, row.split())
        if a != b:
            graph.add_edge(a - 1, b - 1, 1)
    if graph.get_paths_by_bfs():
        print('YES')
        print(' '.join(graph.paths[0]))
        print(' '.join(graph.paths[1]))
    else:
        print('NO')


if __name__ == "__main__":
    main()
