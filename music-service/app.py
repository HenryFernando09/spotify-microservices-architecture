from flask import Flask, jsonify, request

app = Flask(__name__)

canciones = []

@app.route('/')
def inicio():
    return jsonify({"service": "Music Service", "status": "running"})

@app.route('/canciones', methods=['GET'])
def get_canciones():
    return jsonify({"canciones": canciones})

@app.route('/canciones', methods=['POST'])
def add_cancion():
    data = request.get_json()
    cancion = {
        "titulo": data.get("titulo"),
        "artista": data.get("artista"),
        "album": data.get("album")
    }
    canciones.append(cancion)
    return jsonify({"message": "Canción agregada", "cancion": cancion}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

