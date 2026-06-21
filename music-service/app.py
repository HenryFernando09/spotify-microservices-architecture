from flask import Flask, jsonify, request
import mysql.connector
import time

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="music123",
        database="music_db"
    )

def init_db():
    for intento in range(10):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS canciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    artista VARCHAR(255) NOT NULL,
                    album VARCHAR(255)
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Base de datos lista")
            return
        except mysql.connector.Error as err:
            print(f"Esperando a MySQL... intento {intento+1}: {err}")
            time.sleep(3)

@app.route('/')
def inicio():
    return jsonify({"service": "Music Service", "status": "running"})

@app.route('/canciones', methods=['GET'])
def get_canciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canciones")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"canciones": resultado})

@app.route('/canciones', methods=['POST'])
def add_cancion():
    data = request.get_json()
    titulo = data.get("titulo")
    artista = data.get("artista")
    album = data.get("album")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO canciones (titulo, artista, album) VALUES (%s, %s, %s)",
        (titulo, artista, album)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Canción agregada",
        "cancion": {"id": nuevo_id, "titulo": titulo, "artista": artista, "album": album}
    }), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
