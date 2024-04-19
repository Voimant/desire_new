import psycopg2

with psycopg2.connect(database="acquaintances_db", user="root", password="X7cGDF6Q8yqjYbBg") as conn:
    with conn.cursor() as cur:
        def delete_db():
            """
            Функция, удаляющая таблицы базы данных
            :return: БД удалена
            """
            cur.execute("""
            DROP TABLE blacklist;
            DROP TABLE user_liked;
            DROP TABLE reviews_and_suggestions;
            DROP TABLE users
            CASCADE;
            """)
            return 'БД удалена'

        #print(delete_db())
        conn.commit()

        def create_db():
            """
            Функция, создающая структуру БД (таблицы)
            :return: База данных создана
            """
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user_name VARCHAR(40) PRIMARY KEY,
                    chat_id BIGINT NOT NULL,
                    nick_name VARCHAR(40),
                    age SMALLINT NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    photo TEXT,
                    about_me TEXT NOT NULL,
                    preferences VARCHAR(10),
                    city VARCHAR(30) NOT NULL,
                    user_index INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS blacklist(
                    user_name VARCHAR(40) REFERENCES users(user_name)
                    ON DELETE CASCADE,
                    not_liked_user VARCHAR(40) NOT NULL,
                    UNIQUE (user_name, not_liked_user)
                );
                CREATE TABLE IF NOT EXISTS reviews_and_suggestions(
                    user_name VARCHAR(40) REFERENCES users(user_name)
                    ON DELETE CASCADE,
                    description TEXT
                );
                CREATE TABLE IF NOT EXISTS user_liked(
                    user_name VARCHAR(40) REFERENCES users(user_name)
                    ON DELETE CASCADE,
                    liked_user VARCHAR(40) NOT NULL,
                    UNIQUE (user_name, liked_user)
                );
                """)
            return 'База данных создана'

       # print(create_db())
        conn.commit()
        def add_column():
             cur.execute("""ALTER TABLE users ADD COLUMN preferences_age INTEGER""")
             return 'Столбец preferences_age добавлен'
        #
        #
       # print(add_column())
       # conn.commit()
