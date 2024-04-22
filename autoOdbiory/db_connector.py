import psycopg2
import configparser

class DatabaseConnector:
    def __init__(self, path_to_db_init):
        main_config = configparser.ConfigParser()
        main_config.read(path_to_db_init)
        self.dbname = main_config['DATABASE']['Name']
        self.user = main_config['DATABASE']['User']
        self.password = main_config['DATABASE']['Password']
        self.host = main_config['DATABASE']['Host']
        self.port = main_config['DATABASE']['Port']
        self.schema = main_config['DATABASE']['Schema']
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.set_default_schema()
            print("Połączono z bazą danych")
        except Exception as e:
            print("Błąd podczas łączenia z bazą danych:", e)

    def set_default_schema(self):
        if self.connection:
            try:
                cur = self.connection.cursor()
                cur.execute(f"SET search_path TO {self.schema}")
                print(f"Schemat {self.schema} został ustawiony jako domyślny.")
                self.connection.commit()
            except psycopg2.Error as e:
                print("Błąd podczas ustawiania schematu:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Rozłączono z bazą danych.")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Zapytanie zostało wykonane.")
        except Exception as e:
            self.connection.rollback()
            print("Błąd podczas wykonywania zapytania:", e)
        finally:
            cursor.close()
