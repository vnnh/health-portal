import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = os.environ['PHONE_NUMBER']
client = Client(account_sid, auth_token)


def call(_phone):
    client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to=phone_number,
        from_='+19378216081'
    )


def email(address, message):
    print(f"Send '{message}' to {address}")
