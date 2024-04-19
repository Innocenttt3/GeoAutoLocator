import imaplib
import email
import googlemaps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import pandas as pd


def calculate_distances(origins, destinations, api_key):

    gmaps = googlemaps.Client(key=api_key)
    distance_matrix = gmaps.distance_matrix(origins, destinations, mode="driving")
    distances = []

    for row in distance_matrix['rows']:
        row_distances = []
        for element in row['elements']:
            distance = element.get('distance', {}).get('text', 'Unknown')
            row_distances.append(distance)
        distances.append(row_distances)

    return distances


def fetch_email():
    config = configparser.ConfigParser()
    config.read('/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini')
    login = config['EMAIL']['Username']
    password = config['EMAIL']['Password']
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.select('inbox')
    result, data = mail.search(None, 'UNSEEN')
    if result == 'OK':
        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            if result == 'OK':
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                print("Od: " + msg['From'])
                print("Temat: " + msg['Subject'])
                print("Treść: " + str(msg.get_payload(decode=True)))
                print("\n")
    mail.close()
    mail.logout()


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


start = ["Akademicka Lublin"]
destinations_data = pd.read_excel("/Users/kamilgolawski/Nauka/Programowanie/Python/autoOdbiory/mcd.xlsx")
designations = destinations_data['Adres'].tolist()
print(designations)

config = configparser.ConfigParser()
config.read('/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini')
api_key = config['API']['apiKey']

calculate_distances = calculate_distances(start, designations, api_key)

for i, start in enumerate(start):
    for j, destination in enumerate(designations):
        print(f"Długość trasy między {start} a {destination}: {calculate_distances[i][j]}")