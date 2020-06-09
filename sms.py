from flask import Flask, request, redirect, make_response, redirect, url_for
from random import randint
from twilio_api import get_twilio_criteria, twilio_responder, twilio_sender

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("login"))

"""
This is the details route. Enter the endpoint to get your details.
You can change the client_number to your number if it's registered on the current account
"""
@app.route("/details", methods=["GET"])
def login():
    criteria = get_twilio_criteria()
    #All this does is return JSON for you to use as headers
    return {"save these as headers, you can substitute the values with yours": criteria}


"""
This is the incoming SMS endpoint, it listens for your SMS and replies accordingly if your number is registered.
This endpoint is best left untouched if you're not developing
"""
@app.route("/sms", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our number
    body = request.values.get('Body', None)

    # Determine the right reply for this message
    if body.lower() in ("hello", "hi"):
        message = "Hi from Team-Titans! Send 'CHECK BALANCE' or '1' to see your balance. \nSend 'BYE' or '2' for a goodbye."

    elif body.lower() in ("check balance", '1'):
        message = f"Your balance is {randint(1000,99999)}"

    elif body.lower() in ('bye', "2"):
        message = "Goodbye"

    elif body:
        message = "Invalid message, Type 'HELLO' or 'HI' for a tip"

    #Call the Twilio Responder passing the message to it
    response = twilio_responder(message)
    return response

"""
This endpoint is for sending an SMS to your number using your client app.
Using the headers already set from the "/details" endpoint, all you have to do is send a JSON containing the text body and the client number if you wish to change that
It results in an SMS to the client number if registered with the current account
"""
@app.route("/send", methods=["GET", "POST"])
def outgoing_sms():
    #Checking the request method to proceed if POST
    if request.method == "POST":
        #Calls the function for sending the text
        response = twilio_sender(request)
        return response

    #return JSON with criteria to fill
    return { "Fill out the text body and client number if empty and submit as JSON": dict(sender=request.headers.get('sender'),
                                                                                          reciever=request.headers.get("receiver"),
                                                                                          text="")
            }
        

