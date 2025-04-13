import psycopg2
from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD
from datetime import datetime
# зачем нам chat_id в частозадаваемых


class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                fetchmany: bool = False,
                commit: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                elif fetchmany:
                    result = cursor.fetchmany()
            return result


class TableCreator(DataBase):
    def create_user_table(self):
        sql = """
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                patronymic TEXT NOT NULL,
                us_group TEXT NOT NULL,
                username TEXT NOT NULL,
                administrator BOOLEAN DEFAULT false,
                chat_id BIGINT NOT NULL UNIQUE
            );
        """
        self.manager(sql, commit=True)

    def create_static_question_table(self):
        sql = """
            DROP TABLE IF EXISTS static_questions;
            CREATE TABLE IF NOT EXISTS static_questions (
                static_question_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                category_id INTEGER NOT NULL REFERENCES question_categories(category_id) ON DELETE CASCADE,
                answer TEXT NOT NULL
            ); 
        """
        self.manager(sql, commit=True)

    def create_dynamic_question_table(self):
        sql = """
            DROP TABLE IF EXISTS dynamic_questions;
            CREATE TABLE IF NOT EXISTS dynamic_questions (
                dynamic_question_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                category_id INTEGER NOT NULL REFERENCES question_categories(category_id) ON DELETE CASCADE,
                answer BOOLEAN DEFAULT false
            );
        """
        self.manager(sql, commit=True)

    def create_question_categories(self):
        sql = """
            DROP TABLE IF EXISTS question_categories;
            CREATE TABLE IF NOT EXISTS question_categories (
                category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );
        """
        self.manager(sql, commit=True)

    def create_question_subcategories(self):
        sql = """
            DROP TABLE IF EXISTS question_subcategories;
            CREATE TABLE IF NOT EXISTS question_subcategories (
                subcategory_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category_id INTEGER REFERENCES question_categories(category_id) ON DELETE CASCADE,   
                CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES question_categories (category_id) ON DELETE CASCADE
            );
        """
        self.manager(sql, commit=True)


class UserManager(DataBase):
    def get_is_user_administrator(self, chat_id):
        sql = """
            SELECT administrator FROM users 
            WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def user_exists(self, chat_id):
        sql = """
        SELECT 1 FROM users WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def add_user(self, last_name, first_name, patronymic, us_group, username, chat_id):
        sql = """
               INSERT INTO users(last_name, first_name, patronymic, us_group, username, chat_id)
               VALUES (%s, %s, %s, %s, %s, %s);
           """
        self.manager(sql, last_name, first_name, patronymic, us_group, username, chat_id, commit=True)

    def get_full_user_info(self, chat_id):
        sql = """
            SELECT last_name, first_name, patronymic, us_group, administrator FROM users
            WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def get_first_name(self, chat_id):
        sql = """
            SELECT first_name FROM users
            WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def get_user_id(self, chat_id):
        sql = """
            SELECT user_id FROM users
            WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)


class StaticQuestionManager(DataBase):
    def get_all_static_question_by_category(self, category):
        sql = """
            SELECT * FROM static_questions
            WHERE category = %s;
        """
        return self.manager(sql, category, fetchone=True)


class DynamicQuestionManager(DataBase):
    def add_dynamic_question(self, user_id, description, category_id):
        sql = """
            INSERT INTO dynamic_questions(user_id, description, category_id)
            VALUES (%s, %s, %s);
        """
        self.manager(sql, user_id, description, category_id, commit=True)

    def get_dynamic_question_by_category(self, category_name):
        sql = """
            SELECT 
                last_name, 
                first_name, 
                patronymic, 
                us_group, 
                username, 
                name AS category, 
                description
            FROM dynamic_questions 
            JOIN users ON dynamic_questions.user_id = users.user_id
            JOIN question_categories ON dynamic_questions.category_id = question_categories.category_id
            WHERE question_categories.name = %s AND answer = 'false';
        """
        return self.manager(sql, category_name, fetchall=True)


class QuestionCategoryManager(DataBase):
    def get_category(self):
        sql = """
            SELECT name FROM question_categories;
        """
        return self.manager(sql, fetchall=True)

    def get_category_id_by_name(self, category_name):
        sql = """
            SELECT category_id FROM question_categories
            WHERE name = %s;
        """
        return self.manager(sql, category_name, fetchone=True)

    def get_name_by_category_id(self, category_id):
        sql = """
            SELECT name FROM question_categories
            WHERE category_id = %s
        """
        return self.manager(sql, category_id, fetchone=True)


class QuestionSubcategoryManager(DataBase):
    def get_subcategories_by_category_id(self, category_id):
        sql = """
            SELECT subcategory_id, name FROM question_subcategories
            WHERE category_id = %s;
        """
        return self.manager(sql, category_id, fetchall=True)

    def get_subcategories_description_by_subcategory_id(self, category_id):
        sql = """
            SELECT name, description FROM question_subcategories
            WHERE subcategory_id = %s;
        """
        return self.manager(sql, category_id, fetchmany=True)


class MainManager:
    def __init__(self):
        self.user: UserManager = UserManager()
        self.static_question: StaticQuestionManager = StaticQuestionManager()
        self.dynamic_question: DynamicQuestionManager = DynamicQuestionManager()
        self.question_category: QuestionCategoryManager = QuestionCategoryManager()
        self.question_subcategory: QuestionSubcategoryManager = QuestionSubcategoryManager()


creator = TableCreator()
# creator.create_user_table()
# creator.create_question_categories()
# creator.create_question_subcategories()
# creator.create_static_question_table()
# creator.create_dynamic_question_table()
