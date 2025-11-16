import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        load_dotenv()
        self.account_sid=os.getenv("ACCOUNT_SID")
        self.auth_token=os.getenv("AUTH_TOKEN")
        self.client=Client(self.account_sid, self.auth_token)
        self.sender = os.getenv("SMTP_SENDER")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_message(self, msg):
        message = self.client.messages.create(
            body=msg,
            from_="+18576785581",
            to="+375333278073"
        )
        print(message.body)

    def send_to_email(self, recipient, message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.sender, password=self.password)
            connection.sendmail(from_addr=self.sender,
                                to_addrs=recipient,
                                msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8'))