# Поиск фильмов по базе данных sakila
# ---------------------------------------------------------------------------
""" Импорт необходимых библиотек """
import os                               # доступ к переменным окружения
from dotenv import load_dotenv          # Загружает переменные из файла .env
import mysql.connector                  # для подключения к базе данных MySQL
from prettytable import PrettyTable     # для подключения к базе данных MySQL
from datetime import datetime           # для работы с датами и временем
# ----------------------------------------------------------------------------
""" Загрузка переменных окружения """   # (pip install python-dotenv)

load_dotenv()

""" Конфигурирование базы данных """
sakila_db_config = {
    'host': os.getenv('SAKILA_DB_HOST'),
    'user': os.getenv('SAKILA_DB_USER'),
    'password': os.getenv('SAKILA_DB_PASSWORD'),
    'database': os.getenv('SAKILA_DB_NAME')
}

search_history_db_config = {
    'host': os.getenv('SEARCH_HISTORY_DB_HOST'),
    'user': os.getenv('SEARCH_HISTORY_DB_USER'),
    'password': os.getenv('SEARCH_HISTORY_DB_PASSWORD'),
    'database': os.getenv('SEARCH_HISTORY_DB_NAME')
}
# ----------------------------------------------------------------------------
class Database:
    """ класс управляет подключением к базе данных """
    def __init__(self, config):
        self.config = config

    def connect(self):
        return mysql.connector.connect(**self.config)

# ----------------------------------------------------------------------------
class SearchHistory:
    """ Класс для работы с историей поиска """
    def __init__(self, db_config):
        self.db = Database(db_config)

    def log_search(self, search_text):  # записывает текст поиска и текущую дату/время в таблицу `search_history`
        conn = self.db.connect()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO search_history (search_text, req_time, SQL_req) VALUES (%s, %s, %s)",
                           (search_text, datetime.now(), None))
            conn.commit()

    def get_popular_searches(self):   # извлекает 10 самых популярных поисковых запросов из таблицы `search_history`
        conn = self.db.connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT search_text, COUNT(*) as search_count FROM search_history GROUP BY search_text "
                           "ORDER BY search_count DESC LIMIT 10")
            return cursor.fetchall()

# ----------------------------------------------------------------------------
class MovieSearch:
    """ Класс для поиска фильмов """
    def __init__(self, db_config):
        self.db = Database(db_config)

    def search_by_keyword(self, keyword):   # выполняет поиск фильмов по ключевому слову
        conn = self.db.connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, description FROM film WHERE title LIKE %s LIMIT 10",
                           ('%' + keyword + '%',))
            return cursor.fetchall()

    def search_by_genre_year(self, genre, year):   # выполняет поиск фильмов по жанру и году
        conn = self.db.connect()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT f.title, f.description FROM film f
                JOIN film_category fc ON f.film_id = fc.film_id
                JOIN category c ON fc.category_id = c.category_id
                WHERE c.name = %s AND f.release_year = %s LIMIT 10
            """, (genre, year))
            return cursor.fetchall()

# ----------------------------------------------------------------------------


def display_results(headers, results):   # Функция для отображения результатов в виде таблицы
    table = PrettyTable(headers)
    table.add_rows(results)
    print(table)

# ----------------------------------------------------------------------------
def main():    # Создаем объекты для работы с базой данных
    movie_search = MovieSearch(sakila_db_config)
    search_history = SearchHistory(search_history_db_config)

    while True:
        choice = input("\nВведите команду:\n1: Поиск фильмов по ключевому слову\n2: Поиск фильмов по жанру и году\n3: "
                       "Вывод популярных поисков\n4: Выход\nВаш выбор: ")

        if choice == '1':
            keyword = input("Введите ключевое слово: ")
            search_history.log_search(keyword)
            results = movie_search.search_by_keyword(keyword)
            display_results(["Название", "Описание"], results)

        elif choice == '2':
            genre = input("Введите жанр: ")
            year = input("Введите год: ")
            search_history.log_search(f"{genre}, {year}")
            results = movie_search.search_by_genre_year(genre, year)
            display_results(["Название", "Описание"], results)

        elif choice == '3':
            popular_searches = search_history.get_popular_searches()
            display_results(["Поисковый запрос", "Количество"], popular_searches)

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()