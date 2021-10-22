"""
D. MultiMap

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте множественное отображение с использованием хеш таблиц.

Входные данные
Входной файл содержит описание операций, их количество не превышает 100000(10^5).
В каждой строке находится одна из следующих операций:
put 𝑥 𝑦 — добавить пару (𝑥,𝑦). Если пара уже есть, то второй раз её добавлять не надо.
delete 𝑥 𝑦 — удалить пару (𝑥,𝑦). Если пары нет, то ничего делать не надо.
deleteall 𝑥 — удалить все пары с первым элементом 𝑥.
get 𝑥 — вывести количество пар с первым элементом 𝑥, а затем вторые элементы всех этих пар в произвольном порядке.
Ключи и значения — строки из латинских букв длинной не более 20 символов.
Выходные данные
Выведите последовательно результат выполнения всех операций get.
Следуйте формату выходного файла из примера. Гарантируется, что размер выходного файла не превысит 10 мегабайт.

Пример
входные данные
put a a
put a b
put a c
get a
delete a b
get a
deleteall a
get a
выходные данные
3 a b c
2 a c
0

Любой метод разрешения коллизий, какой вам нравится:)
"""
import sys
from random import choice

SEPARATOR = "\n"
UNICODE = "utf-8"
MAX_SIZE = 10 ** 5
RIP_VAL = -1
P_VALS = [331777, 614657]
A_VALS = list(range(29, 37, 2))


class CustomSet:
    def __init__(self):
        self.size = 0
        self.rip_size = 0
        self.capacity = 2
        self.elements = [None] * self.capacity
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)

    def get_hash_val(self, value):
        hash_value = 0
        current_a = self.a
        for char in value:
            hash_value = (hash_value * current_a + ord(char)) % self.p
            current_a = current_a * self.a % self.p
        return hash_value % self.capacity

    def do_rehash_and_resize(self):
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)
        old_elements = self.elements[:]
        if self.size + 1 >= self.capacity // 2 and self.capacity < 2 * MAX_SIZE:
            self.capacity = self.capacity * 2 + 3
        elif self.size < self.capacity // 8 and self.capacity > 8:
            self.capacity = (self.capacity - 3) // 2
        self.elements = [None] * self.capacity
        self.size = 0
        self.rip_size = 0
        for val in old_elements:
            if val is not None and val != RIP_VAL:
                self.insert(val, check=False)

    def insert(self, val, check=True):
        hash_val = self.get_hash_val(val)
        target_rip_hash = None
        target_none_hash = None
        while True:
            current_val = self.elements[hash_val]
            if current_val == val:
                return
            elif current_val == RIP_VAL and target_rip_hash is None:
                target_rip_hash = hash_val
            elif current_val is None:
                target_none_hash = hash_val
                break
            else:
                hash_val = (hash_val + 1) % self.capacity

        if target_rip_hash is not None:
            self.elements[target_rip_hash] = val
            self.size += 1
            self.rip_size -= 1
        elif target_none_hash is not None:
            self.elements[target_none_hash] = val
            self.size += 1

        if check and self.size + self.rip_size + 1 > self.capacity // 2:
            self.do_rehash_and_resize()

    def delete(self, val):
        hash_val = self.get_hash_val(val)
        while True:
            current_val = self.elements[hash_val]
            if current_val is None:
                return
            elif current_val == val:
                self.elements[hash_val] = RIP_VAL
                self.size -= 1
                self.rip_size += 1
                return
            else:
                hash_val = (hash_val + 1) % self.capacity

    def get_values(self):
        count = 0
        values = []
        for val in self.elements:
            if val is not None and val != RIP_VAL:
                values.append(val)
                count += 1
        values = [str(count), ] + values
        return values


class CustomMap:
    def __init__(self):
        self.size = 0
        self.rip_size = 0
        self.capacity = 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)

    def get_hash_val(self, value):
        hash_value = 0
        current_a = self.a
        for char in value:
            hash_value = (hash_value * current_a + ord(char)) % self.p
            current_a = current_a * self.a % self.p
        return hash_value % self.capacity

    def do_rehash_and_resize(self):
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)
        old_capacity = self.capacity
        old_keys = self.keys[:]
        old_values = self.values[:]
        if self.size + 1 >= self.capacity // 2 and self.capacity < 2 * MAX_SIZE:
            self.capacity = self.capacity * 2 + 3
        elif self.size < self.capacity // 8 and self.capacity > 8:
            self.capacity = (self.capacity - 3) // 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        self.rip_size = 0
        for i in range(old_capacity):
            key = old_keys[i]
            if key is not None and key != RIP_VAL:
                self.put_many(key, old_values[i])

    def put_many(self, key, vals):
        hash_val = self.get_hash_val(key)
        while True:
            current_key = self.keys[hash_val]
            if current_key is None:
                self.keys[hash_val] = key
                self.values[hash_val] = vals
                self.size += 1
                break
            else:
                hash_val = (hash_val + 1) % self.capacity

    def put(self, key, val, check=True):
        hash_val = self.get_hash_val(key)
        target_rip_hash = None
        target_none_hash = None
        while True:
            current_key = self.keys[hash_val]
            if current_key == key:
                self.values[hash_val].insert(val)
                return
            elif current_key == RIP_VAL and target_rip_hash is None:
                target_rip_hash = hash_val
            elif current_key is None:
                target_none_hash = hash_val
                break
            else:
                hash_val = (hash_val + 1) % self.capacity

        if target_rip_hash is not None:
            self.keys[target_rip_hash] = key
            self.values[target_rip_hash] = CustomSet()
            self.values[target_rip_hash].insert(val)
            self.size += 1
            self.rip_size -= 1
        elif target_none_hash is not None:
            self.keys[target_none_hash] = key
            self.values[target_none_hash] = CustomSet()
            self.values[target_none_hash].insert(val)
            self.size += 1

        if check and self.size + self.rip_size + 1 > self.capacity // 2:
            self.do_rehash_and_resize()

    def delete(self, key, val):
        hash_val = self.get_hash_val(key)
        while True:
            current_key = self.keys[hash_val]
            if current_key is None:
                return
            elif current_key == key:
                self.values[hash_val].delete(val)
                if self.values[hash_val].size == 0:
                    self.delete_all(key)
                return
            else:
                hash_val = (hash_val + 1) % self.capacity

    def delete_all(self, key):
        hash_val = self.get_hash_val(key)
        while True:
            current_key = self.keys[hash_val]
            if current_key is None:
                return
            elif current_key == key:
                self.keys[hash_val] = RIP_VAL
                self.values[hash_val] = None
                self.size -= 1
                self.rip_size += 1
                return
            else:
                hash_val = (hash_val + 1) % self.capacity

    def get(self, key):
        hash_val = self.get_hash_val(key)
        while True:
            current_key = self.keys[hash_val]
            if current_key is None:
                return ['0']
            elif current_key == key:
                return self.values[hash_val].get_values()
            else:
                hash_val = (hash_val + 1) % self.capacity


def main():
    custom_map = CustomMap()
    data = sys.stdin.buffer.read().splitlines()
    results = []
    for operation in data:
        args = operation.decode(UNICODE).split()
        if args[0] == 'put':
            custom_map.put(args[1], args[2])
        elif args[0] == 'get':
            results.append(' '.join(custom_map.get(args[1])))
        elif args[0] == 'delete':
            custom_map.delete(args[1], args[2])
        elif args[0] == 'deleteall':
            custom_map.delete_all(args[1])

    encoded_array = (SEPARATOR.join(results)).encode(UNICODE)
    sys.stdout.buffer.write(encoded_array)


if __name__ == "__main__":
    main()
