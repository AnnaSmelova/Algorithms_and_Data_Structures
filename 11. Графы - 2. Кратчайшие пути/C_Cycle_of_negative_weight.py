"""
C. Цикл отрицательного веса
ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод
Дан ориентированный граф. Определите, есть ли в нем цикл отрицательного веса, и если да, то выведите его.

Входные данные
Во входном файле в первой строке число N (1≤N≤100) — количество вершин графа.
В следующих N строках находится по N чисел — матрица смежности графа.
Все веса ребер не превышают по модулю 10000. Если ребра нет, то соответствующее число равно 100000.

Выходные данные
В первой строке выходного файла выведите «YES», если цикл существует или «NO» в противном случае.
При его наличии выведите во второй строке количество вершин в искомом цикле
и в третьей строке — вершины входящие в этот цикл в порядке обхода.

Пример
входные данные
2
0 -1
-1 0
выходные данные
YES
2
2 1

Тут надо найти цикл отрицательного веса при помощи алгоритма Флойда
"""
import sys


INF = 100000


class Graph:
    def __init__(self, n):
        self.size = n
        self.shortest_path = []
        self.next = [[v for v in range(n)] for _ in range(n)]

    def floyd_warshall(self):
        for k in range(self.size):
            for u in range(self.size):
                for v in range(self.size):
                    if (self.shortest_path[u][v] > self.shortest_path[u][k] + self.shortest_path[k][v]
                            and self.shortest_path[u][k] < INF
                            and self.shortest_path[k][v] < INF):
                        self.shortest_path[u][v] = self.shortest_path[u][k] + self.shortest_path[k][v]
                        self.next[u][v] = self.next[u][k]

    def get_negative_cycle(self):
        negative_cycle = []
        for i in range(self.size):
            if self.shortest_path[i][i] < 0:
                v = self.next[i][i]
                while (v + 1) not in negative_cycle:
                    negative_cycle.append(v + 1)
                    v = self.next[v][v]
                ind = negative_cycle.index(v + 1)
                negative_cycle = negative_cycle[ind:]
                break
        return negative_cycle


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    graph = Graph(n)
    for row in data[1:]:
        graph.shortest_path.append(list(map(int, row.split())))
    graph.floyd_warshall()
    cycle = graph.get_negative_cycle()
    if cycle:
        print('YES')
        print(len(cycle))
        print(' '.join(map(str, cycle)))
    else:
        print('NO')


if __name__ == "__main__":
    main()
