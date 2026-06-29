from flask import Flask, jsonify, request
import mysql.connector
import time

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="172.17.0.3",     
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
        "message": "Cancion agregada",
        "cancion": {"id": nuevo_id, "titulo": titulo, "artista": artista, "album": album}
    }), 201

@app.route('/ui')
def interfaz():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Music Service</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: Segoe UI, sans-serif; }
body { background: #0f1117; color: #e2e8f0; padding: 24px; }
.header { background: linear-gradient(135deg, #1DB954, #158a3e); border-radius: 12px; padding: 20px 28px; margin-bottom: 24px; }
.header h1 { color: #fff; font-size: 1.4rem; }
.header p { color: rgba(255,255,255,0.8); font-size: 0.85rem; }
.card { background: #1a1f2e; border: 1px solid #2d3748; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
h2 { color: #a0aec0; font-size: 1rem; margin-bottom: 14px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 12px; }
input { background: #0f1117; border: 1px solid #2d3748; border-radius: 8px; padding: 10px; color: #e2e8f0; width: 100%; }
button { background: #1DB954; color: #fff; border: none; border-radius: 8px; padding: 10px; width: 100%; font-weight: 600; cursor: pointer; }
.song { background: #0f1117; border: 1px solid #2d3748; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; }
.song b { color: #1DB954; }
</style>
</head>
<body>
<div class="header">
<h1>🎵 Music Service - Running</h1>
<p>Microservicio de canciones · Puerto 5001</p>
</div>
<div class="card">
<h2>➕ Agregar cancion</h2>
<div class="grid">
<input id="titulo" placeholder="Titulo"/>
<input id="artista" placeholder="Artista"/>
<input id="album" placeholder="Album"/>
</div>
<button onclick="agregar()">Agregar → POST /canciones</button>
</div>
<div class="card">
<h2>🎧 Canciones en MySQL</h2>
<div id="lista">Cargando...</div>
</div>
<script>
async function cargar() {
const res = await fetch("/canciones");
const data = await res.json();
document.getElementById("lista").innerHTML = data.canciones.map(c =>
"<div class=song><b>#" + c.id + "</b> " + c.titulo + " - " + c.artista + " (" + c.album + ")</div>"
).join("");
}
async function agregar() {
const titulo = document.getElementById("titulo").value;
const artista = document.getElementById("artista").value;
const album = document.getElementById("album").value;
if (!titulo || !artista) return;
await fetch("/canciones", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({titulo: titulo, artista: artista, album: album})
});
document.getElementById("titulo").value = "";
document.getElementById("artista").value = "";
document.getElementById("album").value = "";
cargar();
}
cargar();
</script>
</body>
</html>"""

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
