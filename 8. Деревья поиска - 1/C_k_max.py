"""
C. 𝐾 -й максимум

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 512 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Напишите программу, реализующую структуру данных, позволяющую добавлять и удалять элементы,
а также находить 𝑘-й максимум.

Входные данные
Первая строка входного файла содержит натуральное число 𝑛 — количество команд (𝑛≤100000).
Последующие 𝑛 строк содержат по одной команде каждая. Команда записывается в виде двух чисел
𝑐_𝑖 и 𝑘_𝑖 — тип и аргумент команды соответственно (|𝑘_𝑖|≤10^9). Поддерживаемые команды:

+1 (или просто 1): Добавить элемент с ключом 𝑘𝑖.
 0: Найти и вывести 𝑘𝑖-й максимум.
-1: Удалить элемент с ключом 𝑘𝑖.

Гарантируется, что в процессе работы в структуре не требуется хранить элементы с равными ключами или удалять
несуществующие элементы. Также гарантируется, что при запросе 𝑘_𝑖-го максимума, он существует.

Выходные данные
Для каждой команды нулевого типа в выходной файл должна быть выведена строка,
содержащая единственное число — 𝑘𝑖-й максимум.

Пример
входные данные
11
+1 5
+1 3
+1 7
0 1
0 2
0 3
-1 5
+1 10
0 1
0 2
0 3
выходные данные
7
5
3
10
7
3

Тут надо вспомнить, что в вершине можно хранить вспомогательную информацию, например, число вершин в поддереве
"""
import sys


class Node:
    def __init__(self, key=None):
        self.key = key
        self.height = 1
        self.balance = 0
        self.left = None
        self.right = None
        self.nodes_cnt = 1


class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def fix(v):
        left_height = 0 if v.left is None else v.left.height
        right_height = 0 if v.right is None else v.right.height
        v.height = max(left_height, right_height) + 1
        left_nodes_cnt = 0 if v.left is None else v.left.nodes_cnt
        right_nodes_cnt = 0 if v.right is None else v.right.nodes_cnt
        v.nodes_cnt = left_nodes_cnt + right_nodes_cnt + 1
        v.balance = left_height - right_height
        return

    def small_rotate(self, p, dir='left'):
        if dir == 'left':
            q = p.right
            p.right = q.left
            q.left = p
        else:
            q = p.left
            p.left = q.right
            q.right = p
        self.fix(p)
        self.fix(q)
        return q

    def big_rotate(self, p, dir='left'):
        if dir == 'left':
            p.right = self.small_rotate(p.right, 'right')
        else:
            p.left = self.small_rotate(p.left, 'left')
        return self.small_rotate(p, dir)

    def balance(self, v):
        if v is None:
            return None
        if v.balance == -2 and v.right.balance <= 0:
            v = self.small_rotate(v, 'left')
        elif v.balance == -2 and v.right.balance > 0:
            v = self.big_rotate(v, 'left')
        elif v.balance == 2 and v.left.balance >= 0:
            v = self.small_rotate(v, 'right')
        elif v.balance == 2 and v.left.balance < 0:
            v = self.big_rotate(v, 'right')
        return v

    @staticmethod
    def get_height(v):
        if v is None:
            return 0
        return v.height

    def get_balance(self, v):
        if v is None:
            return 0
        return self.get_height(v.left) - self.get_height(v.right)

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
            v.nodes_cnt += 1
        elif v.key < x:
            v.right = self.insert(v.right, x)
            v.nodes_cnt += 1
        self.fix(v)
        return self.balance(v)

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
        if v is not None:
            self.fix(v)
        return self.balance(v)

    @staticmethod
    def find_max(v):
        while v.right is not None:
            v = v.right
        return v

    def get_k_max(self, v, k):
        if v is None:
            return None
        pos = v.nodes_cnt - k + 1
        left_nodes_cnt = 0 if v.left is None else v.left.nodes_cnt
        right_nodes_cnt = v.nodes_cnt - left_nodes_cnt - 1
        if pos == left_nodes_cnt + 1:
            result = v.key
        elif pos <= left_nodes_cnt:
            result = self.get_k_max(v.left, k - right_nodes_cnt - 1)
        else:
            result = self.get_k_max(v.right, k)
        return result


def main():
    n = int(input())
    tree = AVLTree()
    for i in range(n):
        args = sys.stdin.readline().split(' ')
        args[1] = int(args[1])
        if args[0] == '+1' or args[0] == '1':
            tree.root = tree.insert(tree.root, args[1])
        elif args[0] == '-1':
            tree.root = tree.delete(tree.root, args[1])
        elif args[0] == '0':
            print(str(tree.get_k_max(tree.root, args[1])))


if __name__ == "__main__":
    main()
