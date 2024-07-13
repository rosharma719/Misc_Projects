from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize the OpenAI client with the API key

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if 'code' not in data or 'source_lang' not in data or 'target_lang' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    source_code = data['code']
    source_lang = data['source_lang']
    target_lang = data['target_lang']

    try:
        translated_code = translate_code(source_code, source_lang, target_lang)
        return jsonify({'translated_code': translated_code})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def translate_code(source_code, source_lang, target_lang):
    messages = [
        {"role": "system", "content": "You translate code."}, 
        {"role": "user", "content": f"Translate the following {source_lang} code to {target_lang}:\n\n{source_code}. Return JUST the code."}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Correct way to access the message from the response
    translated_code = response.choices[0].message.content
    return translated_code

if __name__ == '__main__':
    app.run(debug=True)
