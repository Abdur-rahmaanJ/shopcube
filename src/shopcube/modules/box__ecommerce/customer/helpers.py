import os
from twilio.rest import Client
import uuid

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send_verify_code(phone_number):
    token = str(uuid.uuid4())[:4]
    message = client.messages.create(
                                body=token,
                                from_='+15733045463',
                                to=phone_number
                            )

    print(message.sid)
    return token