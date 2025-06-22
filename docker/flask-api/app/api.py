from app.graphs import GrafoMultiagente
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.text_processor.load_pdf import main as load_pdf

app = Flask(__name__)
CORS(app)

'''
Este es un sistema legal multiagente que utiliza Flask para crear una API RESTful.
Los agentes trabajan juntos para responder preguntas legales utilizando técnicas avanzadas de procesamiento de lenguaje natural.
El endpoint principal es `/chatgpt`, que recibe preguntas legales en formato JSON y devuelve respuestas generadas por el sistema multiagente.
'''
@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bienvenido al Sistema Legal Multiagente</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #121212;
                color: #e0e0e0;
                padding: 20px;
            }
            .container {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                max-width: 800px;
                margin: auto;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            }
            h1, h2, h3 {
                color: #ffffff;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin-bottom: 10px;
            }
            code, pre {
                background-color: #2d2d2d;
                color: #c5f6fa;
                padding: 4px 8px;
                border-radius: 6px;
                font-family: monospace;
            }
            a {
                color: #80cbc4;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido al Sistema Legal Multiagente</h1>
            <p>Este sistema utiliza múltiples agentes inteligentes que actúan como asistentes legales para analizar y responder preguntas jurídicas utilizando técnicas avanzadas de procesamiento de lenguaje natural.</p>
            
            <h2>Endpoints disponibles</h2>
            <ul>
                <li><strong><code>GET /</code></strong>: Muestra esta página de bienvenida.</li>
                <li><strong><code>POST /chatgpt</code></strong>: Envía una pregunta legal en formato JSON y recibe una respuesta generada por el sistema multiagente.</li>
            </ul>
            
            <h3>Ejemplo de uso del endpoint <code>/chatgpt</code>:</h3>
            <pre>{
    "message": "¿Cuáles son los requisitos para iniciar un juicio laboral?",
    "previous_response": null
}</pre>
        </div>
    </body>
    </html>
    """
    return html_content
    
'''
Endpoint para interactuar con el sistema multiagente.

Args:
    message (str): Pregunta legal que el usuario desea hacer.
    previous_response (str, optional): Respuesta previa del analista para continuar el flujo.
Returns:
    JSON con la respuesta generada por el sistema multiagente.
'''
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    # Si no viene eL id del mensaje anterior, se puede omitir
    previous_response = data.get('previous_response', None)
    if previous_response is not None:
        print(f"Previous response: {previous_response}")

    grafo = GrafoMultiagente().construir_grafo_multiagente(previous_response)
    estado_inicial = {"pregunta": data['message']}
    resultado = grafo.invoke(estado_inicial)

    print("\nRespuesta final al usuario:")
    print(resultado["respuesta_final"])
    
    response = {
        "message": f"You said: {data['message']}",
        "chatgpt_response": resultado["respuesta_final"] if resultado["respuesta_final"] else "No response from ChatGPT",
        "previous_response": resultado['respuesta_final']
    }
    print(f"ChatGPT response: {resultado['respuesta_final']}")
    
    return jsonify(response)


if __name__ == "__main__":
    load_pdf()  # Cargar los PDFs al iniciar la aplicación
    app.run(debug=True, host="0.0.0.0", port=5000)