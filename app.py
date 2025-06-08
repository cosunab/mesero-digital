from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Clave de OpenAI desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "")
    response = MessagingResponse()
    msg = response.message()

    # Consulta a OpenAI
    try:
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un mesero virtual, atento, amable, y puedes hablar en cualquier idioma según el cliente."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = chat_response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Lo siento, hubo un problema. Intenta de nuevo más tarde."

    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)





