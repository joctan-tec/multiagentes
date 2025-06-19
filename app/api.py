from agents.graphs import construir_grafo_multiagente
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def init_page():
    return render_template("app/web/index.html")

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    # Si no viene eL id del mensaje anterior, se puede omitir
    previous_response = data.get('previous_response', None)
    if previous_response is not None:
        print(f"Previous response: {previous_response}")

    grafo = construir_grafo_multiagente(previous_response)
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
    app.run(debug=True, host="0.0.0.0", port=5000)