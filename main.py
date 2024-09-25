import sys, re, glob
from collections import Counter

TEXT = "" # обрабатываемый текст из файла
WORDS_BY_LINES = [] # двумерный список слов по строкам
# Список пар вида (n, m), используется для бин поиска слова по номеру
# n - номер первого слова в строке
# m - номер последнего слова в строке
LINE_WORDS_MINMAX_NUMBER = []
LINES = [] # текст разбитый по строкам
NUM_WORDS = 0 # количество слов в тексте
REPEATED_WORDS = {} # карта слов, повторяющихся более 1 раза
FREQ_WORDS_CACHE = {} # карта вида (слово, список индексов строк в которых оно есть)

TOP_FREQ_WORDS = 10
INCORRECT_COMMAND_MSG = "\tНекорректная команда, введите \"help\", чтобы посмотреть список команд"
SAMPLE_NAME = "output-"
SAMPLE_EXT = ".txt"

def read_file(filename):
    """Чтение файла и возврат его содержимого как строки"""
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
    words = re.findall(r'\b[\w-]+\b', text)
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
    """Найти индексы строк, в которых есть слово target"""
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
    """Вывести на экран строки, в которых есть слово target"""
    res_lines = [] # итоговый список индексов строк
    if target in cache:
        res_lines = cache[target] # если это слово часто употребляется - взять из "кэша"
    else:
        res_lines = find_lines_word_occurs_in(target, ws_by_lines) # если нет - выполнить поиск
    # Вывести строки на экран
    if len(res_lines) == 0:
        print("\tДанное слово не найдено в тексте")
    else:
        print(f"\tНайдено {len(res_lines)} вхождений:")
    for res in set(res_lines):
        print(f"\t{lines[res]}")

def get_word_by_index(idx, borders, words_by_lines):
    """Вывести на экран слово по номеру idx"""
    l = 0
    h = len(borders) - 1
    mid = 0

    while l <= h:
        mid = (l + h) // 2

        if borders[mid][1] < idx:
            l = mid + 1
        elif borders[mid][0] > idx:
            h = mid - 1
        else:
            return words_by_lines[mid][idx - borders[mid][0]]
    return ""

def count_existing_files():
    return len(glob.glob(SAMPLE_NAME + "*" + SAMPLE_EXT))

def write_sample_file_content(text, ftype):
    n = count_existing_files()  # вычислить номер нового файла
    try:
        with open(SAMPLE_NAME + str(n) + SAMPLE_EXT, "x", encoding='utf-8') as file:
            file.write(text.lower())
    except IOError:
        print("\t! Возникла ошибка, файл не записан")
        return
    print(f"\tТекст {ftype} успешно записан в файл {SAMPLE_NAME + str(n) + SAMPLE_EXT}")

def print_stats():
    if len(sys.argv) != 2:
        print("Использование: python main.py [filename]")
        sys.exit(1)

    global TEXT
    filename = sys.argv[1]
    TEXT = read_file(filename)

    # Подсчет строк, слов и символов
    num_lines, lines = count_lines(TEXT)
    global LINES
    LINES = lines
    global NUM_WORDS
    NUM_WORDS, words = count_words(TEXT)
    num_chars = count_characters(TEXT)

    # Повторяющиеся слова
    repeated_words = find_repeated_words(words)

    # Самое длинное слово
    longest_word = find_longest_word(words)

    if NUM_WORDS == 0:
        print("Текст пустой, нет данных для поиска/статистики")
        sys.exit(1)

    # Вывод результатов
    print(">>> Статистика текста <<<")
    print(f"Количество строк: {num_lines}")
    print(f"Количество слов: {NUM_WORDS}")
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

def prep_helper_structs():
    """Подготовка вспомогательных структур для оптимизации операций"""
    c = 1
    for line in LINES:
        n, line_words = count_words(line)
        LINE_WORDS_MINMAX_NUMBER.append((c, c + n - 1))
        c += n
        WORDS_BY_LINES.append([w.lower() for w in line_words])

    first_n_most_freq = min(len(REPEATED_WORDS), TOP_FREQ_WORDS)
    for i, (k, v) in enumerate(REPEATED_WORDS.items()):
        if i == first_n_most_freq:
            break
        FREQ_WORDS_CACHE[k.lower()] = find_lines_word_occurs_in(k.lower(), WORDS_BY_LINES)

def listen_commands():
    # Логика команд
    input_line = ""
    while input_line != "exit":
        input_line = input(">> ")
        spl = input_line.rstrip().split()
        command = spl[0]

        if command == "exit":
            sys.exit(1)

        if command == "help":
            print_refs()

        if len(spl) != 2:
            print(INCORRECT_COMMAND_MSG)
            continue

        subcommand = spl[1]

        if command == "fword":
            print_lines_word_occurs_in(subcommand.lower(), WORDS_BY_LINES, FREQ_WORDS_CACHE, LINES)
        elif command == "fnum":
            try:
                number = int(subcommand)
                if number <= 0 or number > NUM_WORDS:
                    print(f"Некорректный номер слова, всего слов в тексте: {NUM_WORDS}")
                    continue
                found_word = get_word_by_index(number, LINE_WORDS_MINMAX_NUMBER, WORDS_BY_LINES)
                if found_word:
                    print(found_word)
            except ValueError:
                print(INCORRECT_COMMAND_MSG)
        elif command == "save":
            if subcommand == "lc":
                write_sample_file_content(TEXT.lower(), "в нижнем регистре")
            elif subcommand == "wp":
                write_sample_file_content(re.sub('[^\w\s]+', '', TEXT), "без знаков препинания")
            else:
                print(INCORRECT_COMMAND_MSG)

def main():
    print_stats()
    prep_helper_structs()
    listen_commands()

if __name__ == "__main__":
    main()
