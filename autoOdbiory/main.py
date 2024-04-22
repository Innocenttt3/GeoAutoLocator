from db_connector import DatabaseConnector

if __name__ == '__main__':
    database = DatabaseConnector("/Users/kamilgolawski/Nauka/Programowanie/pliki init/dbConfig.ini")
    database.connect()