import sqlite3
from text_processing import creating_custom_named_entities, search_for_single_root_words_en
from thefuzz import process


def search(text: str, coll: int):
    # Подключение к БД
    con = sqlite3.connect("sirius.sqlite3")
    # Создание курсора
    cur = con.cursor()

    try:
        # Подготавливаем строку для поиска в стиле SQL LIKE
        like_text = f'%{text}%'
        
        # Поиск по терминам и описанию
        term_query = """
                     SELECT term_eng, abbr_eng, category, part_references, term_rus, abbr_rus, definition_rus, definition_eng, context_eng, context_rus
                     FROM name_table
                     WHERE term_eng LIKE ? OR definition_eng LIKE ? OR context_eng LIKE ? OR
                           term_rus LIKE ? OR definition_rus LIKE ? OR context_rus LIKE ?
                    """
        cur.execute(term_query, (like_text, like_text, like_text, like_text, like_text, like_text))
        term_results = cur.fetchall()

        # Поиск по аббревиатурам и описанию
        abbr_query = """
                     SELECT term_eng, abbr_eng, category, part_references, term_rus, abbr_rus, definition_rus, definition_eng, context_eng, context_rus
                     FROM name_table
                     WHERE abbr_eng LIKE ? OR abbr_rus LIKE ? OR
                           definition_eng LIKE ? OR definition_rus LIKE ?
                    """
        cur.execute(abbr_query, (like_text, like_text, like_text, like_text))
        abbr_results = cur.fetchall()

        # Объединяем результаты с приоритетом для аббревиатур
        results = abbr_results + term_results

        if results:
            found = True
            # Вывод ограниченного количества результатов на экран
            for elem in results[:coll]:
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
        else:
            # Получение всех терминов и аббревиатур для предложения исправлений
            cur.execute("SELECT term_eng, abbr_eng, term_rus, abbr_rus FROM name_table")
            all_terms = cur.fetchall()

            # Создание списка всех возможных терминов и аббревиатур
            all_terms_flat = [item for sublist in all_terms for item in sublist if item]

            # Использование thefuzz для нахождения похожих слов
            suggestions = process.extract(text, all_terms_flat, limit=5)

            print("По вашему запросу ничего не найдено.")
            print("Возможно вы имели ввиду:")
            for suggestion in suggestions:
                print(f"- {suggestion[0]}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрытие соединения с базой данных
        con.close()
