"""
B. Map

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте ассоциативный массив с использованием хеш таблицы.

Входные данные
Входной файл содержит описание операций, их количество не превышает 100000(10^5).
В каждой строке находится одна из следующих операций:
put 𝑥 𝑦 — поставить в соответствие ключу 𝑥 значение 𝑦. Если ключ уже есть, то значение необходимо изменить.
delete 𝑥 — удалить ключ 𝑥. Если элемента 𝑥 нет, то ничего делать не надо.
get 𝑥 — если ключ 𝑥 есть в ассоциативном массиве, то выведите соответствующее ему значение, иначе выведите «none».
Ключи и значения — строки из латинских букв длинной не более 20 символов.
Выходные данные
Выведите последовательно результат выполнения всех операций get. Следуйте формату выходного файла из примера.

Пример
входные данные
put hello privet
put bye poka
get hello
get bye
delete hello
get hello
выходные данные
privet
poka
none

Тут нужен Map (логично), разрешаем коллизии при помощи метода цепочек.
"""
import sys
from random import choice

SEPARATOR = "\n"
UNICODE = "utf-8"
MAX_SIZE = 10 ** 5
P_VALS = [655360001, 1073676287, 2971215073]
A_VALS = list(range(30, 101))


class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def get_value(self, key):
        curr_el = self.head
        while curr_el is not None:
            if curr_el.key == key:
                return curr_el
            curr_el = curr_el.next_node
        return None

    def insert_value(self, key, value):
        node = self.get_value(key)
        if node is not None:
            node.value = value
        else:
            self.head = Node(key, value, self.head)

    def delete_value(self, key):
        if self.head is None:
            return
        if self.head.key == key:
            self.head = self.head.next_node
            return
        prev_el = self.head
        curr_el = self.head.next_node
        while curr_el is not None:
            if curr_el.key == key:
                prev_el.next_node = curr_el.next_node
                break
            prev_el = curr_el
            curr_el = curr_el.next_node


class CustomMap:
    def __init__(self):
        self.capacity = MAX_SIZE * 2
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

    def put(self, key, value):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is None:
            self.elements[hash_value] = LinkedList()
        self.elements[hash_value].insert_value(key, value)

    def get(self, key):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is None:
            result = 'none'
        else:
            element = self.elements[hash_value].get_value(key)
            if element is None:
                result = 'none'
            else:
                result = element.value
        return result

    def delete(self, key):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is not None:
            self.elements[hash_value].delete_value(key)


def main():
    custom_map = CustomMap()
    data = sys.stdin.buffer.read().splitlines()
    results = []
    for operation in data:
        args = operation.decode(UNICODE).split()
        if args[0] == 'put':
            custom_map.put(args[1], args[2])
        elif args[0] == 'get':
            results.append(custom_map.get(args[1]))
        elif args[0] == 'delete':
            custom_map.delete(args[1])

    encoded_array = (SEPARATOR.join(results)).encode(UNICODE)
    sys.stdout.buffer.write(encoded_array)


if __name__ == "__main__":
    main()
