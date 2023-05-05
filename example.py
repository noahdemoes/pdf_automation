import pdfplumber
import re
from pydantic import BaseModel
import pandas as pd
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Pydantic model
class Person(BaseModel):
    name: str
    number: str
    email: str

# Function to extract data from the PDF
def extract_data(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    print(text)
    
    for line in text.split("\n"):
        if "Name:" in line:
            name = line.split("Name: ")[1]
        if "Email:" in line:
            email = line.split("Email: ")[1]
        if "Number: " in line:
            number = line.split("Number: ")[1]

    return Person(name=name, number=number, email=email)

# Extract data from the PDF and create a Person instance
person_data = extract_data("sample_pdf.pdf")

# Convert the Pydantic model instance to a dictionary
person_dict = person_data.dict()

# Create a Pandas DataFrame and save it to a CSV file
df = pd.DataFrame([person_dict])
df.to_csv("sample_output.csv", index=False)



def send_email(sender_email, sender_password, recipient_email):
    # Read the content of the message.txt file
    with open('message.txt', 'r') as file:
        message_content = file.read()

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Email from message.txt'

    # Attach the content to the email
    msg.attach(MIMEText(message_content, 'plain'))

    # Connect and log in to the email server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)

    # Send the email and close the connection
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

# Sender's email credentials
sender_email = 'your_email@example.com'
sender_password = 'your_password'
recipient_email = 'recipient@example.com'

send_email(sender_email, sender_password, recipient_email)
