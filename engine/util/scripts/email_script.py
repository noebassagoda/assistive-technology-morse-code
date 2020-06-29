import requests
import sys
import os
import smtplib, ssl


from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText

# from dotenv import load_dotenv

email_dest    = sys.argv[1]
email_subject = sys.argv[2]
email_content = sys.argv[3]

def send_email(email_dest, email_subject, email_content):
  try:
    conn = smtplib.SMTP('imap.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    SENDER_EMAIL, SENDER_EMAIL_PASSWORD = parse_credentials()
    conn.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)

    try:
      conn.sendmail(SENDER_EMAIL, email_dest, f'Subject: {email_subject} \n\n {email_content}')
    finally:
      conn.quit()

    return "Email enviado con exito"
  except:
    return "Fallo en el envio del email"

def parse_credentials():
  f = open("config.txt", 'r')
  text = f.read()
  rows = text.split('\n')
  email = rows[0].split('=')[1]
  password = rows[1].split('=')[1]
  return email, password

print(send_email(email_dest, email_subject, email_content))
sys.stdout.flush()
