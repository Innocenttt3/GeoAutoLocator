from celery import Celery
from logic import EmailHandler
import configparser

celery = Celery('tasks', broker='redis://localhost:6379/0')
email_data_file_path = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx'
UPLOAD_FOLDER = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/server storage'
RESULTS_FOLDER = '/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/autoOdbiory/results'
CONFIG_FILE_PATH = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'

email_handler = EmailHandler(CONFIG_FILE_PATH)
email_handler.set_email_data_file_path(email_data_file_path)
service_config = configparser.ConfigParser()
service_config.read(CONFIG_FILE_PATH)


@celery.task()
def start_email_handler_task():
    email_handler.start_operations()


@celery.task()
def stop_email_handler_task():
    email_handler.stop_operations()
