from logic import EmailHandler


if __name__ == '__main__':
    config_file_path = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'
    email_data_file_path = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx'
    email_handler = EmailHandler(config_file_path, email_data_file_path)
    email_handler.start_operations()