"""
C. LinkedMap

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Реализуйте прошитый ассоциативный массив с использованием хеш таблицы.

Входные данные
Входной файл содержит описание операций, их количество не превышает 100000(10^5).
В каждой строке находится одна из следующих операций:
put 𝑥 𝑦 — поставить в соответствие ключу 𝑥 значение 𝑦. Если элемент уже есть, то значение необходимо изменить.
delete 𝑥 — удалить ключ 𝑥. Если элемента 𝑥 нет, то ничего делать не надо.
get 𝑥 — если ключ 𝑥 есть в множестве выведите соответствующее ему значение, если нет выведите «none».
prev 𝑥 — вывести значение соответствующее ключу находящемуся в ассоциативном массиве,
который был вставлен позже всех, но до 𝑥 или «none», если такого нет или в массиве нет 𝑥.
next 𝑥 — вывести значение соответствующее ключу находящемуся в ассоциативном массиве,
который был вставлен раньше всех, но после 𝑥 или «none», если такого нет или в массиве нет 𝑥.
Ключи и значения — строки из латинских букв длинной не более 20 символов.
Выходные данные
Выведите последовательно результат выполнения всех операций get, prev, next.
Следуйте формату выходного файла из примера.

Пример
входные данные
put zero a
put one b
put two c
put three d
put four e
get two
prev two
next two
delete one
delete three
get two
prev two
next two
next four
выходные данные
c
b
d
c
a
e
none

Не очень понимаю насколько больно это делать, модернизируя хеш-таблицу с открытой адресацией,
так что очень советую обратить внимание на слово "Linked" и использовать метод цепочек.
"""
import sys
from random import choice

SEPARATOR = "\n"
UNICODE = "utf-8"
MAX_SIZE = 10 ** 5
P_VALS = [655360001, 1073676287, 2971215073]
A_VALS = list(range(30, 101))


class Node:
    def __init__(self, key, value, next_node=None, prev_key=None, next_key=None):
        self.key = key
        self.value = value
        self.next_key = next_key
        self.prev_key = prev_key
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def get_element_by_key(self, key):
        current = self.head
        while current is not None:
            if current.key == key:
                return current
            current = current.next_node
        return None

    def get_neighbor_key(self, key, n_type):
        current = self.get_element_by_key(key)
        if current is not None:
            if n_type == 'next':
                return current.next_key
            else:
                return current.prev_key
        return None

    def insert_value(self, key, value, last_key):
        node = self.get_element_by_key(key)
        if node is not None:
            node.value = value
            return False
        else:
            self.head = Node(key, value, self.head, last_key)
            return True
        return False

    def delete_key(self, key):
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next_node
            return True
        prev_el = self.head
        curr_el = self.head.next_node
        while curr_el is not None:
            if curr_el.key == key:
                prev_el.next_node = curr_el.next_node
                return True
            prev_el = curr_el
            curr_el = curr_el.next_node
        return False


class CustomMap:
    def __init__(self):
        self.capacity = MAX_SIZE * 2
        self.elements = [None] * self.capacity
        self.a = choice(A_VALS)
        self.p = choice(P_VALS)
        self.last_key = None

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
        result = self.elements[hash_value].insert_value(key, value, self.last_key)
        if result:
            if self.last_key is not None:
                last_key_hash_value = self.get_hash_val(self.last_key)
                if self.elements[last_key_hash_value] is not None:
                    last_el = self.elements[last_key_hash_value].get_element_by_key(self.last_key)
                    if last_el is not None:
                        last_el.next_key = key
            self.last_key = key

    def get(self, key):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is None:
            return 'none'
        else:
            element = self.elements[hash_value].get_element_by_key(key)
            if element is None:
                return 'none'
            else:
                return element.value

    def delete(self, key):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is not None:
            element = self.elements[hash_value].get_element_by_key(key)
            if element is not None:
                next_key = element.next_key
                prev_key = element.prev_key
                result = self.elements[hash_value].delete_key(key)
                if result:
                    if prev_key is not None:
                        prev_node_hash_value = self.get_hash_val(prev_key)
                        if self.elements[prev_node_hash_value] is not None:
                            prev_node = self.elements[prev_node_hash_value].get_element_by_key(prev_key)
                            if prev_node is not None:
                                prev_node.next_key = next_key
                    if next_key is not None:
                        next_node_hash_value = self.get_hash_val(next_key)
                        if self.elements[next_node_hash_value] is not None:
                            next_node = self.elements[next_node_hash_value].get_element_by_key(next_key)
                            if next_node is not None:
                                next_node.prev_key = prev_key
                    if self.last_key == key:
                        self.last_key = prev_key

    def get_neighbor(self, key, n_type='next'):
        hash_value = self.get_hash_val(key)
        if self.elements[hash_value] is not None:
            if n_type == 'next':
                next_key = self.elements[hash_value].get_neighbor_key(key, 'next')
                if next_key is not None:
                    return self.get(next_key)
            else:
                prev_key = self.elements[hash_value].get_neighbor_key(key, 'prev')
                if prev_key is not None:
                    return self.get(prev_key)
        return 'none'


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
        elif args[0] == 'next':
            results.append(custom_map.get_neighbor(args[1], 'next'))
        elif args[0] == 'prev':
            results.append(custom_map.get_neighbor(args[1], 'prev'))

    encoded_array = (SEPARATOR.join(results)).encode(UNICODE)
    sys.stdout.buffer.write(encoded_array)


if __name__ == "__main__":
    main()
