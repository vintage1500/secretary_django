from django.db import connection

def close_db_connection():
    """Закрытие соединения с БД после операций"""
    connection.close()

def execute_with_retry(query_func, max_retries=3):
    """Повторное выполнение при ошибках БД"""
    for attempt in range(max_retries):
        try:
            return query_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            connection.close()  