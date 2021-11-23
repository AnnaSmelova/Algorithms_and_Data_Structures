"""
D. И снова сумма

ограничение по времени на тест: 3 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте структуру данных, которая поддерживает множество S целых чисел,
с котором разрешается производить следующие операции:

add(i) — добавить в множество S число i (если он там уже есть, то множество не меняется);
sum(l,r) — вывести сумму всех элементов x из S, которые удовлетворяют неравенству l≤x≤r.

Входные данные
Исходно множество S пусто. Первая строка входного файла содержит n — количество операций (1≤n≤300000).
Следующие n строк содержат операции. Каждая операция имеет вид либо «+ i», либо «? l r».
Операция «? l r» задает запрос sum(l,r).

Если операция «+ i» идет во входном файле в начале или после другой операции «+», то она задает операцию add(i).
Если же она идет после запроса «?», и результат этого запроса был y, то выполняется операция add((i+y) mod 10^9).

Во всех запросах и операциях добавления параметры лежат в интервале от 0 до 10^9.

Выходные данные
Для каждого запроса выведите одно число — ответ на запрос.

Пример
входные данные
6
+ 1
+ 3
+ 3
? 2 4
+ 1
? 2 4
выходные данные
3
7

Тут уже никаких подсказок, нужно хранить много информации и подумать, хороший тамада и задачи интересные.
Еще раз напомню, что Декартово дерево нельзя (splay на самом деле тоже)
"""
import sys


MOD = 10 ** 9


class Node:
    def __init__(self, key=None):
        self.key = key
        self.height = 1
        self.balance = 0
        self.left = None
        self.right = None
        self.sum = key
        self.lb = key
        self.rb = key


class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def fix(v):
        left_height = 0 if v.left is None else v.left.height
        right_height = 0 if v.right is None else v.right.height
        v.height = max(left_height, right_height) + 1
        v.balance = left_height - right_height
        v.lb = v.key if v.left is None else v.left.lb
        v.rb = v.key if v.right is None else v.right.rb
        left_sum = 0 if v.left is None else v.left.sum
        right_sum = 0 if v.right is None else v.right.sum
        v.sum = left_sum + right_sum + v.key
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

    def insert(self, v, x):
        if v is None:
            return Node(x)
        if v.key > x:
            v.left = self.insert(v.left, x)
        elif v.key < x:
            v.right = self.insert(v.right, x)
        self.fix(v)
        return self.balance(v)

    def get_sum(self, v, lb, rb):
        curr_sum = 0
        if v is None:
            return 0
        if lb <= v.lb and v.rb <= rb:
            curr_sum += v.sum
        elif (v.lb <= lb <= v.rb) or (v.lb <= rb <= v.rb):
            curr_sum += self.get_sum(v.left, lb, rb)
            curr_sum += self.get_sum(v.right, lb, rb)
            if lb <= v.key <= rb:
                curr_sum += v.key
        return curr_sum


def main():
    n = int(input())
    tree = AVLTree()
    prev_operation = '+'
    prev_result = 0
    for i in range(n):
        args = sys.stdin.readline().split(' ')
        if args[0] == '?':
            prev_operation = '?'
            prev_result = tree.get_sum(tree.root, int(args[1]), int(args[2]))
            print(prev_result)
        elif args[0] == '+':
            x = ((prev_result + int(args[1])) % MOD)
            tree.root = tree.insert(tree.root, x)
            prev_operation = '+'
            prev_result = 0


if __name__ == "__main__":
    main()
