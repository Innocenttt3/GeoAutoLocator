import imaplib
import email
import googlemaps
import smtplib
import email.utils
import pandas as pd
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import Optional, List
from client import Client
import time


class EmailHandler:
    def __init__(self, config_file_path: str, email_data_file_path: str):
        self.is_running = False
        self.config_file_path = config_file_path
        self.email_data_file_path = email_data_file_path

    def calculate_distances(self, origins, destinations, api_key):
        gmaps = googlemaps.Client(key=api_key)

        distance_matrix = gmaps.distance_matrix(origins, destinations, mode="driving")
        results = []

        for i, row in enumerate(distance_matrix['rows']):
            for j, element in enumerate(row['elements']):
                distance_meters = element.get('distance', {}).get('value', float('inf'))
                distance_km = distance_meters / 1000
                destination_name = destinations[j]
                results.append((distance_km, destination_name))

        shortest_distance = min(results, key=lambda x: x[0])

        return shortest_distance

    def fetch_emails(self, login, password) -> Optional[List[Client]]:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(login, password)
        mail.select('inbox')
        result, data = mail.search(None, 'UNSEEN')
        emails_content = []

        if result == 'OK':
            for num in data[0].split():
                result, data = mail.fetch(num, '(RFC822)')
                if result == 'OK':
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    encoded_sender = msg['From']
                    email_address = email.utils.parseaddr(encoded_sender)[1]
                    name = decode_header(encoded_sender)[0][0].decode('utf-8')

                    payload = msg.get_payload()
                    if isinstance(payload, list):
                        payload = payload[0]

                    content = payload if isinstance(payload, str) else payload.get_payload(decode=True).decode('utf-8')

                    client_id = len(emails_content) + 1
                    client = Client(client_id, email_address, content, name)
                    emails_content.append(client)

        mail.close()
        mail.logout()

        if emails_content:
            return emails_content
        else:
            return None

    def send_email(self, sender_email, sender_password, receiver_email, subject, body):
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Wiadomość została wysłana!")

    def process_emails(self):
        main_config = configparser.ConfigParser()
        main_config.read(self.config_file_path)
        api_key = main_config['API']['apiKey']
        print(api_key)
        login = main_config['EMAIL']['Username']
        password = main_config['EMAIL']['Password']

        destinations_data = pd.read_excel(self.email_data_file_path)
        top_prio_destinations = destinations_data[destinations_data['Priorytety'] == 1]['Adres'].tolist()

        clients_emails = self.fetch_emails(login, password)

        if clients_emails is not None:
            print("Nowe wiadomości w skrzynce:")
            for client in clients_emails:
                destination_unit = self.calculate_distances(client.content, top_prio_destinations, api_key)
                print(destination_unit)
                content_string = str(destination_unit)
                self.send_email(login, password, client.email, "auto odpowiedz", content_string)
        else:
            print("Brak nowych wiadomości")

    def run_email_handler(self):
        while self.is_running:
            self.process_emails()
            time.sleep(60)

    def start_operations(self):
        if not self.is_running:
            self.is_running = True
            self.run_email_handler()

    def stop_operations(self):
        self.is_running = False
