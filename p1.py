from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Compiler Backend Running"

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code')
    language = request.json.get('language')
    user_input = request.json.get('input', '')

    try:
        #  PYTHON
        if language == "python":
            with open("temp.py", "w") as f:
                f.write(code)

            start = time.time()

            result = subprocess.run(
                ["python", "temp.py"],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            end = time.time()

            return jsonify({
                "output": result.stdout,
                "error": result.stderr,
                "time": round(end - start, 4)
            })

        #  C
        elif language == "c":
            with open("temp.c", "w") as f:
                f.write(code)

    # 🔴 Compile step
            compile_process = subprocess.run(
                ["gcc", "temp.c", "-o", "temp.exe"],
                capture_output=True,
                text=True
            )

    # 🔴 IMPORTANT CHECK
            if compile_process.returncode != 0:
                return jsonify({
                    "output": "",
                    "error": compile_process.stderr,
                    "time": 0
                })

    # 🟢 Only runs if compile SUCCESS
            result = subprocess.run(
                ["temp.exe"],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            return jsonify({
                "output": result.stdout,
                "error": result.stderr,
                "time": 0
            })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)