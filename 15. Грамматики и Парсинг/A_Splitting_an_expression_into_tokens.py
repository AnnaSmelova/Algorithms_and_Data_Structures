"""
Требования к выполнению домашнего задания:
Запрещено использовать встроенные парсеры, regexp-ы, функции по типу eval() и replace(), чтобы считерить
Лексер и Парсер должны быть вынесены в отдельные классы
Лексер должен инициализироваться строкой входных данных и иметь метод nextToken/nextLexem,
который будет использовать Парсер.
Парсер должен использовать лексер и не аппелировать к символам напрямую
Пожелания:
Токены лучше реализовывать через enum
Дерево разбора -- отдельный класс с методом evaluate()

A. Разделение выражения на лексемы

ограничение по времени на тест: 1 секунда
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Задано числовое выражение, заканчивающееся точкой.
Необходимо разбить его на лексемы и вывести каждую на новой строке.
Гарантируется, что исходное выражение корректно.

В выражении могут встречаться знаки сложения, вычитания, умножения и скобки.
Приоритет операций стандартный.
Все числа в выражении целые и принадлежат диапазону LongInt.

Входные данные
Первая строка содержит заданное выражение. Его длина не превосходит 100 знаков.
Гарантируется, что выражение заканчивается точкой.

Выходные данные
Выведите все встречающиеся лексемы выражения по порядку и ровно по одной на каждой строке.

Пример
входные данные
1+(2*2-3).
выходные данные
1
+
(
2
*
2
-
3
)

Учимся писать Лексер
"""
import sys


UNICODE = "utf-8"
END_OF_EXPRESSION = "."


class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.current_pos = 0

    def get_next_token(self):
        current_symbol = self.expression[self.current_pos]
        if current_symbol.isdigit():
            result = ''
            while current_symbol.isdigit():
                result += current_symbol
                self.current_pos += 1
                current_symbol = self.expression[self.current_pos]
            self.current_pos -= 1
            result = int(result)
        elif END_OF_EXPRESSION == current_symbol:
            result = None
        else:
            result = current_symbol
        self.current_pos += 1
        return result


def main():
    data = sys.stdin.buffer.read().splitlines()
    expression = data[0].decode(UNICODE)
    lexer = Lexer(expression)
    token = lexer.get_next_token()
    while token is not None:
        print(token)
        token = lexer.get_next_token()


if __name__ == "__main__":
    main()
