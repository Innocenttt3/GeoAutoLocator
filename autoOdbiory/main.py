from db_connector import DatabaseConnector
from user import User
if __name__ == '__main__':
    database = DatabaseConnector("/Users/kamilgolawski/Nauka/Programowanie/pliki init/dbConfig.ini")
    database.connect()
    admin = User("admin", "admin123")
    database.execute_query("INSERT INTO users (login, password, id) VALUES (admin.username, admin.password, 1)")
    database.execute_query("SELECT * FROM users")