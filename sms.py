from flask import Flask, request, redirect, make_response, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from random import randint

app = Flask(__name__)

"""
This is the details route. Enter the endpoint to get your details.
You can change the client_number to your number if it's registered on the current account
"""
@app.route("/details", methods=["GET"])
def login():
    account_sid = 'ACff897b8003c8a71345d7a1a148c54b00'
    auth_token = 'e4bb1a71b4d8bb5c482ffb69bf1b4659'
    twilio_number = '+12018906264'
    client_number = '+2348078000877'

    #All this does is return JSON for you to use as headers
    return {"save these as headers": dict(account_sid=account_sid,
                auth_token=auth_token,
                twilio_number=twilio_number,
                client_number=client_number)}

"""
This is the incoming SMS endpoint, it listens for your SMS and replies accordingly if your number is registered.
This endpoint is best left untouched if you're not developing
"""
@app.route("/sms", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    #body = "hello"
    print(body)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body.lower() in ("hello", "hi"):
        resp.message("Hi from Team-Titans! Send 'CHECK BALANCE' or '1' to see your balance. \nSend 'BYE' or '2' for a goodbye.")
    elif body.lower() in ("check balance", '1'):
        resp.message(f"Your balance is {randint(1000,99999)}")
    elif body.lower() in ('bye', "2"):
        resp.message("Goodbye")
    elif body:
        resp.message("Invalid message, Type 'HELLO' or 'HI' for a tip")

    print(str(resp))

    return str(resp)

"""
This endpoint is for sending an SMS to your number using your client app.
Using the headers already set from the "/details" endpoint, all you have to do is send a JSON containing the text body and the client number if you wish to change that
It results in an SMS to the client number if registered with the current account
"""
@app.route("/send", methods=["GET", "POST"])
def outgoing_sms():
    #Checking the request method to proceed if POST
    if request.method == "POST":
        json = request.get_json()
        get = request.headers.get

        #A list of criteria so the endpoint doesn't return a 500 response should the client have missed a criteria
        criteria = [get("auth_token"), get("account_sid"), 
                    get("twilio_number"), json.get("text"), 
                    (json.get("client_number") or get("client_number"))]
        if not all(criteria):

            #return a JSON containing the error message if criteria are missing
            return dict(error = {"message": "Missing Criteria. Make sure all headers are set and the text and client number"}), 400

        #set all the variables to be used in the Twilio request 
        text = json["text"]
        client_number = request.headers.get("client_number") if request.headers.get("client_number")\
            else json["client_number"]
        twilio_number = request.headers.get("twilio_number")
        account_sid = request.headers.get("account_sid")
        auth_token = request.headers.get("auth_token")

        #Creating the Client Object to send the SMS
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                        body= text,
                        from_= twilio_number,
                        to= client_number
                    )

        #Sending the SMS
        print(message.sid)
        return dict(text = text,
                    sender = twilio_number,
                    recipient = client_number,
                    status="sent")

    #return a JSON with criteria to fill
    return { "Fill out the text body and client number if empty and submit as JSON": dict(client_number=request.headers.get('client_number'),
                                                                        text="")
            }
        

if __name__ == "__main__":
    app.run(debug=True)
