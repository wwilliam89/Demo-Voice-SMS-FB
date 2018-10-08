from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.jwt.client import ClientCapabilityToken

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/token', methods=['GET'])
def get_capability_token():
    """Respond to incoming requests."""

    # Find these values at twilio.com/console
    account_sid = 'ACb6668bf93d26af3fc8e3f632bd0bdaba'
    auth_token = '2976634966b7b78a332063b4368eedb6'

    capability = ClientCapabilityToken(account_sid, auth_token)

    # Twilio Application Sid
    application_sid = 'AP2439c31dd3d2b5604f3d795d40bfb97c'
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming('ValerieTest')
    token = capability.to_jwt()
    print(capability.to_jwt())

    return Response(token, mimetype='application/jwt')

@app.route("/voice", methods=['POST'])
def get_voice_twiml():
    """Respond to incoming calls with a simple text message."""

    resp = VoiceResponse()
    resp.say("Thanks for calling!")

    return Response(str(resp), mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True)