"""
B. Неявный ключ

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Научитесь быстро делать две операции с массивом:
add i x — добавить после i-го элемента x (0≤i≤n)
del i — удалить i-й элемент (1≤i≤n)

Входные данные
На первой строке n0 и m (1≤n0,m≤10^5) — длина исходного массива и количество запросов.
На второй строке n0 целых чисел от 0 до 10^9-1 — исходный массив.
Далее m строк, содержащие запросы.
Гарантируется, что запросы корректны: например, если просят удалить i-й элемент, он точно есть.

Выходные данные
Выведите конечное состояние массива. На первой строке количество элементов, на второй строке сам массив.

Пример
входные данные
3 4
1 2 3
del 3
add 0 9
add 3 8
del 2
выходные данные
3
9 2 8

Тренируемся писать неявный ключ
"""
import sys
from random import randint


UNICODE = "utf-8"
N_OPERATIONS = 100000


class Node:
    def __init__(self, value=None, priority=None):
        self.value = value
        self.priority = priority
        self.nodes_cnt = 1
        self.left = None
        self.right = None

    def get_left_nodes_cnt(self):
        if self.left is None:
            return 0
        else:
            return self.left.nodes_cnt

    def get_right_nodes_cnt(self):
        if self.right is None:
            return 0
        else:
            return self.right.nodes_cnt


class Treap:
    def __init__(self):
        self.root = None

    @staticmethod
    def fix(v):
        v.nodes_cnt = v.get_left_nodes_cnt() + v.get_right_nodes_cnt() + 1
        return

    def split(self, v, x):
        if v is None:
            return None, None
        if v.get_left_nodes_cnt() > x:
            t_1, t_2 = self.split(v.left, x)
            v.left = t_2
            self.fix(v)
            return t_1, v
        else:
            t_1, t_2 = self.split(v.right, x - v.get_left_nodes_cnt() - 1)
            v.right = t_1
            self.fix(v)
            return v, t_2

    def merge(self, t_1, t_2):
        if t_1 is None:
            return t_2
        if t_2 is None:
            return t_1
        if t_1.priority > t_2.priority:
            t_1.right = self.merge(t_1.right, t_2)
            self.fix(t_1)
            return t_1
        else:
            t_2.left = self.merge(t_1, t_2.left)
            self.fix(t_2)
            return t_2

    def insert(self, v, i, x):
        priority = randint(0, N_OPERATIONS)
        if v is None:
            return Node(x, priority)
        else:
            t_1, t_2 = self.split(v, i)
            t_1 = self.merge(t_1, Node(x, priority))
            v = self.merge(t_1, t_2)
            return v

    def delete(self, v, i):
        t_1, t_2 = self.split(v, i)
        t_11, t_12 = self.split(t_1, i - 1)
        v = self.merge(t_11, t_2)
        return v

    def print_array(self, v):
        if v:
            self.print_array(v.left)
            print(v.value, end=' ')
            self.print_array(v.right)


def main():
    data = sys.stdin.buffer.read().splitlines()
    n_0, m = map(int, data[0].split())
    a = list(map(int, data[1].split()))
    tree = Treap()
    for i in range(n_0):
        tree.root = tree.insert(tree.root, i, a[i])
    for operation in data[2:]:
        args = operation.decode(UNICODE).split()
        if args[0] == 'add':
            tree.root = tree.insert(tree.root, int(args[1]) - 1, int(args[2]))
        elif args[0] == 'del':
            tree.root = tree.delete(tree.root, int(args[1]) - 1)
    if tree.root is None:
        print(0)
    else:
        print(tree.root.nodes_cnt)
        tree.print_array(tree.root)


if __name__ == "__main__":
    main()
