"""
B. Подсчет опыта

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 64 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод
В очередной онлайн игре игроки, как обычно, сражаются с монстрами и набирают опыт.
Для того, чтобы сражаться с монстрами, они объединяются в кланы.
После победы над монстром, всем участникам клана, победившего его, добавляется одинаковое число единиц опыта.
Особенностью этой игры является то, что кланы никогда не распадаются и из клана нельзя выйти.
Единственная доступная операция — объединение двух кланов в один.

Поскольку игроков стало уже много, вам поручили написать систему учета текущего опыта игроков.

Входные данные
В первой строке входного файла содержатся числа
n (1≤n≤200000) и m 1≤m≤200000 — число зарегистрированных игроков и число запросов.

В следующих m строках содержатся описания запросов. Запросы бывают трех типов:

join X Y — объединить кланы, в которые входят игроки X и Y (если они уже в одном клане, то ничего не меняется).
add X V — добавить V единиц опыта всем участникам клана, в который входит игрок X (1≤V≤100).
get X — вывести текущий опыт игрока X.
Изначально у всех игроков 0 опыта и каждый из них состоит в клане, состоящим из него одного.

Выходные данные
Для каждого запроса get X выведите текущий опыт игрока X.

Пример
входные данные
3 6
add 1 100
join 1 3
add 1 50
get 1
get 2
get 3
выходные данные
150
0
50

Прикольная задачка на применение СНМ, не забываем обе эвристики
"""
import sys


UNICODE = "utf-8"


class DSU:
    def __init__(self, n):
        self.parents = [i for i in range(n)]
        self.childs = [[i] for i in range(n)]
        self.experience = [0 for _ in range(n)]
        self.sizes = [1 for _ in range(n)]

    def get_parent(self, el):
        if self.parents[el] != el:
            self.parents[el] = self.get_parent(self.parents[el])
        return self.parents[el]

    def get_experience(self, el):
        return self.experience[el]

    def join(self, el_1, el_2):
        p_1 = self.get_parent(el_1)
        p_2 = self.get_parent(el_2)
        if p_1 != p_2:
            if self.sizes[p_1] < self.sizes[p_2]:
                p_1, p_2 = p_2, p_1
            self.parents[p_2] = p_1
            self.sizes[p_1] += self.sizes[p_2]
            self.childs[p_1].extend(self.childs[p_2])

    def add_experience(self, el, value):
        parent = self.get_parent(el)
        for child in self.childs[parent]:
            self.experience[child] += value


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    dsu = DSU(n)
    for row in data[1:]:
        args = row.decode(UNICODE).split()
        if args[0] == 'get':
            print(dsu.get_experience(int(args[1]) - 1))
        elif args[0] == 'join':
            args[1], args[2] = int(args[1]) - 1, int(args[2]) - 1
            if args[1] != args[2]:
                dsu.join(args[1], args[2])
        elif args[0] == 'add':
            args[1], args[2] = int(args[1]) - 1, int(args[2])
            if args[2] != 0:
                dsu.add_experience(args[1], args[2])


if __name__ == "__main__":
    main()
