import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser


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

fetch_email()

config = configparser.ConfigParser()
config.read('/Users/kamilgolawski/Nauka/Programowanie/pliki init/config.ini')
sender_email = config['EMAIL']['Username']
sender_password = config['EMAIL']['Password']
receiver_email = "kamilgolawski3@icloud.com"
subject = "Testowa wiadomość do wysłania"
body = "Treść testowej wiadomości"

send_email(sender_email, sender_password, receiver_email, subject, body)
