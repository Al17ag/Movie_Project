# Создал таблицы в MySQL
# код работает

import mysql.connector  # взаимодействие с сервером MySQL

db = mysql.connector.connect(
            host = 'mysql.itcareerhub.de',
            user = 'ich1',
            password = 'ich1_password_ilovedbs')
# Создание курсора, объект курсора, который позволяет выполнять SQL-запросы и получать результаты.
cursor = db.cursor()

# SQL-код для создания новой базы данных и таблиц
sql_create_database = """
CREATE DATABASE IF NOT EXISTS 310524_ptm_AG;
USE 310524_ptm_AG;

CREATE TABLE search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    search_text TEXT,                               # для хранения текста поискового запроса
    req_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   # чтобы записывать время запроса
    SQL_req TEXT                                    # для хранения текста SQL-запроса.
);
CREATE TABLE bot_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    search_text TEXT,
    req_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sql_req TEXT
);
"""


# Выполнение SQL-кода
cursor.execute(sql_create_database)

# Закрытие курсора и соединения
cursor.close()
db.close()