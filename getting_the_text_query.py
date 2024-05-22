from search import search

while True:
    # Запрос текста для поиска у пользователя
    text_query = input("Поиск: ")

    # Запрос количества ответов у пользователя
    while True:
        try:
            number_of_responses = int(input("Введите количество ответов: "))
            break
        except ValueError:
            print("Пожалуйста, введите корректное число.")

    # Выполнение функции поиска с введенными пользователем параметрами
    search(text_query, number_of_responses)

    # Проверка, были ли найдены результаты
    choice = input("Хотите ввести новое слово? (да/нет): ").lower()
    if choice != "да":
        break
