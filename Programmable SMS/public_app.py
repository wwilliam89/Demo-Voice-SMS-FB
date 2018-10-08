import argparse
import io
from google.cloud import vision
from google.cloud.vision import types

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Credentials.json"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def image_search_sms():
    # Start our response
    resp = MessagingResponse()

    # Grab values from incoming message
    message_from = request.values.get('From', None)
    if request.values['NumMedia'] != '0':
        message_image_url = request.values['MediaUrl0']
        # If it's a landmark, output that - otherwise keep annotating
        initialResults = annotate(message_image_url)
        if (type(initialResults) == str):
            result = initialResults
        else:
            result = report(initialResults)
        resp.message(result)
    else:
        resp.message('Please send an image.')

    # Forward the message onto a new number
    #resp.message(body = message_from + ": \n " + message_body, to="+15105574281")


    return str(resp)


def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    for landmark in landmarks:
        print('Landmark: ' + landmark.description)
        descriptionReplaced = (landmark.description).replace(" ","+")
        landmark_msg = 'This looks like a famous landmark. Perhaps it\'s: ' + landmark.description + '.\n\nInterested in learning more? Here you go: https://www.google.com/search?q=' + descriptionReplaced
        return landmark_msg

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    topMatchResult = ''
    topMatchUrl = ''
    topMatchMessage = ''

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        indexPage = 0
        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

            if (indexPage == 0):
                topMatchUrl = '\n\nFind out more here: ' + page.url
            indexPage += 1

    if annotations.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        index = 0
        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
            
            if (index == 0):
                if (entity.score < 1):
                    topMatchResult = 'That\'s a lovely picture, but we can\'t identify it. Please try another image.'
                else: 
                    topMatchResult = 'This looks familiar. Perhaps it\'s: ' + entity.description
            index += 1

    topMatchMessage = topMatchResult + topMatchUrl

    return topMatchMessage


if __name__ == '__main__':
    app.run(debug=True)
