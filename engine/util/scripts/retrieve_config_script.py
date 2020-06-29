import requests
import sys
import os
import smtplib, ssl
import json


from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText

def save_new_config():
  try:
    SENDER_EMAIL, SENDER_EMAIL_PASSWORD, MORSE_SPEED = parse_credentials()
    credentials = {
      "email": SENDER_EMAIL,
      "password": SENDER_EMAIL_PASSWORD,
      "speed": MORSE_SPEED
    }

    return json.dumps(credentials)
  except:
    return "Fallo"

def parse_credentials():
  f = open("config.txt", 'r')
  text = f.read()
  rows = text.split('\n')
  email = rows[0].split('=')[1]
  password = rows[1].split('=')[1]
  speed = rows[2].split('=')[1]
  return email, password, speed

print(save_new_config())
sys.stdout.flush()
