"""
A. Минимум на стеке

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Вам требуется реализовать структуру данных, выполняющую следующие операции:

Добавить элемент 𝑥 в конец структуры.
Удалить последний элемент из структуры.
Выдать минимальный элемент в структуре.

Входные данные
В первой строке входного файла задано одно целое число 𝑛 — количество операций (1≤𝑛≤10^6).
В следующих 𝑛 строках заданы сами операции.
В 𝑖–ой строке число 𝑡_𝑖 — тип операции (1, если операция добавления. 2, если операция удаления.
3, если операция минимума). Если задана операция добавления, то через пробел записано целое число 𝑥 — элемент,
который следует добавить в структуру (−10^9≤𝑥≤10^9).
Гарантируется, что перед каждой операцией удаления или нахождения минимума структура не пуста.

Выходные данные
Для каждой операции нахождения минимума выведите одно число — минимальный элемент в структуре.
Ответы разделяйте переводом строки.

Пример
входные данные
8
1 2
1 3
1 -3
3
2
3
2
3
выходные данные
-3
2
2

Требуется использовать самописный стек на связном списке (тоже самописном)
"""
import sys


class Node:
    def __init__(self, val, min_val=None, prev_node=None):
        self.val = val
        if min_val:
            self.min_val = min(val, min_val)
        else:
            self.min_val = val
        self.prev_node = prev_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_val(self, val):
        if self.size == 0:
            new_node = Node(val)
            self.head = new_node
            self.tail = new_node
        else:
            new_node = Node(val, self.tail.min_val, self.tail)
            self.tail = new_node
        self.size += 1

    def erase_tail(self):
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev_node
        self.size -= 1


class Stack(LinkedList):
    def get_min_val(self):
        return self.tail.min_val


def main():
    n = int(sys.stdin.readline())
    stack = Stack()
    for _ in range(n):
        operation = sys.stdin.readline().split()
        if operation[0] == '1':
            stack.insert_val(int(operation[1]))
        elif operation[0] == '2':
            stack.erase_tail()
        else:
            print(stack.get_min_val())


if __name__ == "__main__":
    main()
