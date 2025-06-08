from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Obtener la clave de OpenAI desde las variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')

        if not incoming_msg:
            return _error_response("No se recibió mensaje válido.")

        # Prompt base con instrucciones
        prompt = f"""
Eres un mesero virtual de un restaurante. Estás aquí para ayudar al cliente con sus preguntas sobre el menú, hacer sugerencias y tomar pedidos.

El cliente ha dicho: "{incoming_msg}"
Responde de forma amigable, clara y útil.
"""

        # Generar respuesta con OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        # Responder vía Twilio
        twilio_response = MessagingResponse()
        twilio_response.message(reply)
        return str(twilio_response)

    except Exception as e:
        print("Error:", e)
        return _error_response("Lo siento, hubo un problema. Intenta de nuevo más tarde.")

def _error_response(message):
    twilio_response = MessagingResponse()
    twilio_response.message(message)
    return str(twilio_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

