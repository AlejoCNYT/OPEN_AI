import os

from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente con la clave API
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Solicitud al modelo
prompt = "Escribe un saludo tipo 'Hello World' con un toque creativo de IA."
response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role": "user", "content": prompt}],
        temperature = 0.6
        )

# Mostrar respuesta
print("Respuesta del modelo:")
print(response.choices[0].message.content)
