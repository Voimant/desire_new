from pprint import pprint
import psycopg2.extras
import pandas as pd

from acquaintances_db.db import conn


def add_user(user_name: str, chat_id: int, nick_name, age: int, gender: str, photo, about_me: str,
             preferences: str,
             city: str, user_index: int, preferences_age: int):
    """
    Функция, позволяющая добавить нового пользователя в таблицу users
    :param user_name: имя пользователя
    :param chat_id: id чата пользователя
    :param nick_name: ник пользователя
    :param age: возраст пользователя
    :param gender: пол пользователя (мужчина, девушка, пара)
    :param photo: фото пользователя
    :param about_me: информатия пользователя о себе
    :param preferences: предпочтения пользователя (мужчина, девушка, пара)
    :param city: город, в котором проживает пользователь
    :param user_index: индекс пользователя
    :param preferences_age: предпочтительный возраст искомого кандидата
    :return: Новый пользователь добавлен (Пользователь с таким user_name уже есть в базе)
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT user_name FROM users Where user_name = %s""", (user_name,))
        cur.fetchone()
        if cur.fetchone() is None:
            try:
                cur.execute("""
                            INSERT INTO users (user_name, chat_id, nick_name, age, gender, photo, about_me, preferences, city, user_index, preferences_age)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (user_name) DO NOTHING;""",
                            (
                                user_name, chat_id, nick_name, age, gender, photo, about_me, preferences, city,
                                user_index, preferences_age))
            except Exception as e:
                print(e)
                return 'Пользователь с таким user_name уже есть в базе'
        return 'Новый пользователь добавлен'





def all_id_csv():
    """
    Функция записи id пользователей в csv файл
    игнорировать предупреждение для подключения, отличного от SQLAlchemy
    смотрите: github.com/pandas-dev/pandas/issues/45660
    """
    file = pd.read_sql('SELECT user_name FROM users', conn)
    file.to_csv('users.csv', index=False)
    return 'user_name клиентов успешно записаны в файл csv'


# print(all_id_csv())

def reviews(user_name: str, description: str):
    """
    Функция для записи текста отзывов и предложений
    :param user_name: имя пользователя
    :param description: текст отзыва и/или предложения
    :return: Информация в таблицу отзывов и предложений внесена
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO reviews_and_suggestions(user_name, description)
            VALUES (%s, %s);""", (user_name, description))
        return 'Информация в таблицу отзывов и предложений внесена'


# us_name = 'Марина'
# user_description = 'Ничего так приложение'
# # print(reviews(us_name, user_description))
# conn.commit()


def liked(user_name: str, liked_user: str):
    """
    Функция для записи пары (пользователь, выполняющий запрос-пользователь, который понравился) в таблицу user_liked
    :param user_name: пользователь, выполняющий запрос
    :param liked_user: пользователь, который понравился
    :return: Понравившийся пользователь добавлен (Такая пара уже существует)
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT user_name, liked_user FROM user_liked Where user_name = %s AND liked_user = %s""",
                    (user_name, liked_user))
        cur.fetchone()
        if cur.fetchone() is None:
            try:
                cur.execute("""
                       INSERT INTO user_liked(user_name, liked_user)
                       VALUES (%s, %s)
                       ON CONFLICT (user_name, liked_user) DO NOTHING;""", (user_name, liked_user))
            except Exception as e:
                print(e)
                return 'Такая пара уже существует'
        return 'Понравившийся пользователь добавлен'


# us_name = 'Настя'
# like_user = 'Миша'
# # print(liked(us_name, like_user))
# conn.commit()


def not_liked(user_name: str, not_liked_user: str):
    """
    Функция для записи пары (пользователь, выполняющий запрос-пользователь, который не понравился) в таблицу blacklist
    :param user_name: пользователь, выполняющий запрос
    :param not_liked_user: пользователь, который не понравился
    :return: Пользователь, которые не нравится добавлен (Такая пара уже существует)
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT user_name, not_liked_user FROM blacklist Where user_name = %s AND not_liked_user = %s""",
                    (user_name, not_liked_user))
        cur.fetchone()
        if cur.fetchone() is None:
            try:
                cur.execute("""
                       INSERT INTO blacklist(user_name, not_liked_user)
                       VALUES (%s, %s)
                       ON CONFLICT (user_name, not_liked_user) DO NOTHING;""", (user_name, not_liked_user))
            except Exception as e:
                print(e)
                return 'Такая пара уже существует'
        return 'Пользователь, которые не нравится добавлен'


# us_name = 'Один'
# not_like_us = 'Миша'
# # print(not_liked(us_name, not_like_us))
# conn.commit()


def delete_user(user_name: str):
    """
    Функкция для удаления пользователя из таблицы users (каскадом удаляет всю информацию по данному пользователю из всех аблиц)
    :param user_name: пользователь из таблицы users
    :return: пользователь удалён
    """
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM users WHERE user_name = %s;""", (user_name,))
        conn.commit()
        return 'Пользователь удалён из базы данных'


# us_name = 'Voimant'
# print(delete_user(us_name))
# conn.commit()
def db_chat_id_user(user_name: str):
    """чат ид по юзернам"""
    with conn.cursor() as cur:
        select_query = "select chat_id from users where user_name = '{}'".format(user_name)
        cur.execute(select_query)
        ret = cur.fetchone()
        for row in ret:
            return row
print(db_chat_id_user('Voimant'))

#

def search(user_name):
    """
    Функция запроса вывода пола, возраста и предпочтений пользователя
    :param user_name: имя пользователя
    :return: список со словарём (пол, возрвст, предпочтения рльзователя, ведущего поиск)
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT gender, preferences_age, preferences, user_index FROM users WHERE user_name = %s""", (user_name,))
        res = cur.fetchall()
        res_list = []
        for row in res:
            res_list.append(dict(row))
        return res_list


def my_anketa(user_name):
    """
    Функция запроса вывода пола, возраста и предпочтений пользователя
    :param user_name: имя пользователя
    :return: список со словарём (пол, возрвст, предпочтения рльзователя, ведущего поиск)
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT user_name, chat_id, nick_name, age, gender, photo, about_me, preferences, city, preferences_age
             FROM users WHERE user_name = %s""", (user_name,))
        res = cur.fetchall()
        res_list = []
        for row in res:
            res_list.append(dict(row))
        return res_list

#
# us_name = 'Локи'


# pprint(search(us_name))


def search3(age: int, preferences: str, gender: str):
    """
    Функция запроса по выводу анкеты подходящих по параматрам пользователей (имя пользователя, ник, пол, информация о себе,
    его предпочтения, город, фото)
    :param age: возраст искомого кандидата
    :param preferences: пол искомого кандидата
    :param gender: предпочтения искомого кандидата
    :return: список словарей с подходящими кандтдатами
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT user_name, nick_name, gender, age, about_me, preferences, city, photo, chat_id FROM users WHERE age BETWEEN (%s - 2) AND (%s + 19)
            AND gender = %s AND preferences = %s AND bun is not true""", (age, age, preferences, gender))
        res = cur.fetchall()
        res_list = []
        for row in res:
            res_list.append(dict(row))
        return res_list


def search4(age: int, preferences: str, gender: str):
    """
    Функция запроса по выводу анкеты подходящих по параматрам пользователей (имя пользователя, ник, пол, информация о себе,
    его предпочтения, город, фото)
    :param age: возраст искомого кандидата
    :param preferences: пол искомого кандидата
    :param gender: предпочтения искомого кандидата
    :return: список словарей с подходящими кандтдатами
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """SELECT user_name, nick_name, gender, age, about_me, preferences, city, photo, chat_id FROM users WHERE age BETWEEN (%s - 0) AND (%s + 50)
            AND gender = %s AND preferences = %s""", (age, age, preferences, gender))
        res = cur.fetchall()
        res_list = []
        for row in res:
            res_list.append(dict(row))
        return res_list

#
# user_gender = 'мужчина'
# user_age = 34
# user_preferences = 'девушка'


# pprint(search3(user_age, user_preferences, user_gender))


def search_user(user_name):
    """
    Функция, которая проверяет по user_name есть ли такой пользователь в базе
    :param user_name: имя пользователя
    :return: имя пользователя либо None
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT user_name FROM users WHERE user_name = %s""", (user_name,))
        return cur.fetchone()

#
# us_name = 'Валя'


# print(search_user(us_name))

def update_user_index(user_index, user_name):
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET user_index = %s WHERE user_name = %s""", (user_index, user_name))
        return 'индекс обновили'


def update_user_data(nick_name, age: int, gender: str, photo, about_me: str, preferences: str,
                     city: str, preferences_age: int, user_name: str):
    """
    Функция обновления данных в таблице users
    :param nick_name: ник пользователя
    :param age: возраст пользователя
    :param gender: пол пользователя(мужчина, девушка, пара)
    :param photo: фото пользователя
    :param about_me: информатия пользователя о себе
    :param preferences: предпочтения пользователя(мужчина, девушка, пара)
    :param city: город, в котором проживает пользователь
    :param preferences_age: предпочтительный возраст искомого кандидата
    :param user_name: имя пользователя
    :return: Данные пользователя обновлены
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET nick_name = %s, age = %s, gender = %s, photo = %s,
                    about_me = %s, preferences = %s, city = %s, preferences_age = %s WHERE user_name = %s""",
                    (nick_name, age, gender, photo, about_me, preferences, city, preferences_age, user_name))
        return 'Данные пользователя обновлены'

#
# us_name = 'Локи'
# user_nick = '@lok'
# user_age = 28
# user_gender = 'мужчина'
# user_photo = ''
# user_about_me = 'нравится рисовать'
# user_preferences = 'пара'
# user_city = 'Рим'
# print(
#     update_user_data(user_nick, user_age, user_gender, user_photo, user_about_me, user_preferences, user_city, us_name))
# conn.commit()
#
def delete_user_liked(user_name):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM user_liked WHERE user_name = %s;""", (user_name,))
        return 'Запись из табицы user_liked удалена'



def update_index(user_name):
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET user_index = 0 WHERE user_name = %s""", (user_name,))
        return 'user_index обнулён'

# us_name = 'Voimant'
# print(delete_user_liked(us_name))
# conn.commit()
#
#
# us_name = 'Voimant'
# print(update_index(us_name))
# conn.commit()

def list_liked_users(user_name):
    """
    Функция получения списка понравившихся людей по определённому пользователю
    :param user_name: имя пользователя
    :return: список понравившихся людей
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT liked_user FROM user_liked WHERE user_name = %s""", (user_name,))
        list_1 = []
        for i in cur.fetchall():
            for item in i:
                list_1.append(item)
        return list_1

def delete_user_liked(user_name):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM user_liked WHERE user_name = %s;""", (user_name,))
        return 'Запись из табицы user_liked удалена'


def delete_not_liked_user(user_name):
    """
    Функция удаления понравившихся кандидатов по user_name
    :param user_name: имя пользователя ведущего поиск
    :return: Запись из табицы blacklist удалена
    """
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM blacklist WHERE user_name = %s;""", (user_name,))
        return 'Запись из табицы blacklist удалена'


# us_name = 'Voimant'
# print(delete_not_liked_user(us_name))
# conn.commit()

def list_not_liked_users(user_name):
    """
    Функция получения списка непонравившихся людей по определённому пользователю
    :param user_name: имя пользователя
    :return: список непонравившихся людей
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT not_liked_user FROM blacklist WHERE user_name = %s""", (user_name,))
        list_1 = []
        for i in cur.fetchall():
            for item in i:
                list_1.append(item)
        return list_1


# us_name = 'Миша'
# # print(list_not_liked_users(us_name))



def update_nick_name(nick_name: str, user_name: str):
    """
    Функция обновления ника пользователя
    :param nick_name: ник пользователя
    :param user_name: имя пользователя
    :return: Ник пользователя обновлён
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET nick_name = %s WHERE user_name = %s""", (nick_name, user_name,))
        return 'Ник пользователя обновлён'


# us_name = 'Миша'
# user_nick = 'mychan'
# # print(update_nick_name(user_nick, us_name))
# conn.commit()


def update_age(age: int, user_name: str):
    """
    Функция обновления возраста пользователя
    :param age: возраст пользователя
    :param user_name: имя пользователя
    :return: Возраст пользователя обновлён
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET age = %s WHERE user_name = %s""", (age, user_name,))
        return 'Возраст пользователя обновлён'


# us_name = 'Миша'
# user_age = 23
# # print(update_age(user_age, us_name))
# conn.commit()


def update_gender(gender: str, user_name: str):
    """
    Функция обновления пола пользователя
    :param gender: пол пользователя
    :param user_name: имя пользователя
    :return: Пол пользователя обновлён
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET gender = %s WHERE user_name = %s""", (gender, user_name,))
        return 'Пол пользователя обновлён'


# us_name = 'Миша'
# user_gender = 'девушка'
# # print(update_gender(user_gender, us_name))
# conn.commit()


def update_photo(photo: str, user_name: str):
    """
    Функция обновления фото пользователя
    :param photo: ссылка на фото пользователя
    :param user_name: имя пользователя
    :return:
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET photo = %s WHERE user_name = %s""", (photo, user_name,))
        return 'Фото пользователя обновлёно'


# us_name = 'Миша'
# user_photo = 'err'
# # print(update_photo(user_photo, us_name))
# conn.commit()


def update_about_me(about_me: str, user_name: str):
    """
    Функция обновления пользователем информации о себе
    :param about_me: информация о себе
    :param user_name: имя пользователя
    :return:
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET about_me = %s WHERE user_name = %s""", (about_me, user_name,))
        return 'Информация пользователя о себе обновлена'


# us_name = 'Миша'
# user_about_me = 'Тащусь от комиксов'
# # print(update_about_me(user_about_me, us_name))
# conn.commit()


def update_preferences(preferences: str, user_name: str):
    """
    Функция обновления предпочтения пользователя
    :param preferences: предпочтения пользователя
    :param user_name: имя пользователя
    :return: Предпочтения пользователя обновлены
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET preferences = %s WHERE user_name = %s""", (preferences, user_name,))
        return 'Предпочтения пользователя обновлены'


# us_name = 'Миша'
# user_preferences = 'пара'
# # print(update_preferences(user_preferences, us_name))
# conn.commit()
#

def update_city(city: str, user_name: str):
    """
    Функция обновления города пользователя
    :param city: город
    :param user_name: имя пользователя
    :return: Город пользователя обновлён
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET city = %s WHERE user_name = %s""", (city, user_name,))
        return 'Город пользователя обновлён'


# us_name = 'Миша'
# user_city = 'Москва'
# # print(update_city(user_city, us_name))
# conn.commit()


def update_preferences_age(preferences_age: int, user_name: str):
    """
    Функция обновления предпочтительного возраста искомого кандидата
    :param preferences_age: предпочтительный возраст искомого кандидата
    :param user_name: имя пользователя
    :return: Предпочтительный возраст искомого кандидата обновлён
    """
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET preferences_age = %s WHERE user_name = %s""", (preferences_age, user_name,))
        return 'Предпочтительный возраст искомого кандидата обновлён'


def delete_from_blacklist():
    """
    Функция удаления понравившихся кандидатов по user_name
    :return: Табица blacklist очищена
    """
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM blacklist""")
        return 'Табица blacklist очищена'


# print(delete_from_blacklist())
# conn.commit()


def delete_from_user_liked():
    """
    Функция удаления понравившихся кандидатов по user_name
    :return: Табица user_liked очищена
    """
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM user_liked""")
        return 'Табица user_liked очищена'


# print(delete_from_user_liked())
# conn.commit()




# us_name = 'Миша'
# user_preferences_age = 36
# # print(update_preferences_age(user_preferences_age, us_name))
# conn.commit()
def delete_from_users():
    """
    Функция удаления анкет пользоваталей из таблицы users
    :return: Табица users очищена
    """
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM users""")
        return 'Табица users очищена'


# print(delete_from_users())
# conn.commit()

def list_id():
    """
    Функция получает список id чатов пользователей
    :return: список id чатов
    """
    with conn.cursor() as cur:
        cur.execute("""SELECT chat_id FROM users""")
        list_1 = [item for i in cur.fetchall() for item in i]
        return list_1


#print(list_id())

def report():
    file = pd.read_sql("""SELECT user_name, nick_name, age, gender,
     about_me, preferences, city, preferences_age FROM users""", conn)
    file.to_excel('report.xlsx', index=False)
    return 'информация успешно записана в файл exel'
# print(report())

def db_bun(username):
    with conn.cursor() as cur:
        update = "UPDATE users set bun = true where user_name = '{}'".format(str(username))
        cur.execute(update)
        conn.commit()
        return 'Готово'

#print(db_bun('VIP_DESIRE_1'))

def db_rebun(username):
    with conn.cursor() as cur:
        update = "UPDATE users set bun = false where user_name = '{}'".format(str(username))
        cur.execute(update)
        conn.commit()
        return 'Готово'

#print(db_rebun('VIP_DESIRE_1'))


def db_my_chat_id(user_name):
    with conn.cursor() as cur:
        select = "select chat_id from users where user_name = '{}'".format(user_name)
        cur.execute(select)
        ret = cur.fetchone()
        for x in ret:
            return x
#print(db_my_chat_id('VIP_DESIRE_1'))


def db_bun_users(user_name: str):
    with conn.cursor() as cur:
        select = "select bun from users where bun = true and user_name = '{}'".format(user_name)
        cur.execute(select)
        ret = cur.fetchone()
        try:
            for x in ret:
                return x
        except Exception as e:
            print(e)
            return False

#print(db_bun_users('VIP_DESIRE_1'))