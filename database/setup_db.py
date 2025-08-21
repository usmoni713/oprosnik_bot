import asyncio
import json

from time import time
from typing import Any
import asyncpg
from random import randint


class Database:
    """Объект для работы с базой данных PostgreSQL"""

    def __init__(
        self,
        db_name: str = "oprosnik_bot",
        db_user: str = "usmoni03",
        db_password: str = "1234",
        db_host: str = "localhost",
        db_port: int = 5432,
    ):
        """Инициализирует подключение к базе данных"""
        self._db_name: str = db_name
        self._db_user: str = db_user
        self._db_password: str = db_password
        self._db_host: str = db_host
        self._db_port: int = db_port
        self._conn: asyncpg.Connection | None = None
        self.have_conn: bool = False
        self.need_close_conn: bool = False
        self.db_id = randint(1000, 999999)

    async def _connect(self) -> None:
        """Соединяет с базой данных"""
        if self.have_conn:
            return
        self._conn = await asyncpg.connect(
            database=self._db_name,
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
        )
        self.have_conn = True

    async def _close(self) -> None:
        """Закрывает соединение с базой данных"""
        if self.need_close_conn:
            if self.have_conn:
                await self._conn.close()
                self.have_conn = False

    async def execute_query(
        self,
        query: str,
    ) -> None:
        """Выполняет SQL-запрос

        :param query: SQL-запрос
        :param args: параметры запроса
        :return: None
        """
        if not self.have_conn:
            await self._connect()
            await self._conn.execute(query)
            await self._close()
        else:
            await self._conn.execute(query)

    async def create_tables(
        self,
        table_names_with_fields: list[tuple[str, list[tuple[str, str]]]],
    ) -> None:
        """Создает таблицы в базе данных и их столбцы"""
        # Соединяемся с базой данных
        await self._connect()
        # Если таблицы еще не существуют,
        # то создаем их
        for table_name, fields in table_names_with_fields:
            await self._conn.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(map(lambda field_with_type: f'{field_with_type[0]} {field_with_type[1]}', fields))});"
            )
        await self._close()

    async def fill_table(
        self,
        table_name: str,  # имя таблицы
        field_names: list[str],  # имена полей таблицы
        values: list[Any],  # значения для вставки
    ) -> None:
        """Заполняет таблицу данными

        :param table_name: имя таблицы
        :param field_names: имена полей таблицы
        :param values: значения для вставки,
               каждое значение должно быть в
               виде кортежа с количеством элементов,
               равным количеству полей в таблице
        """
        # Вставляем данные в таблицу
        query = ""
        for s_values in values:
            query += f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES {s_values}; \n "
        await self.execute_query(
            query,
        )

    async def get_table_data(
        self,
        table_name: str,  # имя таблицы
        field_names: list[str] | None = None,  # имена полей таблицы
        conditions: str = "",
    ) -> list[asyncpg.Record] | Any:
        """Возвращает значения полей из таблицы
        :param table_name: имя таблицы
        :param field_names: имена полей таблицы
        :return: список кортежей, каждый кортеж - это значения полей
                 из одной строки таблицы
        """
        # Соединяемся с базой данных
        if not self.have_conn:
            await self._connect()
        # Запрашиваем данные из таблицы
        records: list[asyncpg.Record]
        query = ""

        if not field_names is None:
            query += f"SELECT {', '.join(field_names)} FROM {table_name}"
        else:
            query += f"SELECT * FROM {table_name}"
        if conditions != "":
            query += f" WHERE {conditions}"

        
        records = await self._conn.fetch(f"{query};")

        # Закрываем соединение
        if not self.have_conn:
            await self._close()

        return records

    async def delete_value_from_table(
        self,
        table_name: str,  # имя таблицы
        field_name: str,  # имя поля
        value_to_delete: str,  # значение для удаления
    ):
        """Удаляет значение из поля в таблице"""

        query = f"DELETE FROM {table_name} WHERE {field_name} = {value_to_delete};"
        await self.execute_query(
            query,
        )

   
    async def add_question_for_quiz(
        self, 
        id_quiz:int,
        questions:list
    ):
        query = f"UPDATE quizzes SET questions = '{questions}' WHERE id_quiz = {id_quiz}"
        await self.execute_query(query)


    async def chec_user_in_database(
        self,
        user_id: int,
        table_name: str = "users",
        field_name: str = "id_user",
    ) -> bool:
        """Проверяет наличие пользователя в базе данных"""
        records = await self.get_table_data(
            table_name=table_name,
            field_names=(field_name,),
            conditions=f"{field_name} = {user_id}",
        )
        if len(records) == 0:
            return False
        else:
            return True

    async def add_new_user_in_database(
        self,
        user_id: int,
        class_: int = 9,
        age: int = 16,
    ):
        """Добавляет пользователя в базу данных"""
        await self.fill_table(
            table_name="users",
            field_names=("id_user", "class_", "age"),
            values=((user_id, class_, age),),
        )

    async def add_new_quiz(
        self,
        name_quiz:str,
        status:int,
        quantity_of_questions:int,
        questions_:list
        ):
        questions = json.dumps(questions_)
        await self.fill_table(
            table_name="quizzes",
            field_names=("name_quiz", "status", "quantity_of_questions","questions"),
            values=((name_quiz, status, quantity_of_questions, questions),)
        )
    async def get_quiz_with_name(
        self, 
        name_quiz:str
        ):
        res = await self.get_table_data(
            "quizzes", 
            conditions=f"name_quiz = '{name_quiz}'"

        )
        quiz = dict(res[0])
        quiz["questions"] = json.loads(quiz.get("questions"))
            

        
        return quiz


table_names_with_fields = [
    (
        "quizzes",
        [
            
            ("name_quiz", "TEXT"),
            ("status", "SMALLINT"),
            ("quantity_of_questions", "INTEGER"),
            ("questions", "JSONB"),
            # и другие поля
        ],
    ),
]


async def main() -> None:
    """Главная функция"""
    db = Database()

    print("Создаем таблицы...")
    await db.create_tables(table_names_with_fields)
    print("Таблицы созданы.")

    print("\nЗаполняем данные в Таблицу.")
    await db.add_new_quiz("quiz1", 0, 5, questions_=[
    {"type_question":"option", "text_question":"rrrrr?", "options_for_question":["option1", "2", "op3"]},
    {"type_question":"text", "text_question":"rrrrr1?"},
    {"type_question":"text", "text_question":"rrrrr2?"},
    {"type_question":"text", "text_question":"rrrrr3?"},
    {"type_question":"text", "text_question":"rrrrr4?"}
    ])
    
    print("Данные добавлены в таблицу.")

    print("\nПолучаем данные из таблицы и вводим на экран.\n")

    quiz1 = await db.get_quiz_with_name("quiz1")
    print(
        f"{quiz1=}")

    #TODO создать функцию для получение каждого столбца


if __name__ == "__main__":

    start_time = time()  # измеряем время выполнения функции

    asyncio.run(main())
    print(f"\n\nФункция выполнена за {time() - start_time} секунд")