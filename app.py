from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()
    msg = response.message()

    if "hola" in incoming_msg:
        msg.body("¡Hola! Soy tu mesero virtual. ¿En qué puedo ayudarte hoy?")
    else:
        msg.body("No entendí tu mensaje. ¿Puedes repetirlo, por favor?")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)




