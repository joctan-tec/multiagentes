from flask import Flask, request, jsonify
from flask_cors import CORS

from open_ai_conf import get_openai_client


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    # Si no viene eL id del mensaje anterior, se puede omitir
    previous_response_id = data.get('previous_response_id', None)
    if previous_response_id is not None:
        print(f"Previous response ID: {previous_response_id}")
    
    print("Mensaje anterior  ----------------" ,previous_response_id)

    # Here you would typically call the OpenAI API with the provided message
    # For demonstration, we will just echo back the message
    openai_client = get_openai_client()
    
    if previous_response_id:
        chatgpt_response = openai_client.responses.create(
            model="gpt-4o-mini",
            input=data['message'],
            previous_response_id=previous_response_id
        )
        
    else:
        chatgpt_response = openai_client.responses.create(
            model="gpt-4o-mini",
            input=data['message'],
        )
    
    response = {
        "message": f"You said: {data['message']}",
        "chatgpt_response": chatgpt_response.output_text if chatgpt_response else "No response from ChatGPT",
        "previous_response_id": chatgpt_response.id if chatgpt_response else None
    }
    print(f"ChatGPT response: {chatgpt_response}")
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)