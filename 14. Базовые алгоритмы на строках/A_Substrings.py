"""
A. Сравнения подстрок

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дана строка s. Ответьте на m запросов вида: равны ли подстроки s[a..b] и s[c..d].

Входные данные
В первой строке ввода записана строка s (1≤|s|≤10^5).

Во второй строке записано целое число m — количество запросов (0≤m≤10^5).

В следующих m строках четверки чисел a,b,c,d (1≤a≤b≤|s|,1≤c≤d≤|s|).

Выходные данные
Выведите m строк. Выведите Yes, если подстроки совпадают, и No иначе.

Пример
входные данные
trololo
3
1 7 1 7
3 5 5 7
1 1 1 5
выходные данные
Yes
Yes
No

Хорошая тренировочная задачка для полиномиальных Хешей
"""
import sys


FIRST_LETTER = ord('a')
UNICODE = "utf-8"
P = 29
M = 1073676287


class String:
    def __init__(self, string):
        self.string = string
        self.size = len(self.string)
        self.hash_value = [0 for _ in range(self.size)]
        self.hash_value[0] = ord(self.string[0]) - FIRST_LETTER + 1
        self.hash_power = [0 for _ in range(self.size)]
        self.hash_power[0] = 1
        for i in range(1, self.size):
            self.hash_value[i] = (self.hash_value[i - 1] * P + ord(self.string[i]) - FIRST_LETTER + 1) % M
            self.hash_power[i] = (self.hash_power[i - 1] * P) % M

    def get_hash(self, start, end):
        if 0 == start:
            return self.hash_value[end]
        return (self.hash_value[end] - (self.hash_value[start - 1] * self.hash_power[end - start + 1]) % M + M) % M

    def compare_substrings(self, start_1, end_1, start_2, end_2):
        if end_1 - start_1 == end_2 - start_2:
            if self.get_hash(start_1, end_1) == self.get_hash(start_2, end_2):
                return 'Yes'
        return 'No'


def main():
    data = sys.stdin.buffer.read().splitlines()
    s = data[0].decode(UNICODE)
    string = String(s)
    m = int(data[1])
    for row in data[2:]:
        a, b, c, d = map(int, row.split())
        print(string.compare_substrings(a - 1, b - 1, c - 1, d - 1))


if __name__ == "__main__":
    main()
