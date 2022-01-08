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

C. Новогоднее выражение

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 64 мегабайта
ввод: стандартный ввод
вывод: стандартный вывод

Задано новогоднее выражение, заканчивающееся точкой.
Необходимо посчитать его значение или сказать, что оно содержит ошибку.
В новогоднем выражении могут встречаться знаки сложения, вычитания, умножения и скобки,
константы Ded Moroz, Moroz и Snegurochka, а также вызов функции Podarok,
которая принимает одно число на вход и возвращает его, увеличенное на 5, если оно было положительно,
или возвращает его модуль, если оно было меньше либо равно 0.
Приоритет операций стандартный. Все числа в выражении целые и принадлежат диапазону LongInt.
Также гарантируется, что все промежуточные вычисления умещаются в этот тип.

Входные данные
Первая строка содержит заданное выражение.
Его длина не превосходит 200 знаков.
Гарантируется, что выражение заканчивается точкой.

Значения констант:
Ded Moroz	2020
Moroz	-30
Snegurochka	10

Выходные данные
Выведите значение этого новогоднего выражения или слово «WRONG», если значение не определено.

Пример 1
входные данные
Podarok(Moroz-Ded Moroz)*2.
выходные данные
4100

Пример 2
входные данные
Snegurochka-30.
выходные данные
-20


Расширяем грамматику с учетом трех переменных и одной новой функции, а дальше все как в B
"""
import sys


UNICODE = "utf-8"
END_OF_EXPRESSION = "."
OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
VAR_DELIMITER = " "
PROD_OPER = "*"
PLUS_OPER = "+"
MINUS_OPER = "-"
CONSTANTS = {"Ded Moroz": 2020, "Moroz": -30, "Snegurochka": 10}
FUNCTIONS = {"Podarok(": lambda x: x + 5 if x > 0 else abs(x)}


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
        elif current_symbol.isalpha() or current_symbol == VAR_DELIMITER:
            result = ''
            while current_symbol.isalpha() or current_symbol == VAR_DELIMITER or current_symbol == OPEN_BRACKET:
                result += current_symbol
                self.current_pos += 1
                if current_symbol == OPEN_BRACKET:
                    break
                current_symbol = self.expression[self.current_pos]
            self.current_pos -= 1
        elif END_OF_EXPRESSION == current_symbol:
            result = None
        else:
            result = current_symbol
        self.current_pos += 1
        return result


class Parser:
    def __init__(self, lexer):
        self.expression = []
        self.current_pos = 0
        self.tree = ParseTree()
        current_token = lexer.get_next_token()
        while current_token is not None:
            self.expression.append(current_token)
            current_token = lexer.get_next_token()
        self.size = len(self.expression)

    def parse_function(self):
        if self.size == self.current_pos:
            raise ValueError()
        current_token = self.expression[self.current_pos]
        if current_token in FUNCTIONS.keys():
            result_node = ParseTree()
            result_node.value = current_token
            self.current_pos += 1
            argument = self.parse_operation()
            if self.size == self.current_pos:
                raise ValueError()
            next_token = self.expression[self.current_pos]
            if next_token != CLOSE_BRACKET:
                raise ValueError()
            else:
                result_node.left_child = argument
                self.current_pos += 1
        else:
            return self.parse_brackets()
        return result_node

    def parse_brackets(self):
        if self.size == self.current_pos:
            raise ValueError()
        result_node = ParseTree()
        current_token = self.expression[self.current_pos]
        if current_token == OPEN_BRACKET:
            self.current_pos += 1
            result_node = self.parse_operation()
            if self.size == self.current_pos:
                raise ValueError()
            next_token = self.expression[self.current_pos]
            if next_token != CLOSE_BRACKET:
                raise ValueError()
        else:
            if current_token in CONSTANTS:
                result_node.value = current_token
            else:
                result_node.value = int(current_token)
            result_node.is_leaf = True
        self.current_pos += 1
        return result_node

    def parse_prod(self):
        if self.size == self.current_pos:
            raise ValueError()
        result_node = None
        first_value = self.parse_function()
        while self.size > self.current_pos:
            operation = self.expression[self.current_pos]
            if operation == PROD_OPER:
                self.current_pos += 1
            else:
                break
            second_value = self.parse_function()
            result_node = ParseTree()
            result_node.value = operation
            result_node.left_child = first_value
            result_node.right_child = second_value
            first_value = result_node

        if result_node is None:
            return first_value
        return result_node

    def parse_operation(self):
        if self.size == self.current_pos:
            raise ValueError()
        result_node = None
        first_value = self.parse_prod()
        while self.size > self.current_pos:
            operation = self.expression[self.current_pos]
            if operation == PLUS_OPER or operation == MINUS_OPER:
                self.current_pos += 1
            else:
                break
            second_value = self.parse_prod()
            result_node = ParseTree()
            result_node.value = operation
            result_node.left_child = first_value
            result_node.right_child = second_value
            first_value = result_node

        if result_node is None:
            return first_value
        return result_node

    def parse_expression(self):
        if self.size == 0:
            raise ValueError()
        self.tree = self.parse_operation()
        if self.size != self.current_pos:
            raise ValueError()
        return self.tree


class ParseTree:
    def __init__(self, value=None):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.is_leaf = False

    def get_result(self, a, b=None):
        operation = self.value
        if operation in FUNCTIONS.keys():
            return FUNCTIONS[operation](a)
        if operation == PLUS_OPER:
            return a + b
        elif operation == MINUS_OPER:
            return a - b
        elif operation == PROD_OPER:
            return a * b

    def evaluate(self):
        if self.is_leaf:
            return self.value
        left_value = None
        right_value = None
        if self.left_child.value is not None:
            if self.left_child.is_leaf:
                left_value = self.left_child.value
            else:
                left_value = self.left_child.evaluate()
        if self.right_child is not None and self.right_child.value is not None:
            if self.right_child.is_leaf:
                right_value = self.right_child.value
            else:
                right_value = self.right_child.evaluate()
        if left_value in CONSTANTS:
            left_value = CONSTANTS[left_value]
        if right_value is not None:
            if right_value in CONSTANTS:
                right_value = CONSTANTS[right_value]
            return self.get_result(left_value, right_value)
        else:
            return self.get_result(left_value)


def main():
    data = sys.stdin.buffer.read().splitlines()
    expression = data[0].decode(UNICODE)
    lexer = Lexer(expression)
    parser = Parser(lexer)
    try:
        tree = parser.parse_expression()
        print(tree.evaluate())
    except ValueError:
        print('WRONG')


if __name__ == "__main__":
    main()
