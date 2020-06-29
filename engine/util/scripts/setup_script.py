import requests
import sys
import os
import smtplib, ssl


from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText

# from dotenv import load_dotenv

email          = sys.argv[1]
email_password = sys.argv[2]
speed          = sys.argv[3]

def save_new_config(email, password, speed):
  try:
    f = open("config.txt", 'r')
    text = f.read()
    rows = text.split('\n')

    new_config = "SENDER_EMAIL=%s\n" % email
    new_config += "SENDER_EMAIL_PASSWORD=%s\n" % password
    new_config +=  "MORSE_SPEED=%s\n" % speed

    f = open("config.txt", 'w')
    f.write(new_config)
    return "Configuracion guardada con exito"
  except:
    return "Fallo en el envio del email"

def parse_new_config():
  f = open("config.txt", 'r')
  text = f.read()
  rows = text.split('\n')
  email = rows[0].split('=')[1]
  password = rows[1].split('=')[1]
  return email, password

print(save_new_config(email, email_password, speed))
sys.stdout.flush()
