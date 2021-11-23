"""
A. Простое двоичное дерево поиска

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте просто двоичное дерево поиска.

Входные данные
Входной файл содержит описание операций с деревом, их количество не превышает 100.
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

Поиграться, реализовав обычное дерево поиска
"""
import sys


SEPARATOR = "\n"
UNICODE = "utf-8"


class Node:
    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None


class SimpleBinarySearchTree:
    def __init__(self):
        self.root = None

    def exists(self, v, x):
        if v is None:
            return 'false'
        elif v.key == x:
            return 'true'
        elif v.key > x:
            return self.exists(v.left, x)
        else:
            return self.exists(v.right, x)

    def insert(self, v, x):
        if v is None:
            return Node(x)
        if v.key > x:
            v.left = self.insert(v.left, x)
        elif v.key < x:
            v.right = self.insert(v.right, x)
        return v

    def delete(self, v, x):
        if v is None:
            return None
        if v.key > x:
            v.left = self.delete(v.left, x)
        elif v.key < x:
            v.right = self.delete(v.right, x)
        else:
            if v.left is None:
                v = v.right
            elif v.right is None:
                v = v.left
            else:
                v.key = self.find_max(v.left).key
                v.left = self.delete(v.left, v.key)
        return v

    @staticmethod
    def find_max(v):
        while v.right is not None:
            v = v.right
        return v

    def get_next(self, x, type='next'):
        v = self.root
        res = None
        while v is not None:
            if type == 'next':
                if v.key > x:
                    res = v
                    v = v.left
                else:
                    v = v.right
            else:
                if v.key < x:
                    res = v
                    v = v.right
                else:
                    v = v.left
        if res:
            return str(res.key)
        else:
            return 'none'


def main():
    data = sys.stdin.buffer.read().splitlines()
    results = []

    tree = SimpleBinarySearchTree()

    for operation in data:
        args = operation.decode(UNICODE).split()
        args[1] = int(args[1])
        if args[0] == 'insert':
            tree.root = tree.insert(tree.root, args[1])
        elif args[0] == 'delete':
            tree.root = tree.delete(tree.root, args[1])
        elif args[0] == 'exists':
            results.append(str(tree.exists(tree.root, args[1])))
        elif args[0] == 'next':
            results.append(str(tree.get_next(args[1], 'next')))
        elif args[0] == 'prev':
            results.append(str(tree.get_next(args[1], 'prev')))

    encoded_array = (SEPARATOR.join(results)).encode(UNICODE)
    sys.stdout.buffer.write(encoded_array)


if __name__ == "__main__":
    main()












