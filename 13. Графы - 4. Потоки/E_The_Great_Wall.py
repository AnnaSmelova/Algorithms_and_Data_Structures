"""
E. Великая стена

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 1024 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

У короля Людовика двое сыновей.
Они ненавидят друг друга, и король боится, что после его смерти страна будет уничтожена страшными войнами.
Поэтому Людовик решил разделить свою страну на две части, в каждой из которых будет властвовать один из его сыновей.
Он посадил их на трон в города A и B, и хочет построить минимально возможное количество фрагментов стены таким образом,
 чтобы не существовало пути из города A в город B.

Страну, в которой властвует Людовик, можно упрощенно представить в виде прямоугольника m×n.
В некоторых клетках этого прямоугольника расположены горы, по остальным же можно свободно перемещаться.
Кроме этого, ландшафт в некоторых клетках удобен для строительства стены, в остальных же строительство невозможно.

При поездках по стране можно перемещаться из клетки в соседнюю по стороне,
только если ни одна из этих клеток не содержит горы или построенного фрагмента стены.

Входные данные
В первой строке входного файла содержатся числа m и n (1≤m,n≤50).
Следующие m строк по n символов задают карту страны. Символы обозначают: «#» — гора, «.» — место,
пригодное для постройки стены, «-» — место, не пригодное для постройки стены, «A» и «B» — города A и B.

Выходные данные
В первой строке выходного файла должно быть выведено минимальное количество фрагментов стены F,
которые необходимо построить. Далее нужно вывести карту в том же формате, как во входном файле.
Клетки со стеной обозначьте символом «+».

Если невозможно произвести требуемую застройку, то выведите в выходной файл единственное число -1.

Пример 1
входные данные
5 5
--...
A-.#-
.#.#-
--.--
--.-B
выходные данные
3
--+..
A-+#-
+#.#-
--.--
--.-B

Пример 2
входные данные
1 2
AB
выходные данные
-1

Пример 3
входные данные
2 2
A#
#B
выходные данные
0
A#
#B
"""
import sys
from collections import defaultdict, deque

UNICODE = "utf-8"
INF = float('inf')


class Edge:
    def __init__(self, v_start, v_end, c, row, col, town=None, is_wall=False, is_mountain=False, can_build=False):
        self.start = v_start
        self.end = v_end
        self.capacity = c
        self.row = row
        self.col = col
        self.flow = 0
        self.back_edge = None

        self.town = town
        self.is_wall = is_wall
        self.is_mountain = is_mountain
        self.can_build = can_build

    def set_back_edge(self, back_edge):
        self.back_edge = back_edge


class Graph:
    def __init__(self, m, n, size):
        self.rows_cnt = m
        self.cols_cnt = n
        self.vertexes = [None for _ in range(size)]
        self.size = size
        self.edges = defaultdict(list)
        self.real_edges = []
        self.max_flow = 0
        self.start_vertex = None
        self.target_vertex = None
        self.used = [0 for _ in range(size)]

    def add_edge(self, a, b, c, i, j, is_real=False, town=None, is_wall=False, is_mountain=False, can_build=False):
        edge = Edge(a, b, c, i, j, town, is_wall, is_mountain, can_build)
        back_edge = Edge(b, a, 0, i, j, town, is_wall, is_mountain, can_build)

        back_edge.set_back_edge(edge)
        edge.set_back_edge(back_edge)

        self.edges[a].append(edge)
        self.edges[b].append(back_edge)
        if is_real:
            self.real_edges.append(edge)

    def add_pseudo_edges(self, m, n, size):
        for row in range(m - 1):
            for col in range(n - 1):
                self.add_edge(row * n + col + size, (row + 1) * n + col, INF, -row, col)
                self.add_edge((row + 1) * n + col + size, row * n + col, INF, -row, col)
                self.add_edge(row * n + col + size, row * n + col + 1, INF, -row, col)
                self.add_edge(row * n + col + 1 + size, row * n + col, INF, -row, col)

        for row in range(m - 1):
            self.add_edge(row * n + (n - 1) + size, (row + 1) * n + (n - 1), INF, -(n - 1), m)
            self.add_edge((row + 1) * n + (n - 1) + size, row * n + (n - 1), INF, -(n - 1), m)

        for col in range(n - 1):
            self.add_edge((m - 1) * n + col + size, (m - 1) * n + col + 1, INF, -(m - 1), n)
            self.add_edge((m - 1) * n + col + 1 + size, (m - 1) * n + col, INF, -(m - 1), n)

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

    def edmonds_karp(self):
        deltas = [INF, 1]
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

    def get_min_cut(self):
        self.edmonds_karp()
        cnt = 0
        if self.max_flow == INF:
            return cnt, INF
        elif self.max_flow == 0:
            return cnt, 0
        if not self.used[self.start_vertex]:
            self.used[self.start_vertex] = 1
        flow_sum = 0
        for i, edge in enumerate(self.real_edges):
            if self.used[edge.start] and not self.used[edge.end]:
                if edge.capacity > 0:
                    cnt += 1
                    flow_sum += edge.capacity
                    edge.is_wall = True

        return cnt, flow_sum

    def get_graph_img(self):
        result = ''
        current_row = 0
        for edge in self.real_edges:
            if edge.row > current_row:
                result += '\n'
                current_row += 1
            if edge.is_wall:
                result += '+'
            elif edge.town == 'A':
                result += 'A'
            elif edge.town == 'B':
                result += 'B'
            elif edge.is_mountain:
                result += '#'
            elif edge.can_build:
                result += '.'
            else:
                result += '-'
        return result

    def __str__(self):
        return self.get_graph_img()


def main():
    data = sys.stdin.buffer.read().splitlines()
    m, n = map(int, data[0].split())
    size = m * n
    graph = Graph(m, n, size * 2)
    for row, string in enumerate(data[1:]):
        string = string.decode(UNICODE)
        for col, el in enumerate(string):
            if el == '#':
                graph.add_edge(row * n + col, row * n + col + size, 0, row, col, True, is_mountain=True)
            elif el == '.':
                graph.add_edge(row * n + col, row * n + col + size, 1, row, col, True, can_build=True)
            elif el == '-':
                graph.add_edge(row * n + col, row * n + col + size, INF, row, col, True)
            elif el == 'A':
                graph.start_vertex = row * n + col + size
                graph.add_edge(row * n + col + size, row * n + col + size, 0, row, col, True, town='A')
            elif el == 'B':
                graph.target_vertex = row * n + col
                graph.add_edge(row * n + col, row * n + col, 0, row, col, True, town='B')
    graph.add_pseudo_edges(m, n, size)

    cnt, flow_sum = graph.get_min_cut()
    if flow_sum == INF:
        print(-1)
    else:
        print(cnt)
        print(graph)


if __name__ == "__main__":
    main()
