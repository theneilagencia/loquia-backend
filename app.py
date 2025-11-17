
# app.py limpo e corrigido
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import jwt
from supabase import create_client
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = Flask(__name__)
CORS(app)

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:8]}... (truncated)")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT Secret
JWT_SECRET = os.getenv("JWT_SECRET", "loquia")

# Rota para testar conexão com Supabase
@app.get("/supabase/test")
def supabase_test():
    try:
        response = supabase.auth.get_user()
        return jsonify({"status": "ok", "supabase_response": str(response)}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# Health check
@app.get("/health")
def health():
    return jsonify({"status": "ok"})

# Rota de cadastro de usuário
@app.post("/auth/signup")
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios."}), 400

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.get("error"):
            return jsonify({"error": response["error"]}), 400
        return jsonify({"message": "Usuário cadastrado com sucesso.", "user": response["user"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
