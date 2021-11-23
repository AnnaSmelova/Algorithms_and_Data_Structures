"""
D. Развороты

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Вам дан массив a1=1,a2=2,...,an=n и последовательность операций:
переставить элементы с li по ri в обратном порядке.
Например, для массива 1,2,3,4,5, после операции (2,4) новый порядок будет 1,4,3,2,5.
А после применения операции (3,5) порядок элементов в массиве будет 1,4,5,2,3.

Выведите порядок элементов в массиве после выполнения всех операций.

Входные данные
В первой строке входного файла указаны числа n и m (2≤n≤100000, 1≤m≤100000)
— число элементов в массиве и число операций.
Следующие m строк содержат операции в виде двух целых чисел: li и ri (1≤li≤ri≤n).

Выходные данные
Выведите n целых чисел — порядок элементов в массиве после применения всех операций.

Пример
входные данные
5 3
2 4
3 5
2 2
выходные данные
1 4 5 2 3

Ну и на десерт самое прикольное, что умеет Декартово дерево
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
        self.reverse_flag = False

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

    @staticmethod
    def push(v):
        if v is not None and v.reverse_flag:
            v.reverse_flag = not v.reverse_flag
            v.left, v.right = v.right, v.left
            if v.left is not None:
                v.left.reverse_flag = not v.left.reverse_flag
            if v.right is not None:
                v.right.reverse_flag = not v.right.reverse_flag

    def split(self, v, x):
        if v is None:
            return None, None
        self.push(v)
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
        self.push(t_1)
        self.push(t_2)
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

    def print_array(self, v):
        if v:
            self.push(v)
            self.print_array(v.left)
            print(v.value, end=' ')
            self.print_array(v.right)

    def reverse(self, v, l_i, r_i):
        if l_i != r_i:
            t_1, t_2 = self.split(v, l_i - 1)
            t_21, t_22 = self.split(t_2, r_i - l_i)
            t_21.reverse_flag = not t_21.reverse_flag
            self.push(t_21)
            v = self.merge(t_1, self.merge(t_21, t_22))
        return v


def main():
    data = sys.stdin.buffer.read().splitlines()
    n, m = map(int, data[0].split())
    a = list(range(1, n + 1))
    tree = Treap()
    for i in range(n):
        tree.root = tree.insert(tree.root, i, a[i])
    for operation in data[1:]:
        args = operation.decode(UNICODE).split()
        l_i, r_i = map(int, args)
        tree.root = tree.reverse(tree.root, l_i - 1, r_i - 1)
    tree.print_array(tree.root)


if __name__ == "__main__":
    main()
