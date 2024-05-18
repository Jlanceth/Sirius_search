import sqlite3
from text_processing import creating_custom_named_entities, search_for_single_root_words_en
from thefuzz import process

def search(text: str, coll: int):
    # Подключение к БД
    con = sqlite3.connect("sirius.sqlite3")
    # Создание курсора
    cur = con.cursor()

    try:
        # Удаление предварительной обработки текста, чтобы искать по полному термину
        # text = search_for_single_root_words_en(text)

        # Поиск производится по следующим столбцам с английским и русским текстом: term_eng, abbr_eng, category, part_references, term_rus, abbr_rus, definition_rus, definition_eng, context_rus, context_eng
        query = """
                SELECT term_eng, abbr_eng, category, part_references, term_rus, abbr_rus, definition_rus, definition_eng, context_rus, context_eng
                FROM name_table
                WHERE term_eng LIKE ? OR abbr_eng LIKE ? OR 
                      definition_eng LIKE ? OR context_eng LIKE ? OR
                      term_rus LIKE ? OR abbr_rus LIKE ? OR 
                      definition_rus LIKE ? OR context_rus LIKE ?
                """
        # Выполнение запроса и получение всех результатов
        like_text = f'%{text}%'
        cur.execute(query, (like_text, like_text, like_text, like_text, like_text, like_text, like_text, like_text))
        results = cur.fetchmany(coll)

        # Проверка наличия результатов
        if not results:
            print("По вашему запросу ничего не найдено.")
            return

        # Вывод результатов на экран
        for elem in results:
            term_eng, abbr_eng, category, part_references, term_rus, abbr_rus, definition_rus, definition_eng, context_rus, context_eng = elem
            print(f"Термин на английском: {term_eng}")
            print(f"Аббревиатура на английском: {abbr_eng}")
            print(f"Категория: {category}")
            print(f"Part References: {part_references}")
            print(f"Термин на русском: {term_rus}")
            print(f"Аббревиатура на русском: {abbr_rus}")
            print(f"Объяснение на русском: {definition_rus}")
            print(f"Объяснение на английском: {definition_eng}")
            print(f"Контекст на русском: {context_rus}")
            print(f"Контекст на английском: {context_eng}")
            print("-" * 40)  # Разделитель между записями
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрытие соединения с базой данных
        con.close()
