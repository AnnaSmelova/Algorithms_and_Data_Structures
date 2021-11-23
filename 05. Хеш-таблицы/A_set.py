"""
A. Set

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте множество с использованием хеш таблицы.

Входные данные
Входной файл содержит описание операций, их количество не превышает 1000000(10^6).
В каждой строке находится одна из следующих операций:
insert 𝑥 — добавить элемент 𝑥 в множество. Если элемент уже есть в множестве, то ничего делать не надо.
delete 𝑥 — удалить элемент 𝑥. Если элемента 𝑥 нет, то ничего делать не надо.
exists 𝑥 — если ключ 𝑥 есть в множестве выведите «true», если нет «false».
В множество помещаются и извлекаются только целые числа, не превышающие по модулю 10^9.

Выходные данные
Выведите последовательно результат выполнения всех операций exists. Следуйте формату выходного файла из примера.

Пример
входные данные
insert 2
insert 5
insert 3
exists 2
exists 4
insert 2
delete 2
exists 2
выходные данные
true
false
false

Требуется реализовать Set на самописной Хеш-таблице с использованием открытой адресации.
"""
import sys
from random import choice

SEPARATOR = "\n"
UNICODE = "utf-8"
MAX_SIZE = 10 ** 6
RIP_VAL = 10 ** 9 + 7
P_VALS = [1073676287, 2971215073]
A_VALS = list(range(1, 19, 2))


class CustomSet:
    def __init__(self):
        self.size = 0
        self.rip_size = 0
        self.capacity = 2
        self.elements = [None] * self.capacity
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)

    def get_hash_val(self, value):
        return ((value * self.a) % self.p) % self.capacity

    def do_rehash_and_resize(self):
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)
        old_elements = self.elements[:]
        if self.size + 1 >= self.capacity // 2 and self.capacity < 2 * MAX_SIZE:
            self.capacity = self.capacity * 2
        elif self.size < self.capacity // 8 and self.capacity > 8:
            self.capacity = self.capacity // 2
        self.elements = [None] * self.capacity
        self.size = 0
        self.rip_size = 0
        for val in old_elements:
            if val is not None and val != RIP_VAL:
                self.insert(val, check=False)

    def insert(self, val, check=True):
        if self.exists(val) == 'false':
            hash_val = self.get_hash_val(val)
            while True:
                current_val = self.elements[hash_val]
                if current_val == val:
                    break
                elif current_val == RIP_VAL:
                    self.elements[hash_val] = val
                    self.size += 1
                    self.rip_size -= 1
                    break
                elif current_val is None:
                    self.elements[hash_val] = val
                    self.size += 1
                    break
                else:
                    hash_val = (hash_val + 1) % self.capacity

            if check and self.size + self.rip_size + 1 > self.capacity // 2:
                self.do_rehash_and_resize()

    def exists(self, val):
        hash_val = self.get_hash_val(val)
        while True:
            current_val = self.elements[hash_val]
            if current_val is None:
                return 'false'
            elif current_val == val:
                return 'true'
            else:
                hash_val = (hash_val + 1) % self.capacity

    def delete(self, val):
        hash_val = self.get_hash_val(val)
        while True:
            current_val = self.elements[hash_val]
            if current_val is None:
                break
            elif current_val == val:
                self.elements[hash_val] = RIP_VAL
                self.size -= 1
                self.rip_size += 1
                break
            else:
                hash_val = (hash_val + 1) % self.capacity


def main():
    custom_set = CustomSet()
    data = sys.stdin.buffer.read().splitlines()
    results = []
    for operation in data:
        args = operation.decode(UNICODE).split()
        if args[0] == 'insert':
            custom_set.insert(int(args[1]))
        elif args[0] == 'exists':
            results.append(custom_set.exists(int(args[1])))
        elif args[0] == 'delete':
            custom_set.delete(int(args[1]))

    encoded_array = (SEPARATOR.join(results)).encode(UNICODE)
    sys.stdout.buffer.write(encoded_array)


if __name__ == "__main__":
    main()
