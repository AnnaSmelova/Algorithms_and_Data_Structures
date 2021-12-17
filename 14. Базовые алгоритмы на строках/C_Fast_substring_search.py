"""
C. Быстрый поиск подстроки в строке

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Даны строки p и t. Требуется найти все вхождения строки p в строку t в качестве подстроки.

Входные данные
Первая строка входного файла содержит p, вторая — t (1≤|p|,|t|≤10^6).
Строки состоят из букв латинского алфавита.

Выходные данные
В первой строке выведите количество вхождений строки p в строку t.
Во второй строке выведите в возрастающем порядке номера символов строки t, с которых начинаются вхождения p.
Символы нумеруются с единицы.

Пример
входные данные
aba
abaCaba
выходные данные
2
1 5

Префикс функция + КМП
"""
import sys


UNICODE = "utf-8"
SEPARATOR = "#"


class String:
    def __init__(self, string_p, string_t):
        self.len_p = len(string_p)
        self.string = string_p + SEPARATOR + string_t
        self.size = self.len_p + 1 + len(string_t)
        self.p_function = [0 for _ in range(self.size)]

    def get_p_function(self):
        for i in range(1, self.size):
            k = self.p_function[i - 1]
            while k > 0 and self.string[i] != self.string[k]:
                k = self.p_function[k - 1]
            if self.string[i] == self.string[k]:
                k += 1
            self.p_function[i] = k
        return self.p_function

    def knuth_morris_pratt(self):
        result = []
        self.p_function = self.get_p_function()
        for i in range(self.size):
            if self.p_function[i] == self.len_p:
                result.append(str(i + 1 - self.len_p * 2))
        return result


def main():
    data = sys.stdin.buffer.read().splitlines()
    p = data[0].decode(UNICODE)
    t = data[1].decode(UNICODE)
    string = String(p, t)
    result = string.knuth_morris_pratt()
    print(len(result))
    print(' '.join(result))


if __name__ == "__main__":
    main()
