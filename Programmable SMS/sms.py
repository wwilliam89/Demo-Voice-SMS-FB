# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import os

# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.environ.get("ACCOUNT_SID_PARTNER_DEMO")
auth_token = os.environ.get("AUTH_TOKEN_PARTNER_DEMO")
client = Client(account_sid, auth_token)


# Send an SMS message
# message = client.messages \
#     .create(
#          body='Hello from Twilio!',
#          from_='+17814127262',
#          to='+19143740402'
#      )

# print(message.sid)

#Send a WhatsApp message
# message = client.messages \
#     .create(
#          body='Hello from WhatsApp!',
#          from_='whatsapp:+14155238886',
#          to='whatsapp:+15105574281'
#      )

# print(message.sid)

# # Send an SMS with a StatusCallback URL
# message = client.messages \
#     .create(
#          body='McAvoy or Stewart? These timelines can get so confusing.',
#          from_='+17814127262',
#          status_callback='https://720a3cc4.ngrok.io/MessageStatus',
#          to='+15105574281'
#      )

# print(message.sid)

# # Send a message with an image URL
# message = client.messages \
#                 .create(
#                      body="Let's grab lunch at Milliways tomorrow!",
#                      from_='+17814127262',
#                      media_url='https://www.redrobin.com/content/dam/web/menu/gourmet-burgers/gourmet-cheeseburger-1100.jpg',
#                      to='+15105574281'
#                  )

# print(message.sid)

# Reply to an incoming message using Twilio SMS
app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5002)