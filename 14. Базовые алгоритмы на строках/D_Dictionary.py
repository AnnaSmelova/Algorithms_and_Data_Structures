"""
D. Словарь

ограничение по времени на тест: 5 секунд
ограничение по памяти на тест: 256 мегабайт
ввод: стандартный ввод
вывод: стандартный вывод

Дан набор слов и текст, требуется определить для каждого слова, присутствует ли оно в тексте как подстрока.

Входные данные
В первой строке дан текст (не более 10^6 строчных латинских букв).
Далее дано число M — количество слов в словаре.

В следующих M строках записаны слова (не более 30 строчных латинских букв).
Слова различны и отсортированы в лексикографическом порядке.

Суммарная длина слов в словаре не более 10^5.

Выходные данные
M строк вида Yes, если слово присутствует, и No иначе.

Пример
входные данные
trololo
3
abacabadabacaba
olo
trol
выходные данные
No
Yes
Yes

Применение Бора
"""
import sys

UNICODE = "utf-8"
FIRST_LETTER = ord('a')
ALPHABET_LNG = 26
WORDS_MAX_LNG = 30


class Vertex:
    def __init__(self):
        self.is_terminal = False
        self.word_ind = None
        self.next = -1


class Trie:
    def __init__(self):
        self.vertexes = [Vertex() for _ in range(ALPHABET_LNG)]

    @staticmethod
    def convert_char_to_ind(char):
        return ord(char) - FIRST_LETTER

    def insert(self, word, ind):
        dictionary = self.vertexes
        for i in range(len(word)):
            char_ind = self.convert_char_to_ind(word[i])
            if not dictionary[char_ind]:
                dictionary[char_ind] = Vertex()
                dictionary[char_ind].is_terminal = False
            if len(word) - 1 == i:
                dictionary[char_ind].is_terminal = True
                dictionary[char_ind].word_ind = ind
            if -1 == dictionary[char_ind].next:
                dictionary[char_ind].next = [Vertex() for _ in range(ALPHABET_LNG)]
            dictionary = dictionary[char_ind].next

    def contains(self, word):
        dictionary = self.vertexes
        terminals_inds = []
        for i in range(len(word)):
            char_ind = self.convert_char_to_ind(word[i])
            if not dictionary[char_ind] or -1 == dictionary[char_ind].next:
                return terminals_inds
            if dictionary[char_ind].is_terminal:
                terminals_inds.append(dictionary[char_ind].word_ind)
            dictionary = dictionary[char_ind].next
        return terminals_inds


def main():
    data = sys.stdin.buffer.read().splitlines()
    text = data[0].decode(UNICODE)
    m = int(data[1])
    trie = Trie()
    for ind, row in enumerate(data[2:]):
        word = row.decode(UNICODE)
        trie.insert(word, ind)

    result = ['No' for _ in range(m)]
    for i in range(len(text)):
        substr = text[i: i + WORDS_MAX_LNG + 1]
        contained_words_inds = trie.contains(substr)
        if contained_words_inds:
            for ind in contained_words_inds:
                result[ind] = 'Yes'

    for res in result:
        print(res)


if __name__ == "__main__":
    main()
