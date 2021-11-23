"""
A. Приключения шахматного коня
ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод
На шахматной доске N×N в клетке (x1, y1) стоит голодный шахматный конь.
Он хочет попасть в клетку (x2, y2), где растет вкусная шахматная трава.
Какое наименьшее количество ходов он должен для этого сделать?

Входные данные
На вход программы поступает пять чисел: N,x1,y1,x2,y2 (5≤N≤20,1≤x1,y1,x2,y2≤N).
Левая верхняя клетка доски имеет координаты (1,1), правая нижняя — (N,N).

Выходные данные
В первой строке выведите единственное число K — количество посещенных клеток.
В каждой из следующих K строк должно быть записано 2 числа — координаты очередной клетки в пути коня.

Пример
входные данные
5
1 1
3 2
выходные данные
2
1 1
3 2

Где-то здесь спрятался граф, еще и невзвешенный, можно попробовать запустить обход в ширину
"""
import sys
from collections import deque


class Graph:
    def __init__(self, n, v_start):
        self.visited = {v_start: 0}
        self.limit = n

    def move_knight(self, x, y):
        steps = [(x + 1, y + 2),
                 (x + 2, y + 1),
                 (x + 2, y - 1),
                 (x + 1, y - 2),
                 (x - 1, y - 2),
                 (x - 2, y - 1),
                 (x - 2, y + 1),
                 (x - 1, y + 2)]

        possible_steps = [(x_p, y_p) for (x_p, y_p) in steps if 1 <= x_p <= self.limit and 1 <= y_p <= self.limit]
        return possible_steps

    def bfs(self, v_start):
        queue = deque([v_start])
        while queue:
            cur_x, cur_y = queue.popleft()
            for v in self.move_knight(cur_x, cur_y):
                if v not in self.visited:
                    self.visited[v] = (cur_x, cur_y)
                    queue.append(v)

    def get_path(self, v_start, v_finish):
        path = [v_finish]
        v = v_finish
        while v != v_start:
            v = self.visited[v]
            path.append(v)
        return path[::-1]


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])
    v_start = tuple(map(int, data[1].split()))
    v_finish = tuple(map(int, data[2].split()))

    graph = Graph(n, v_start)
    graph.bfs(v_start)
    path = graph.get_path(v_start, v_finish)
    print(len(path))
    for step in path:
        print(' '.join(map(str, step)))


if __name__ == "__main__":
    main()
