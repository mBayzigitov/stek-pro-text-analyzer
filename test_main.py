import unittest
import main

class TestFindLongestWord(unittest.TestCase):

    def test_longest_word(self):
        """Проверка нахождения самого длинного слова в списке"""
        words = ["apple", "banana", "cherry", "date"]
        result = main.find_longest_word(words)
        self.assertEqual(result, "banana")

    def test_empty_list(self):
        """Проверка случая с пустым списком"""
        words = []
        result = main.find_longest_word(words)
        self.assertIsNone(result)

    def test_single_word(self):
        """Проверка списка, содержащего одно слово"""
        words = ["watermelon"]
        result = main.find_longest_word(words)
        self.assertEqual(result, "watermelon")

    def test_words_same_length(self):
        """Проверка случая, когда все слова имеют одинаковую длину"""
        words = ["cat", "dog", "bat"]
        result = main.find_longest_word(words)
        # В случае одинаковой длины, будет возвращено первое слово с этой длиной
        self.assertEqual(result, "cat")

    def test_special_characters(self):
        """Проверка слов с особыми символами"""
        words = ["apple", "banana", "super-long-word", "cherry"]
        result = main.find_longest_word(words)
        self.assertEqual(result, "super-long-word")

    def test_mixed_case_words(self):
        """Проверка слов с разным регистром"""
        words = ["apple", "Banana", "cherry"]
        result = main.find_longest_word(words)
        self.assertEqual(result, "Banana")

class TestGetWordByIndex(unittest.TestCase):

    def test_valid_index(self):
        """Проверяем получение слова по корректному индексу"""
        words_by_lines = [["apple", "banana"], ["cherry", "date", "elderberry"]]
        borders = [(0, 1), (2, 4)]

        # Проверка на получение 3-го слова ("date")
        result = main.get_word_by_index(3, borders, words_by_lines)
        self.assertEqual(result, "date")

        # Проверка на получение 0-го слова ("apple")
        result = main.get_word_by_index(0, borders, words_by_lines)
        self.assertEqual(result, "apple")

    def test_out_of_bounds_index(self):
        """Проверяем случай, когда индекс выходит за границы"""
        words_by_lines = [["apple", "banana"], ["cherry", "date", "elderberry"]]
        borders = [(0, 1), (2, 4)]

        # Индекс выходит за границы, ожидаем пустую строку
        result = main.get_word_by_index(5, borders, words_by_lines)
        self.assertEqual(result, "")

        # Индекс отрицательный, тоже ожидаем пустую строку
        result = main.get_word_by_index(-1, borders, words_by_lines)
        self.assertEqual(result, "")

    def test_empty_words(self):
        """Проверяем случай, когда переданы пустые списки"""
        words_by_lines = []
        borders = []

        result = main.get_word_by_index(0, borders, words_by_lines)
        self.assertEqual(result, "")

    def test_edge_case(self):
        """Проверка на граничные значения индекса"""
        words_by_lines = [["one", "two", "three"], ["four", "five"]]
        borders = [(0, 2), (3, 4)]

        # Индекс в начале первого диапазона
        result = main.get_word_by_index(0, borders, words_by_lines)
        self.assertEqual(result, "one")

        # Индекс в конце второго диапазона
        result = main.get_word_by_index(4, borders, words_by_lines)
        self.assertEqual(result, "five")
        
class TestCountWords(unittest.TestCase):

    def test_simple_sentence(self):
        """Проверка для простого предложения"""
        text = "Hello world! This is a test."
        result = main.count_words(text)
        self.assertEqual(result[0], 6)  # 6 слов
        self.assertEqual(result[1], ["hello", "world", "this", "is", "a", "test"])

    def test_sentence_with_hyphens(self):
        """Проверка слов с дефисами"""
        text = "Well-known authors write high-quality books."
        result = main.count_words(text)
        self.assertEqual(result[0], 5)  # 5 слов
        self.assertEqual(result[1], ["well-known", "authors", "write", "high-quality", "books"])

    def test_empty_text(self):
        """Проверка пустого текста"""
        text = ""
        result = main.count_words(text)
        self.assertEqual(result[0], 0)  # 0 слов
        self.assertEqual(result[1], [])  # Пустой список

    def test_text_with_numbers(self):
        """Проверка текста, содержащего числа"""
        text = "The answer is 42."
        result = main.count_words(text)
        self.assertEqual(result[0], 4)  # 4 слова
        self.assertEqual(result[1], ["the", "answer", "is", "42"])

    def test_text_with_special_characters(self):
        """Проверка текста с особыми символами"""
        text = "Hello, world! (This is an example)."
        result = main.count_words(text)
        self.assertEqual(result[0], 6)  # 6 слов
        self.assertEqual(result[1], ["hello", "world", "this", "is", "an", "example"])

    def test_mixed_case_words(self):
        """Проверка текста с разным регистром"""
        text = "HELLO world! This Is A tEsT."
        result = main.count_words(text)
        self.assertEqual(result[0], 6)  # 6 слов
        self.assertEqual(result[1], ["hello", "world", "this", "is", "a", "test"])

class TestFindLinesWordOccursIn(unittest.TestCase):

    def test_single_occurrence(self):
        """Проверка, что функция находит строку с одним вхождением слова"""
        lines = [["apple", "banana"], ["cherry", "date"], ["apple", "elderberry"]]
        result = main.find_lines_word_occurs_in("banana", lines)
        self.assertEqual(result, [0])  # "banana" в строке с индексом 0

    def test_multiple_occurrences(self):
        """Проверка, что функция находит строки с несколькими вхождениями слова"""
        lines = [["apple", "banana"], ["apple", "date"], ["apple", "elderberry"]]
        result = main.find_lines_word_occurs_in("apple", lines)
        self.assertEqual(result, [0, 1, 2])  # "apple" встречается в строках 0, 1 и 2

    def test_no_occurrences(self):
        """Проверка, что функция возвращает пустой список, если слово не встречается"""
        lines = [["apple", "banana"], ["cherry", "date"], ["elderberry"]]
        result = main.find_lines_word_occurs_in("grape", lines)
        self.assertEqual(result, [])  # "grape" не встречается

    def test_empty_lines(self):
        """Проверка, что функция корректно работает с пустыми строками"""
        lines = [["apple", "banana"], [], ["cherry", "apple"]]
        result = main.find_lines_word_occurs_in("apple", lines)
        self.assertEqual(result, [0, 2])  # "apple" встречается в строках 0 и 2

    def test_target_word_with_special_characters(self):
        """Проверка слов с особыми символами."""
        lines = [["apple", "banana"], ["super-long-word", "apple"], ["cherry", "date"]]
        result = main.find_lines_word_occurs_in("super-long-word", lines)
        self.assertEqual(result, [1])  # "super-long-word" встречается в строке 1

if __name__ == '__main__':
    unittest.main()
