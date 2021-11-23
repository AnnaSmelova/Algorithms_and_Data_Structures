"""
B. Постфиксная запись

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

В постфиксной записи (или обратной польской записи) операция записывается после двух операндов.
Например, сумма двух чисел A и B записывается как A B +.
Запись B C + D * обозначает привычное нам (B + C) * D,
а запись A B C + D * + означает A + (B + C) * D.
Достоинство постфиксной записи в том, что она не требует скобок и дополнительных соглашений о приоритете
операторов для своего чтения.

Дано выражение в обратной польской записи. Определите его значение.

Входные данные
В единственной строке записано выражение в постфиксной записи, содержащее однозначные числа и операции +, -, *.
Строка содержит не более 100 чисел и операций.
Выходные данные
Необходимо вывести значение записанного выражения.
Гарантируется, что результат выражения, а также результаты всех промежуточных вычислений по модулю меньше 2^31.

Пример
входные данные
8 9 + 1 7 - *
выходные данные
-102

Тут тоже нужен стек, но в этот раз можно и нужно реализовать его на самописном саморасширяющемся массиве.
"""
import sys


class EnlargingArray:
    def __init__(self):
        self.size = 0
        self.capacity = 2
        self.elements = [0] * self.capacity

    def get_el_by_index(self, ind):
        if ind < 0 or ind >= self.size:
            return None
        return self.elements[ind]

    def update_capacity(self, upd_type='more'):
        if upd_type == 'less':
            self.capacity //= 2
        else:
            self.capacity *= 2
        new_elements = [0] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]
        self.elements = new_elements

    def add_val(self, val):
        if self.size + 1 > self.capacity:
            self.update_capacity('more')
        self.elements[self.size] = val
        self.size += 1

    def pop(self):
        if self.size:
            pop_el = self.get_el_by_index(self.size - 1)
            self.elements[self.size - 1] = 0
            self.size -= 1
        else:
            return None

        if self.size <= self.capacity // 4 and self.capacity > 2:
            self.update_capacity('less')

        return pop_el


class Stack(EnlargingArray):
    @staticmethod
    def check_is_val_num(val):
        try:
            int(val)
            return True
        except ValueError:
            return False

    def add_val(self, val):
        if self.check_is_val_num(val):
            super().add_val(int(val))
        else:
            first_el = self.pop()
            second_el = self.pop()
            if val == '+':
                super().add_val(first_el + second_el)
            elif val == '-':
                super().add_val((second_el - first_el))
            else:
                super().add_val(first_el * second_el)


def main():
    stack = Stack()
    postfix = sys.stdin.readline().split()
    for el in postfix:
        stack.add_val(el)
    print(stack.pop())


if __name__ == "__main__":
    main()
