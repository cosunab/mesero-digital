import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import openai

# Configura tu clave de OpenAI desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")

    response = MessagingResponse()

    if not incoming_msg:
        response.message("No entendí tu mensaje. ¿Puedes repetirlo?")
        return str(response)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un mesero virtual amigable que ayuda a los clientes a elegir su comida. Hablas el idioma del cliente y conoces el menú."
                },
                {
                    "role": "user",
                    "content": incoming_msg
                }
            ]
        )
        answer = completion.choices[0].message.content.strip()
        response.message(answer)
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        response.message("Lo siento, hubo un problema. Intenta de nuevo más tarde.")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

