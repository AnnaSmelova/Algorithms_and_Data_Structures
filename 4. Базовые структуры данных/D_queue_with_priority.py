"""
D. Приоритетная очередь – 2

ограничение по времени на тест: 3 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте приоритетную очередь. Ваша очередь должна поддерживать следующие операции: добавить элемент,
извлечь минимальный элемент, уменьшить элемент, добавленный во время одной из операций.

Если какой-нибудь decrease-key уменьшает уже удаленный элемент, то ничего делать не нужно.

Все операции нумеруются по порядку, начиная с 1.

Входные данные
Содержится описание операций со очередью.
В очередь помещаются и извлекаются только целые числа, не превышающие 10^9 по абсолютной величине.

Гарантируется, что для любого decrease-key x v из входных данных операция под номером 𝑥 является push.

Выходные данные
Выведите последовательно результат выполнения всех операций extract-min из двух целых чисел:
значение элемента и номер операции push, при котором этот элемент был добавлен.
Если в очереди есть несколько минимальных элементов, выведите любой.
Если перед очередной операцией extract-min очередь пуста, выведите звездочку.

Пример
входные данные
push 3
push 4
push 2
extract-min
decrease-key 2 1
extract-min
extract-min
extract-min
выходные данные
2 3
1 2
3 1
*

Используем самописную кучу, которую можно реализовать на стандартном саморасширяющемся массиве.
Если очень хочется, можно даже обычный массив использовать ибо с саморасширением уже все должно быть понятно:)
"""
import sys


class EnlargingArray:
    def __init__(self):
        self.size = 0
        self.capacity = 2
        self.elements = [None] * self.capacity
        self.steps = [None] * self.capacity

    def get_size(self):
        return self.size

    def get_el_by_index(self, ind):
        if ind < 0 or ind >= self.size:
            return None, None
        return self.elements[ind], self.steps[ind]

    def update_capacity(self, upd_type='more'):
        if upd_type == 'less':
            self.capacity //= 2
        else:
            self.capacity *= 2
        new_elements = [None] * self.capacity
        new_steps = [None] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]
            new_steps[i] = self.steps[i]
        self.elements = new_elements
        self.steps = new_steps

    def add_val(self, val, step):
        if self.size + 1 > self.capacity:
            self.update_capacity('more')
        self.elements[self.size] = val
        self.steps[self.size] = step
        self.size += 1

    def pop(self):
        if self.size:
            pop_el, pop_step = self.get_el_by_index(self.size - 1)
            self.elements[self.size - 1] = None
            self.steps[self.size - 1] = None
            self.size -= 1
        else:
            return None, None

        if self.size <= self.capacity // 4 and self.capacity > 2:
            self.update_capacity('less')

        return pop_el, pop_step


class Heap(EnlargingArray):
    def __init__(self):
        super().__init__()
        self.last_step = 0

    def sift_up(self, ind):
        while ind > 0 and self.elements[ind] <= self.elements[(ind - 1) // 2]:
            self.elements[ind], self.elements[(ind - 1) // 2] = self.elements[(ind - 1) // 2], self.elements[ind]
            self.steps[ind], self.steps[(ind - 1) // 2] = self.steps[(ind - 1) // 2], self.steps[ind]
            ind = (ind - 1) // 2

    def sift_down(self, ind):
        while 2 * ind + 1 < self.size:
            curr_el = self.elements[ind]
            left_child = self.elements[2 * ind + 1]
            if 2 * ind + 2 == self.size:
                right_child = left_child + 1
            else:
                right_child = self.elements[2 * ind + 2]
            if left_child < right_child and left_child < curr_el:
                self.elements[ind], self.elements[2 * ind + 1] = self.elements[2 * ind + 1], self.elements[ind]
                self.steps[ind], self.steps[2 * ind + 1] = self.steps[2 * ind + 1], self.steps[ind]
                ind = 2 * ind + 1
            elif right_child <= left_child and right_child < curr_el:
                self.elements[ind], self.elements[2 * ind + 2] = self.elements[2 * ind + 2], self.elements[ind]
                self.steps[ind], self.steps[2 * ind + 2] = self.steps[2 * ind + 2], self.steps[ind]
                ind = 2 * ind + 2
            else:
                break

    def extract_min(self):
        self.last_step += 1
        self.elements[0], self.elements[self.size - 1] = self.elements[self.size - 1], self.elements[0]
        self.steps[0], self.steps[self.size - 1] = self.steps[self.size - 1], self.steps[0]
        extracted_el, extracted_step = super().pop()
        self.sift_down(0)
        return extracted_el, extracted_step

    def insert_val(self, val):
        self.last_step += 1
        target_ind = self.size
        super().add_val(val, self.last_step)
        self.sift_up(target_ind)

    def decrease_val(self, step, val):
        self.last_step += 1
        i = 0
        while self.steps[i] != step and i < self.size:
            i += 1
        if i != self.size and self.steps[i] == step:
            self.elements[i] = val
            self.sift_up(i)


def main():
    operation = sys.stdin.readline().split()
    heap = Heap()
    while operation:
        if operation[0] == 'push':
            val = int(operation[1])
            heap.insert_val(val)
        elif operation[0] == 'decrease-key':
            step = int(operation[1])
            val = int(operation[2])
            heap.decrease_val(step, val)
        else:
            extract_res = heap.extract_min()
            if extract_res[0] != None:
                print(f'{extract_res[0]} {extract_res[1]}')
            else:
                print('*')
        operation = sys.stdin.readline().split()


if __name__ == "__main__":
    main()
