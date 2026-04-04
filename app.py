from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Разрешаем CORS, чтобы фронтенд мог делать fetch с любого домена
players = {}

def get_player(chat_id):
    if chat_id not in players:
        players[chat_id] = {"hp": 3, "level": 0}
    return players[chat_id]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/start', methods=['POST'])
def start():
    chat_id = str(request.json["chat_id"])
    player = get_player(chat_id)
    player["hp"] = 3
    player["level"] = 0
    return jsonify({
        "text": "🏺 Ты вошёл в пирамиду! Выбери парное или непарное:",
        "buttons": ["even", "odd"]
    })

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    chat_id = str(data["chat_id"])
    choice = data["choice"]

    player = get_player(chat_id)
    number = random.randint(1, 10)
    result = "even" if number % 2 == 0 else "odd"

    build_level = False
    if choice == result:
        player["level"] += 1
        build_level = True
        text = f"✅ {number} — угадал! Уровень: {player['level']}"
    else:
        player["hp"] -= 1
        text = f"❌ {number} — не угадал! ❤️ {player['hp']}"

    if player["hp"] <= 0:
        return jsonify({"text": "💀 Ты проиграл", "buttons": ["restart"]})

    if player["level"] >= 5:
        return jsonify({"text": "🏆 Победа!", "buttons": ["restart"]})

    return jsonify({"text": text, "buttons": ["even", "odd"], "build_level": build_level})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
