import os
from dotenv import load_dotenv
from pyexpat.errors import messages
from twilio.rest import Client

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        load_dotenv()
        self.account_sid=os.getenv("ACCOUNT_SID")
        self.auth_token=os.getenv("AUTH_TOKEN")
        self.client=Client(self.account_sid, self.auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            body=msg,
            from_="+18576785581",
            to="+375333278073"
        )
        print(message.body)