from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        message = request.form.get("Body")
        sender = request.form.get("From")

        print(f"✅ Webhook recibido de {sender}")
        print(f"Mensaje recibido: {message}")

        # Crear respuesta TwiML
        resp = MessagingResponse()
        twiml_response = str(resp.message("¡Hola! Soy tu mesero virtual. ¿En qué puedo ayudarte hoy?"))

        return Response(twiml_response, mimetype="application/xml")
    except Exception as e:
        print("❌ Error procesando mensaje:", e)
        return "Error", 500

if __name__ == "__main__":
    app.run(debug=True)



