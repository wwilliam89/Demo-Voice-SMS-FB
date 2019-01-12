# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

#Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ASID"
auth_token  = "ATOKEN"
workspace_sid = "WSID"
workflow_sid = "WFSID"

client = Client(username=account_sid, password=auth_token)

@app.route("/facebook", methods=['GET', 'POST'])
def messenger_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.")

    # Create task for Flex

    return str(resp)

@app.route("/create_task", methods=['GET', 'POST'])
def create_task():
    """Creating a Task"""
    task = client.taskrouter.workspaces(sid=workspace_sid).tasks.create(
        workflow_sid=workflow_sid,
        attributes='{"selected_language":"es"}'
    )
    print(task.attributes)
    resp = Response({}, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(debug=True)
