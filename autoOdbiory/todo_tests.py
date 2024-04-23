from logic import EmailHandler
import configparser

if __name__ == '__main__':
    config_file_path = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'
    email_data_file_path = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx'
    main_config = configparser.ConfigParser()
    main_config.read(config_file_path)
    login = main_config['EMAIL']['Username']
    password = main_config['EMAIL']['Password']
    email_handler = EmailHandler(config_file_path, email_data_file_path)
    print(email_handler.fetch_emails(login, password))