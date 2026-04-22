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

            compile_process = subprocess.run(
                ["gcc", "temp.c", "-o", "temp.exe"],
                capture_output=True,
                text=True
            )

            if compile_process.returncode != 0:
                return jsonify({
                    "output": "",
                    "error": compile_process.stderr,
                    "time": 0
                })

            start = time.time()

            result = subprocess.run(
                ["temp.exe"],
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

    except subprocess.TimeoutExpired:
        return jsonify({
            "output": "",
            "error": "Execution timed out",
            "time": 0
        })

    except Exception as e:
        return jsonify({
            "output": "",
            "error": str(e),
            "time": 0
        })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)