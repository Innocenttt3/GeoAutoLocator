import imaplib
import email
import googlemaps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import configparser
from typing import Optional, List
from client import Client
import email.utils
import pandas as pd


def calculate_distances(origins, destinations, api_key):
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

def fetch_emails(config) -> Optional[List[Client]]:
    login = config['EMAIL']['Username']
    password = config['EMAIL']['Password']
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
                #payload = msg.get_payload()
                content = msg.get_payload(decode=True).decode('utf-8')
                client_id = len(emails_content) + 1
                client = Client(client_id, email_address, content, name)
                emails_content.append(client)

    mail.close()
    mail.logout()

    if emails_content:
        return emails_content
    else:
        return None


def send_email(sender_email, sender_password, receiver_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Wiadomość została wysłana!")


path_to_init_file = '/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini'
destinations_data = pd.read_excel("/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx")
main_config = configparser.ConfigParser()
main_config.read(path_to_init_file)
api_key = main_config['API']['apiKey']
login = main_config['EMAIL']['Username']
password = main_config['EMAIL']['Password']
clients_emails = fetch_emails(main_config)
top_prio_destinations = destinations_data[destinations_data['Priorytety'] == 1]['Adres'].tolist()

if clients_emails is not None:
    print("Nowe wiadomości w skrzynce:")
    for client in clients_emails:
        destination_unit = calculate_distances(client.content, top_prio_destinations, api_key)
        print(destination_unit)
        content_string = str(destination_unit)
        send_email(login, password, client.email, "auto odpowiedz", content_string)
else:
    print("Brak nowych wiadomości")
