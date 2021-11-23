"""
C. Реализуйте очередь

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Для каждой операции изъятия элемента выведите ее результат.

На вход программе подаются строки, содержащие команды. Каждая строка содержит одну команду.
Команда — это либо "+ N", либо "-". Команда "+ N" означает добавление в очередь числа 𝑁, по модулю не превышающего 10^9.
Команда "-" означает изъятие элемента из очереди.

Входные данные
В первой строке содержится количество команд — 𝑚 (1⩽𝑚⩽10^5).
В последующих строках содержатся команды, по одной в каждой строке.
Выходные данные
Выведите числа, которые удаляются из очереди, по одному в каждой строке.
Гарантируется, что изъятий из пустой очереди не производится.

Пример
входные данные
4
+ 1
+ 10
-
-
выходные данные
1
10

Казалось бы, просто очередь, но чтобы быть асом саморасширения тут требуется реализовать
очередь на самописном саморасширяющемся циклическом массиве!
"""
import sys


class Queue:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.capacity = 2
        self.elements = [0] * self.capacity

    def get_size(self):
        return (self.end - self.begin + self.capacity) % self.capacity

    def get_el_by_index(self, ind):
        return self.elements[ind]

    def update_capacity(self, upd_type='more'):
        if upd_type == 'less':
            new_elements = [0] * (self.capacity // 2)
        else:
            new_elements = [0] * (self.capacity * 2)
        size = self.get_size()
        if self.end >= self.begin:
            for i in range(self.begin, self.end):
                new_elements[i - self.begin] = self.elements[i]
        else:
            for i in range(self.begin, self.capacity):
                new_elements[i - self.begin] = self.elements[i]
            for j in range(self.end):
                new_elements[self.capacity + j] = self.elements[j]
        if upd_type == 'less':
            self.capacity //= 2
        else:
            self.capacity *= 2
        self.elements = new_elements
        self.begin = 0
        self.end = size

    def get_next_ind(self, curr_ind):
        return (curr_ind + 1) % self.capacity

    def add_val(self, val):
        size = self.get_size()
        if size + 1 >= self.capacity:
            self.update_capacity('more')
        next_ind = self.get_next_ind(self.end)
        self.elements[self.end] = val
        self.end = next_ind

    def pop(self):
        if self.get_next_ind(self.begin) != self.end:
            pop_el = self.get_el_by_index(self.begin)
            self.elements[self.begin] = 0
            self.begin = self.get_next_ind(self.begin)
        else:
            pop_el = self.get_el_by_index(self.begin)
            self.elements[self.begin] = 0
            self.begin = 0
            self.end = 0

        if self.get_size() <= self.capacity // 4 and self.capacity > 2:
            self.update_capacity('less')

        return pop_el


def main():
    m = int(sys.stdin.readline())
    queue = Queue()
    for _ in range(m):
        operation = sys.stdin.readline().split()
        if operation[0] == '+':
            queue.add_val(int(operation[1]))
        else:
            print(queue.pop())


if __name__ == "__main__":
    main()
