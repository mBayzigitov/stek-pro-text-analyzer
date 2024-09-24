import sys
import re
from collections import Counter

TOP_FREQ_WORDS = 10
INCORRECT_COMMAND_MSG = "\tНекорректная команда, введите \"help\", чтобы посмотреть список команд"

def read_file(filename):
    """Чтение файла и возврат его содержимого как строки."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        sys.exit(1)

def count_lines(text):
    lines = text.splitlines()
    return len(lines), lines

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words), [w.lower() for w in words]

def count_characters(text):
    return len(text)

def find_repeated_words(words):
    """
    Нахождение слов, которые встречаются более одного раза
    и возврат отсортированного словаря по убыванию частоты.
    """
    word_counts = Counter(words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 1}
    return dict(sorted(repeated_words.items(), key=lambda item: item[1], reverse=True))

def find_longest_word(words):
    if words:
        return max(words, key=len)
    return None

def find_lines_word_occurs_in(target, lines):
    res = []
    for i in range(len(lines)):
        for word in lines[i]:
            if word == target:
                res.append(i)
    return res

def print_refs():
    print(">> Доступные команды <<")
    print("\t* fword [слово] - вывести строки, в которых есть заданное слово")
    print("\t* fnum [номер] - вывести слово по номеру из текста")
    print("\t* save lc - (save in lowercase) преобразовать весь текст в нижний регистр и сохранить в новый файл")
    print("\t* save wp - (save without punctuation) удалить из текста все знаки препинания и сохранить результат в отдельный файл")
    print()

def print_lines_word_occurs_in(target, ws_by_lines, cache, lines):
    res_lines = {}
    if target in cache:
        res_lines = cache[target]
    else:
        res_lines = find_lines_word_occurs_in(target, ws_by_lines)
    # Вывести строки на экран
    if len(res_lines) == 0:
        print("\tДанное слово не найдено в тексте")
    else:
        print(f"\tНайдено {len(res_lines)} вхождений:")
    for res in set(res_lines):
        print(f"\t{lines[res]}")

def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py [filename]")
        sys.exit(1)
    
    filename = sys.argv[1]
    text = read_file(filename)

    # Подсчет строк, слов и символов
    num_lines, lines = count_lines(text)
    num_words, words = count_words(text)
    num_chars = count_characters(text)

    # Повторяющиеся слова
    repeated_words = find_repeated_words(words)

    # Самое длинное слово
    longest_word = find_longest_word(words)

    if num_words == 0:
        print("Текст пустой, нет данных для поиска/статистики")
        sys.exit(1)

    # Вывод результатов
    print(">>> Статистика текста <<<")
    print(f"Количество строк: {num_lines}")
    print(f"Количество слов: {num_words}")
    print(f"Количество символов: {num_chars}")
    
    if repeated_words:
        print("Слова, которые повторяются более одного раза:")
        for word, count in repeated_words.items():
            print(f"  {word}: {count} раз(а)")
    else:
        print("Нет слов, которые повторяются более одного раза")
    
    if longest_word:
        print(f"Самое длинное слово: {longest_word}")
    else:
        print("Нет слов в тексте")
    print()

    # Подготовка вспомогательных структур для оптимизации операций
    words_by_lines = []
    line_words_minmax_number = []
    c = 0
    for line in lines:
        n, line_words = count_words(line)
        line_words_minmax_number.append((c, c + n - 1))
        c += n
        words_by_lines.append([w.lower() for w in line_words])

    freq_words_cache = {}
    first_n_most_freq = min(len(repeated_words), TOP_FREQ_WORDS)
    for i, (k, v) in enumerate(repeated_words.items()):
        if i == first_n_most_freq:
            break
        freq_words_cache[k.lower()] = find_lines_word_occurs_in(k.lower(), words_by_lines)

    # Логика команд
    input_line = ""
    while input_line != "exit":
        input_line = input(">> ")
        spl = input_line.split()
        command = spl[0]

        if command == "help":
            print_refs()

        if len(spl) != 2:
            print(INCORRECT_COMMAND_MSG)
            continue

        if command == "fword":
            print_lines_word_occurs_in(spl[1].lower(), words_by_lines, freq_words_cache, lines)

if __name__ == "__main__":
    main()
