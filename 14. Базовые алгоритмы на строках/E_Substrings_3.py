"""
E. Подстроки-3

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Даны K строк из маленьких латинских букв.
Требуется найти их наибольшую общую подстроку.

Входные данные
В первой строке число K (1≤K≤10).

В следующих K строках — собственно K строк (длины строк от 1 до 10000).

Выходные данные
Наибольшая общая подстрока.

Пример
входные данные
3
abacaba
mycabarchive
acabistrue

выходные данные
cab

Слышал, что в свое время такую задачу давали на собеседованиях, можно написать суффиксный массив,
а можно с помощью Хешей и чего-то за логарифм сделать по красоте)
"""
import sys
from collections import defaultdict

UNICODE = "utf-8"
FIRST_LETTER = ord('a')
P = 29
M = 1073676287


class String:
    def __init__(self, string):
        self.string = string
        self.size = len(self.string)
        if self.size > 0:
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


class BagOfStrings:
    def __init__(self, k, strings):
        self.strings = list(map(String, strings))
        self.size = k
        self.common_substring = None

    def get_substring(self, med):
        hashes_set = set()
        substr_hashes = defaultdict(list)
        for i in range(self.size):
            current_string = self.strings[i]
            for j in range(current_string.size - med + 1):
                substr_hashes[current_string].append(current_string.get_hash(j, j + med - 1))
            if i == 0:
                hashes_set = set(substr_hashes[current_string])
            else:
                hashes_set = hashes_set.intersection((set(substr_hashes[current_string])))
                if len(hashes_set) == 0:
                    return None
        last_string = self.strings[-1]
        for m in range(len(substr_hashes[last_string])):
            if substr_hashes[last_string][m] in hashes_set:
                return last_string.string[m:m + med]

    def get_common_substring(self):
        if self.size == 1:
            self.common_substring = self.strings[0].string
            return self.common_substring
        start = 1
        end = 1 + self.strings[0].size
        while start < end:
            med = (start + end) // 2
            common_substring = self.get_substring(med)
            if common_substring is None:
                end = med
            else:
                start = med + 1
                self.common_substring = common_substring
        return self.common_substring


def main():
    data = sys.stdin.buffer.read().splitlines()
    k = int(data[0])
    string_list = [None for _ in range(k)]
    for ind, row in enumerate(data[1:]):
        string = row.decode(UNICODE)
        string_list[ind] = string
    string_list = sorted(string_list, key=len)
    bag = BagOfStrings(k, string_list)
    if bag.get_common_substring() is None:
        print('')
    else:
        print(bag.common_substring)


if __name__ == "__main__":
    main()
