from flask import Flask, jsonify, request
import subprocess
# CORS
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    prompt = data['prompt']
    try:
        subprocess.run(["python3", "./Llama_index/llama_rag.py", prompt])
        
        data_to_write = ""
        with open("./Llama_index/active_strategy.py", 'r+') as file1:
            # read all the times
            lines = file1.readlines()
            
            data_to_write += f"Prompt:{prompt}\n------------------\n"
            for lineNum, line in enumerate(lines):
                
                if lineNum > 7:
                    data_to_write += line + "\n"
        with open("./Llama_index/testing.txt", "w") as file:
            file.write(data_to_write)
        print(data_to_write)
    except Exception as e:
        return jsonify({"status": "error", "data": str(e)})
    
    return jsonify({"status": "success", "data": data_to_write})

if __name__ == '__main__':
    app.run(port=3000)