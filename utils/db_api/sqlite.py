import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
            self,
            sql: str,
            parameters: tuple = None,
            fetchone=False,
            fetchall=False,
            commit=False
    ):
        if not parameters:
            parameters = ()

        connection = self.connection
        connection.set_trace_callback(logger)

        cursor = connection.cursor()
        data = None

        cursor.execute(sql, parameters)

        if commit:
            connection.commit()

        if fetchall:
            data = cursor.fetchall()

        if fetchone:
            data = cursor.fetchone()

        connection.close()

        return data

    def create_table_users(self):
        sql = """
       CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username VARCHAR(255),
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            age INTEGER NOT NULL,
            phone VARCHAR(255) NOT NULL,
            photo_id VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        self.execute(sql, commit=True)

        try:
            self.execute(
                'ALTER TABLE Users ADD COLUMN photo_id VARCHAR(255);',
                commit=True
            )
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])

        return sql, tuple(parameters.values())

    def add_user(
            self,
            id: int,
            username: str,
            first_name: str,
            last_name: str,
            age: int,
            phone: str

    ):
        sql = """
        INSERT INTO Users(
            id,
            username,
            first_name,
            last_name,
            age,
            phone
        )
        VALUES(?, ?, ?, ?, ?, ?)
        """

        self.execute(
            sql,
            parameters=(
                id,
                username,
                first_name,
                last_name,
                age,
                phone
            ),
            commit=True
        )

    def add_photo(self, id: int, photo_id: str):

        sql = """
        UPDATE Users
        SET photo_id=?
        WHERE id=?
        """

        self.execute(
            sql,
            parameters=(
                photo_id,
                id
            ),
            commit=True
        )

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """

        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "

        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(
            sql,
            parameters=parameters,
            fetchone=True
        )

    def count_users(self):
        return self.execute(
            "SELECT COUNT(*) FROM Users;",
            fetchone=True
        )

    def update_user(
            self,
            id: int,
            first_name: str,
            last_name: str,
            age: int,
            phone: str
    ):
        sql = """
        UPDATE Users
        SET first_name=?,
            last_name=?,
            age=?,
            phone=?
        WHERE id=?
        """

        return self.execute(
            sql,
            parameters=(
                first_name,
                last_name,
                age,
                phone,
                id
            ),
            commit=True
        )

    def update_photo(self, id: int, photo_id: str):

        sql = """
        UPDATE Users
        SET photo_id=?
        WHERE id=?
        """

        self.execute(
            sql,
            parameters=(
                photo_id,
                id
            ),
            commit=True
        )

    def delete_user(self, id: int):
        sql = """
        DELETE FROM Users
        WHERE id=?
        """

        return self.execute(
            sql,
            parameters=(id,),
            commit=True
        )

    def select_all_answer(self):
        sql = """
        SELECT * FROM Answer
        """

        return self.execute(sql, fetchall=True)

    def select_tests(self, **kwargs):
        sql = "SELECT * FROM Tests WHERE "

        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(
            sql,
            parameters=parameters,
            fetchone=True
        )

    def update_user_email(self, email, id):
        sql = """
        UPDATE Users
        SET email=?
        WHERE id=?
        """

        return self.execute(
            sql,
            parameters=(email, id),
            commit=True
        )

    def delete_tests(self):
        self.execute(
            "DELETE FROM Tests WHERE TRUE",
            commit=True
        )

    def delete_answer(self):
        self.execute(
            "DELETE FROM Answer WHERE TRUE",
            commit=True
        )


def logger(statement):
    pass

def update_user(self, id, first_name, last_name, age, phone):

    sql = """
    UPDATE Users
    SET first_name=?,
        last_name=?,
        age=?,
        phone=?
    WHERE id=?
    """

    self.execute(
        sql,
        parameters=(
            first_name,
            last_name,
            age,
            phone,
            id
        ),
        commit=True
    )


def delete_user(self, id):

    sql = """
    DELETE FROM Users
    WHERE id=?
    """

    self.execute(
        sql,
        parameters=(id,),
        commit=True
    )