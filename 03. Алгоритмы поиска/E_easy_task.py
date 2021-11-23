"""
E. Очень Легкая Задача

ограничение по времени на тест: 2 секунды
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Сегодня утром жюри решило добавить в вариант олимпиады еще одну, Очень Легкую Задачу.
Ответственный секретарь Оргкомитета напечатал ее условие в одном экземпляре,
и теперь ему нужно до начала олимпиады успеть сделать еще n копий. В его распоряжении имеются два ксерокса,
один из которых копирует лист за x секунд, а другой — за y.
(Разрешается использовать как один ксерокс, так и оба одновременно.
Можно копировать не только с оригинала, но и с копии.)
Помогите ему выяснить, какое минимальное время для этого потребуется.

Входные данные
На вход программы поступают три натуральных числа n, x и y, разделенные пробелом (1≤n≤2·10^8, 1≤x,y≤10).
Выходные данные
Выведите одно число — минимальное время в секундах, необходимое для получения n копий.

Пример 1
входные данные
4 1 1
выходные данные
3

Пример 2
входные данные
5 1 2
выходные данные
4
"""
import sys
from math import log2


def get_copies_cnt_by_time(sec_cnt: int, x: int, y: int) -> int:
    copies_cnt = 0
    first_copy_time = min(x, y)
    if sec_cnt > first_copy_time:
        copies_cnt += 1
        time_left = sec_cnt - first_copy_time
        copies_cnt += time_left // x + time_left // y

    return copies_cnt


def get_min_copy_time(n: int, x: int, y: int) -> int:
    left_val = 0
    right_val = min(x, y) * n
    itn = int(log2(right_val - left_val)) + 1
    for i in range(itn):
        m = int((left_val + right_val) / 2)
        if get_copies_cnt_by_time(m, x, y) < n:
            left_val = m + 1
        else:
            right_val = m

    return right_val


def main():
    n, x, y = map(int, sys.stdin.readline().split())
    print(get_min_copy_time(n, x, y))


if __name__ == "__main__":
    main()
