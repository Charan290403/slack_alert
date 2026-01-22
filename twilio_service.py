from twilio.rest import Client
import re
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    WHATSAPP_FROM
)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#send whatsapp alert to mentioned user 

def send_whatsapp(message, to):
    cleaned = re.sub(r'@\w+', '', message)
    # Remove extra spaces
    message = re.sub(r'\s+', ' ', cleaned).strip()
    print(message)
    client.messages.create(
        from_=WHATSAPP_FROM,
        to=f"whatsapp:+91{to}",
        body=f"🚨 URGENT ALERT\n{message}"
    )

