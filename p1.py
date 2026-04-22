from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Compiler Backend Running"


@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "")
    user_input = data.get("input", "")

    try:
        # =========================
        # 🟢 PYTHON EXECUTION
        # =========================
        if language == "python":
            with open("temp.py", "w") as f:
                f.write(code)

            result = subprocess.run(
                ["python", "temp.py"],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=5
            )

            return jsonify({
                "output": result.stdout,
                "error": result.stderr
            })

        # =========================
        # 🔴 C EXECUTION
        # =========================
        elif language == "c":
            with open("temp.c", "w") as f:
                f.write(code)

            try:
                # Compile C code
                compile_process = subprocess.run(
                    ["gcc", "temp.c", "-o", "temp.exe"],
                    capture_output=True,
                    text=True
                )

                # If compilation fails → return error
                if compile_process.returncode != 0:
                    return jsonify({
                        "output": "",
                        "error": compile_process.stderr
                    })

                # Run executable
                result = subprocess.run(
                    ["temp.exe"],
                    input=user_input,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                return jsonify({
                    "output": result.stdout,
                    "error": result.stderr
                })

            except Exception as e:
                # Handles gcc not found or execution issues
                return jsonify({
                    "output": "",
                    "error": str(e)
                })

        # =========================
        # ❌ INVALID LANGUAGE
        # =========================
        else:
            return jsonify({
                "output": "",
                "error": "Unsupported language"
            })

    except subprocess.TimeoutExpired:
        return jsonify({
            "output": "",
            "error": "Execution timed out"
        })

    except Exception as e:
        return jsonify({
            "output": "",
            "error": str(e)
        })


# =========================
# 🚀 REQUIRED FOR RENDER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)