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

D. Chaotic Evil

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Рассмотрим язык, чуть более похожий на Си, чем в прошлый раз.
В нём есть следующие простые типы:

*{1em}

Имя типа	Размер
bool	1 байт
char или signed char	1 байт
unsigned char	1 байт
short, signed short, short int или signed short int	2 байта
unsigned short или unsigned short int	2 байта
int, signed или signed int	4 байта
unsigned или unsigned int	4 байта
long, signed long, long int или signed long int	8 байт
unsigned long или unsigned long int	8 байт
long long, signed long long, long long int или signed long long int	8 байт
unsigned long long или unsigned long long int	8 байт

*{1em}
В языке есть оператор sizeof, который позволяет узнать размер любого типа в байтах.
К примеру, sizeof(int) равен четырём.

В языке есть оператор alignof, который позволяет узнать выравнивание любого типа в байтах.
Адрес переменной какого-то типа T в памяти должен делиться на alignof(T).
sizeof(T) всегда делится на alignof(T).
alignof(T) всегда является неотрицательной целой степенью двойки.
Для простых типов, alignof(T) == sizeof(T).

В языке есть массивы фиксированной длины, состоящие из элементов одного типа.
Массив из n элементов, каждый типа T обозначается как T[n].
sizeof(T[n]) равен sizeof(T) * n.
К примеру, sizeof(short[13]) равен 26, так как размер типа short — два байта, а в массиве 13 элементов.
alignof(T[n]) равен alignof(T).
Поддержки многомерных массивов в языке нет.

В языке есть структуры — композитные типы, позволяющие объединять фиксированное количество переменных (полей)
разных типов в одну.
Пусть в структуре n>0 полей f1,...,fn типов T1,...,Tn.
Пусть эта структура лежит в памяти по адресу a.
Тогда должны выполняться следующие дополнительные условия:

Адрес f1 равен a.
Для k=2,...,n, Адрес fk больше адреса fk-1.
Поля не могут пересекаться
Как и для самой структуры, так и для всех её полей должны выполнятся стандартные правила выравнивания.
Выравнивание структуры — максимум из выравниваний её полей.
Размер структуры не меньше суммы размеров её полей.
Размер структуры — минимальный из размеров, удовлетворяющий всем условиям.
Вам предлагается написать программу, вычисляющую sizeof и alignof для произвольных типов.

Входные данные
Во вводе записаны команды, typedef, sizeof или alignof.

Команда typedef объявляет новый тип.
Например, typedef eightbytes unsigned char[8] объявляет новый тип eightbytes,
который представляет собой массив из восьми unsigned char.
typedef может также объявлять структуры. Смотрите примеры.
Гарантируется, что имя нового типа — непустая строка из латинских букв длиной не более 32 символов,
кроме bool, char, signed, unsigned, short, int, long, struct, typedef, sizeof, alignof

Гарантируется, что объявления новых типов имеют уникальные имена.

Команды sizeof и alignof печатают на экран на новой строке размер и выравнивание типа соответственно.
Например, sizeof unsigned char[8] напечатает на экран 8.

Гарантируется, что размер входных данных по объёму не превосходит одного мегабайта.
Размер каждого используемого типа не превосходит одного эксабайта.

Выходные данные
Для каждой команды sizeof или alignof в отдельной строке напечатайте результат выполнения соответствующего оператора.

Пример 1
входные данные
typedef eightbytes unsigned char[8]
sizeof eightbytes
alignof eightbytes
выходные данные
8
1

Пример 2
входные данные
typedef verylong struct {
long[2];
unsigned short int[4];
}
sizeof verylong
alignof verylong
выходные данные
24
8

Пример 3
входные данные
typedef verylong struct {
long[2];
unsigned short int[4];
}
typedef evenlonger struct {
verylong[4];
}
sizeof evenlonger
alignof evenlonger
typedef arr evenlonger[123]
sizeof arr
alignof arr
выходные данные
96
8
11808
8

Задача на осознание небоянистого языка, придумывание грамматики и последующая обработка текста на этом языке
"""
import sys


UNICODE = "utf-8"
END_OF_LINE = "\n"
TYPE_FUNC = "typedef"
SIZE_FUNC = "sizeof"
ALIGN_FUNC = "alignof"
STRUCTURE = "struct"
END_OF_STRUCTURE = '}'
IGNORE_SYMBOLS = ["[", "]", "{", " ", ";"]
TYPE_DELIMITER = " "
BASE_TYPES = {
    "bool": [1, 1],
    "char": [1, 1],
    "signed char": [1, 1],
    "unsigned char": [1, 1],
    "short": [2, 2],
    "signed short": [2, 2],
    "short int": [2, 2],
    "signed short int": [2, 2],
    "unsigned short": [2, 2],
    "unsigned short int": [2, 2],
    "int": [4, 4],
    "signed": [4, 4],
    "signed int": [4, 4],
    "unsigned": [4, 4],
    "unsigned int": [4, 4],
    "long": [8, 8],
    "signed long": [8, 8],
    "long int": [8, 8],
    "signed long int": [8, 8],
    "unsigned long": [8, 8],
    "unsigned long int": [8, 8],
    "long long": [8, 8],
    "signed long long": [8, 8],
    "long long int": [8, 8],
    "signed long long int": [8, 8],
    "unsigned long long": [8, 8],
    "unsigned long long int": [8, 8]
}


class Lexer:
    def __init__(self):
        self.current_pos = 0
        self.expression = ''
        self.tokens = []

    def get_expression_tokens(self, expression):
        self.expression = expression
        self.current_pos = 0
        current_token = self.get_next_token()
        while current_token is not None:
            self.tokens.append(current_token)
            current_token = self.get_next_token()

    def get_next_token(self):
        current_symbol = self.expression[self.current_pos]
        if current_symbol in IGNORE_SYMBOLS:
            while current_symbol in IGNORE_SYMBOLS:
                self.current_pos += 1
                current_symbol = self.expression[self.current_pos]
        if current_symbol.isalpha():
            result = ''
            while current_symbol.isalpha():
                result += current_symbol
                self.current_pos += 1
                current_symbol = self.expression[self.current_pos]
                if current_symbol == TYPE_DELIMITER and result in BASE_TYPES.keys():
                    result += current_symbol
                    self.current_pos += 1
                    current_symbol = self.expression[self.current_pos]
            self.current_pos -= 1
        elif current_symbol.isdigit():
            result = ''
            while current_symbol.isdigit():
                result += current_symbol
                self.current_pos += 1
                current_symbol = self.expression[self.current_pos]
            self.current_pos -= 1
        elif current_symbol == END_OF_LINE:
            result = None
        else:
            result = current_symbol
        self.current_pos += 1
        return result


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.size = len(self.tokens)

    def parse_struct(self):
        self.current_pos += 1
        current_token = self.tokens[self.current_pos]
        var_align = 1
        var_size = 0
        cnt = 1
        while current_token != END_OF_STRUCTURE:
            var_type = current_token
            self.current_pos += 1
            current_token = self.tokens[self.current_pos]
            if current_token.isdigit():
                cnt = int(current_token)
                self.current_pos += 1
                current_token = self.tokens[self.current_pos]
            type_align = BASE_TYPES[var_type][1]
            type_size = BASE_TYPES[var_type][0] * cnt
            diff = var_size % type_align
            if diff != 0:
                var_size = var_size - diff + type_align
            var_size += type_size
            var_align = max(BASE_TYPES[var_type][1], var_align)
            cnt = 1
        diff = var_size % var_align
        if diff != 0:
            var_size = var_size - diff + var_align
        self.current_pos += 1
        return var_align, var_size

    def parse_typedef(self):
        self.current_pos += 1
        current_token = self.tokens[self.current_pos]
        var_value = current_token
        self.current_pos += 1
        current_token = self.tokens[self.current_pos]
        if current_token != STRUCTURE:
            var_cnt = 1
            var_type = current_token
            self.current_pos += 1
            current_token = self.tokens[self.current_pos]
            if current_token.isdigit():
                var_cnt = int(current_token)
                self.current_pos += 1
            var_size = BASE_TYPES[var_type][0] * var_cnt
            var_align = BASE_TYPES[var_type][1]
        else:
            var_align, var_size = self.parse_struct()
        BASE_TYPES[var_value] = [var_size, var_align]

    def parse_function(self):
        while self.size - 1 > self.current_pos:
            current_token = self.tokens[self.current_pos]
            if current_token == TYPE_FUNC:
                self.parse_typedef()
            elif current_token == SIZE_FUNC:
                self.current_pos += 1
                var_cnt = 1
                var_type = self.tokens[self.current_pos]
                if self.size - 1 > self.current_pos:
                    self.current_pos += 1
                    current_token = self.tokens[self.current_pos]
                    if current_token.isdigit():
                        var_cnt = int(current_token)
                        self.current_pos += 1
                print(str(BASE_TYPES[var_type][0]*var_cnt))
            elif current_token == ALIGN_FUNC:
                self.current_pos += 1
                var_type = self.tokens[self.current_pos]
                if self.size - 1 > self.current_pos:
                    self.current_pos += 1
                    current_token = self.tokens[self.current_pos]
                    if current_token.isdigit():
                        self.current_pos += 1
                print(str(BASE_TYPES[var_type][1]))


def main():
    data = sys.stdin.buffer.read().decode(UNICODE).splitlines()
    lexer = Lexer()
    for line in data:
        expression = line + END_OF_LINE
        lexer.get_expression_tokens(expression)
    parser = Parser(lexer.tokens)
    parser.parse_function()


if __name__ == "__main__":
    main()
