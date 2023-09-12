from flask import Flask, request, jsonify
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import random

app = Flask(__name__)

# Initialize the CSV data and the language model
csv_data = {}

# Initialize the LLM model and tokenizer
model_name = "EleutherAI/gpt-neo-1.3B"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


@app.route('/test', methods=['GET'])
def Test():
        print("hello test")
        return jsonify({"message": "Test Passed"})

# API endpoint for uploading CSV file
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    print(file)
    
    if file:
        df = pd.read_csv(file)
        csv_data['titles'] = df['title'].tolist()
        csv_data['contents'] = df['content'].tolist()
        return jsonify({"message": "CSV file uploaded successfully"})
    else:
        return jsonify({"message": "No file uploaded"})

# API endpoint for generating essays based on user prompts
@app.route('/generate_essay', methods=['POST'])
def generate_essay():
    data = request.get_json()
    user_prompt = data['prompt']
    generated_essay = generate_essay_from_prompt(user_prompt)
    return jsonify({"essay": generated_essay})

# Function to generate an essay from a user prompt
def generate_essay_from_prompt(user_prompt):
    # Select a random title and content from the CSV data
    if 'titles' in csv_data and 'contents' in csv_data:
        title = random.choice(csv_data['titles'])
        content = random.choice(csv_data['contents'])
    else:
        title = ""
        content = ""

    # Generate essay content using the LLM model
    input_text = f"Title: {title}\n\nPrompt: {user_prompt}\n\nContent: {content}"
    max_length = 500  # Adjust this based on your desired essay length

    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    generated_essay = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_essay

if __name__ == '__main__':
    app.run(debug=True)
