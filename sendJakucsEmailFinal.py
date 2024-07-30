import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from collections import defaultdict

# GMAIL AUTH
from_address = 'test_email@gmail.com'
password = 'gmail_app_code'

# EMAIL BODY
email_body = """ EMAIL BODY CONTENT """

# PDF SOURCE
pdf_directory = 'C:/PATH/TO/PDF/DIRECTORY/'

# COLLECT EMAIL ADDRESSES AND FILES
files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
emails = defaultdict(list)

for file in files:
    name, email_with_ext = file.split('_', 1)
    email = email_with_ext.rsplit('.', 1)[0]  # REPLACE '.PDF' EXTENSION FROM THE END OF THE FILE NAME / EMAIL ADDRESS
    emails[email.strip()].append(os.path.join(pdf_directory, file))

# SEND EMAIL
def send_email(to_address, files):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "EMAIL SUBJECT"

    msg.attach(MIMEText(email_body, 'plain'))

    for file in files:
        with open(file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))

            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

for email, files in emails.items():
    send_email(email, files)
    #print(email, files)
