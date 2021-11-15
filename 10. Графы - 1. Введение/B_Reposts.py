"""
B. Репосты

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Однажды Поликарп опубликовал в социальной сети смешную картинку с опросом про цвет своего хэндла.
Многие из его друзей стали репостить шутку Поликарпа себе в ленту. Некоторые из них репостили репосты и так далее.

Эти события заданы в виде последовательности строк «name1 reposted name2» где name1 — это имя того, кто репостнул,
а name2 — имя того, с чей ленты репостнули шутку.
Гарантируется, что для каждой строки «name1 reposted name2» пользователь «name1» еще не имел эту шутку в свой ленте,
а «name2» уже имел ее в своей ленте к моменту репоста.
Поликарп зарегистрирован под именем «Polycarp», и изначально шутка есть только в его ленте.

Поликарп измеряет успешность шутки как длину наибольшей цепочки репостов.
Выведите успешность шутки Поликарпа.

Входные данные
В первой строке входных данных записано целое число n (1≤n≤200) — количество репостов.
Далее записаны сами репосты в порядке их совершения.
Каждый из них записан в отдельной строке и имеет вид «name1 reposted name2».
Все имена во входных данных состоят из прописных или строчных латинских букв и/или цифр и имеют длины от
2 до 24 символов включительно.

Известно, что имена пользователей регистронезависимы, то есть два имени, отличающиеся исключительно регистром букв,
соответствуют одному и тому же пользователю соцсети.

Выходные данные
Выведите единственное целое число — максимальную длину цепочки репостов.

Пример 1
входные данные
5
tourist reposted Polycarp
Petr reposted Tourist
WJMZBMR reposted Petr
sdya reposted wjmzbmr
vepifanov reposted sdya
выходные данные
6

Пример 2
входные данные
6
Mike reposted Polycarp
Max reposted Polycarp
EveryOne reposted Polycarp
111 reposted Polycarp
VkCup reposted Polycarp
Codeforces reposted Polycarp
выходные данные
2

Пример 3
входные данные
1
SoMeStRaNgEgUe reposted PoLyCaRp
выходные данные
2

Применение поиска в глубину
"""
import sys
import threading
from collections import defaultdict


RECURSION_LIMIT = 10 ** 9
STACK_SIZE = 2 ** 26
FIRST_USER = 'polycarp'
DEFAULT_NUM = 0
UNICODE = "utf-8"


class Graph:
    def __init__(self, n):
        self.graph_list = defaultdict(set)
        self.order = defaultdict(int)

    def add_edge(self, a, b):
        self.graph_list[a].add(b)
        self.graph_list[b].add(a)
        self.order[a] = DEFAULT_NUM
        self.order[b] = DEFAULT_NUM

    def dfs(self, v, num):
        num += 1
        self.order[v] = num
        for v_neighbor in self.graph_list[v]:
            if DEFAULT_NUM == self.order[v_neighbor]:
                self.dfs(v_neighbor, num)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n = int(data[0])

    graph = Graph(n)
    for row in data[1:]:
        a, action, b = row.decode(UNICODE).split()
        a, b = a.lower(), b.lower()
        graph.add_edge(a, b)

    graph.dfs(FIRST_USER, DEFAULT_NUM)
    print(max(graph.order.values()))


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    threading.stack_size(STACK_SIZE)
    thread = threading.Thread(target=main)
    thread.start()
