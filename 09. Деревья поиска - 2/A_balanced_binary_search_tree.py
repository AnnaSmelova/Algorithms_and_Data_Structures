"""
A. Сбалансированное двоичное дерево поиска

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте сбалансированное двоичное дерево поиска.

Входные данные
Входной файл содержит описание операций с деревом, их количество не превышает 10^5.
В каждой строке находится одна из следующих операций:
insert 𝑥 — добавить в дерево ключ 𝑥. Если ключ 𝑥 есть в дереве, то ничего делать не надо;
delete 𝑥 — удалить из дерева ключ 𝑥. Если ключа 𝑥 в дереве нет, то ничего делать не надо;
exists 𝑥 — если ключ 𝑥 есть в дереве выведите «true», если нет «false»;
next 𝑥 — выведите минимальный элемент в дереве, строго больший 𝑥, или «none» если такого нет;
prev 𝑥 — выведите максимальный элемент в дереве, строго меньший 𝑥, или «none» если такого нет.
В дерево помещаются и извлекаются только целые числа, не превышающие по модулю 10^9.
Выходные данные
Выведите последовательно результат выполнения всех операций exists, next, prev.
Следуйте формату выходного файла из примера.

Пример
входные данные
insert 2
insert 5
insert 3
exists 2
exists 4
next 4
prev 4
delete 5
next 4
prev 4
выходные данные
true
false
5
3
none
3

Реализуйте Декартово дерево для знакомой задачи
"""
import sys
from random import randint


UNICODE = "utf-8"
N_OPERATIONS = 100000


class Node:
    def __init__(self, key=None, priority=None):
        self.key = key
        self.priority = priority
        self.left = None
        self.right = None


class Treap:
    def __init__(self):
        self.root = None

    def split(self, v, x):
        if v is None:
            return None, None
        if v.key > x:
            t_1, t_2 = self.split(v.left, x)
            v.left = t_2
            return t_1, v
        else:
            t_1, t_2 = self.split(v.right, x)
            v.right = t_1
            return v, t_2

    def merge(self, t_1, t_2):
        if t_1 is None:
            return t_2
        if t_2 is None:
            return t_1
        if t_1.priority > t_2.priority:
            t_1.right = self.merge(t_1.right, t_2)
            return t_1
        else:
            t_2.left = self.merge(t_1, t_2.left)
            return t_2

    def insert(self, v, x):
        priority = randint(0, N_OPERATIONS)
        if v is None:
            return Node(x, priority)
        else:
            t_1, t_2 = self.split(v, x)
            t_1 = self.merge(t_1, Node(x, priority))
            v = self.merge(t_1, t_2)
            return v

    def exists(self, v, x):
        if v is None:
            return 'false'
        elif v.key == x:
            return 'true'
        elif v.key > x:
            return self.exists(v.left, x)
        else:
            return self.exists(v.right, x)

    def delete(self, v, x):
        t_1, t_2 = self.split(v, x)
        t_11, t_12 = self.split(t_1, x - 1)
        v = self.merge(t_11, t_2)
        return v

    def get_next(self, v, x, type='next'):
        res = None
        if type == 'next':
            t_1, t_2 = self.split(v, x)
            if t_2 is None:
                return v, 'none'
            res = t_2
            while res.left:
                res = res.left
        elif type == 'prev':
            t_1, t_2 = self.split(v, x - 1)
            if t_1 is None:
                return v, 'none'
            res = t_1
            while res.right:
                res = res.right
        v = self.merge(t_1, t_2)
        if res:
            return v, str(res.key)
        else:
            return v, 'none'


def main():
    data = sys.stdin.buffer.read().splitlines()
    tree = Treap()
    for operation in data:
        args = operation.decode(UNICODE).split()
        args[1] = int(args[1])
        if args[0] == 'insert':
            tree.root = tree.insert(tree.root, args[1])
        elif args[0] == 'delete':
            tree.root = tree.delete(tree.root, args[1])
        elif args[0] == 'exists':
            print(str(tree.exists(tree.root, args[1])))
        elif args[0] == 'next':
            tree.root, res = tree.get_next(tree.root, args[1], 'next')
            print(res)
        elif args[0] == 'prev':
            tree.root, res = tree.get_next(tree.root, args[1], 'prev')
            print(res)


if __name__ == "__main__":
    main()
