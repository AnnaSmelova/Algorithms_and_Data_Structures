"""
B. Z-функция

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Постройте Z-функцию для заданной строки s.

Входные данные
Первая строка входного файла содержит s (1≤|s|≤10^6).
Строка состоит из букв латинского алфавита.

Выходные данные
Выведите значения Z-функции строки s для индексов 2,3,...,|s|.

Пример 1
входные данные
aaaAAA
выходные данные
 2 1 0 0 0

Пример 2
входные данные
abacaba
выходные данные
 0 1 0 3 0 1

Хмм... А что тут нужно сделать?
"""
import sys


UNICODE = "utf-8"


class String:
    def __init__(self, string):
        self.string = string
        self.size = len(self.string)
        self.z_function = [0 for _ in range(self.size)]
        self.z_function[0] = ''

    def get_z_function(self):
        start, end = 0, 0
        for i in range(1, self.size):
            self.z_function[i] = max(0, min(end - i, self.z_function[i - start]))
            while (i + self.z_function[i] < self.size
                   and self.string[self.z_function[i]] == self.string[i + self.z_function[i]]):
                self.z_function[i] += 1
            if i + self.z_function[i] > end:
                start = i
                end = i + self.z_function[i]
        return self.z_function


def main():
    data = sys.stdin.buffer.read().splitlines()
    s = data[0].decode(UNICODE)
    string = String(s)
    print(' '.join(map(str, string.get_z_function())))


if __name__ == "__main__":
    main()
