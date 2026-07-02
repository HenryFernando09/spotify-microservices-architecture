from flask import Flask, jsonify, request
import mysql.connector
import time
import urllib.request
import urllib.parse
import json

from catalogo import CANCIONES_POPULARES

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host="172.17.0.2",
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
    """Verificacion rapida de que el servicio esta activo."""
    return jsonify({"service": "Music Service", "status": "running"})


@app.route('/canciones', methods=['GET'])
def get_canciones():
    """Devuelve todas las canciones almacenadas en MySQL."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canciones")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"canciones": resultado})


@app.route('/canciones', methods=['POST'])
def add_cancion():
    """Agrega una nueva cancion a MySQL."""
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


@app.route('/canciones/<int:id>', methods=['DELETE'])
def delete_cancion(id):
    """Elimina una cancion de MySQL por su id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM canciones WHERE id = %s", (id,))
    conn.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return jsonify({"message": "Cancion no encontrada"}), 404
    return jsonify({"message": "Cancion eliminada"}), 200


@app.route('/buscar', methods=['GET'])
def buscar_canciones():
    """
    Busqueda de canciones en dos etapas:
    1. Busqueda instantanea en el catalogo local (CANCIONES_POPULARES).
    2. Si no hay resultados locales, consulta MusicBrainz como respaldo.
    """
    q = request.args.get('q', '').strip().lower()
    if len(q) < 2:
        return jsonify({"resultados": [], "fuente": "none"})

    locales = [
        c for c in CANCIONES_POPULARES
        if q in c["titulo"].lower() or q in c["artista"].lower()
    ][:6]

    if locales:
        return jsonify({"resultados": locales, "fuente": "local"})

    try:
        query = urllib.parse.quote(q)
        url = f"https://musicbrainz.org/ws/2/recording/?query={query}&limit=6&fmt=json"
        req = urllib.request.Request(url, headers={
            "User-Agent": "MusicServiceApp/1.0 (leidi@ucsur.edu.pe)"
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        resultados = []
        for r in data.get("recordings", []):
            titulo = r.get("title", "")
            artista = r.get("artist-credit", [{}])[0].get("name", "") if r.get("artist-credit") else ""
            releases = r.get("releases", [])
            album = releases[0].get("title", "") if releases else ""
            if titulo and artista:
                resultados.append({"titulo": titulo, "artista": artista, "album": album})

        return jsonify({"resultados": resultados, "fuente": "musicbrainz"})

    except Exception:
        return jsonify({"resultados": [], "fuente": "error"})


@app.route('/ui')
def interfaz():
    """Interfaz web para gestionar canciones desde el navegador."""
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
.input-wrap { position: relative; }
input { background: #0f1117; border: 1px solid #2d3748; border-radius: 8px; padding: 10px; color: #e2e8f0; width: 100%; }
input:focus { outline: none; border-color: #1DB954; }
button { background: #1DB954; color: #fff; border: none; border-radius: 8px; padding: 10px; width: 100%; font-weight: 600; cursor: pointer; transition: background 0.2s; }
button:hover { background: #17a349; }
.song { background: #0f1117; border: 1px solid #2d3748; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;
        display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.song span { flex: 1; }
.btn-delete { background: #e53e3e; color: #fff; border: none; border-radius: 6px; padding: 8px 14px;
              font-weight: 600; cursor: pointer; width: auto; flex-shrink: 0; transition: background 0.2s; }
.btn-delete:hover { background: #c53030; }
.sugerencias { position: absolute; top: 100%; left: 0; right: 0; background: #1a1f2e;
               border: 1px solid #1DB954; border-radius: 0 0 8px 8px; z-index: 100;
               max-height: 260px; overflow-y: auto; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
.sugerencia { padding: 10px 14px; cursor: pointer; border-bottom: 1px solid #2d3748; }
.sugerencia:hover { background: #1DB95422; }
.sugerencia strong { color: #e2e8f0; font-size: 0.9rem; }
.sugerencia small { color: #718096; display: block; font-size: 0.78rem; margin-top: 2px; }
.badge { font-size: 0.65rem; background: #1DB954; color: #fff; border-radius: 4px; padding: 1px 6px; margin-left: 6px; vertical-align: middle; }
.badge.mb { background: #553c9a; }
</style>
</head>
<body>
<div class="header">
<h1>&#127925; Music Service — Running</h1>
<p>Microservicio de canciones · Puerto 5001 · Sugerencias: catalogo popular + MusicBrainz</p>
</div>

<div class="card">
<h2>Agregar cancion</h2>
<div class="grid">
  <div class="input-wrap">
    <input id="titulo" placeholder="Titulo — escribe para buscar..." oninput="buscar(this.value)" autocomplete="off">
    <div class="sugerencias" id="sugerencias" style="display:none"></div>
  </div>
  <input id="artista" placeholder="Artista">
  <input id="album" placeholder="Album">
</div>
<button onclick="agregar()">+ Agregar cancion</button>
</div>

<div class="card">
<h2>Canciones en MySQL</h2>
<div id="lista">Cargando...</div>
</div>

<script>
let timer = null;

async function buscar(q) {
  clearTimeout(timer);
  const box = document.getElementById('sugerencias');
  if (q.length < 2) { box.style.display = 'none'; return; }
  timer = setTimeout(async () => {
    try {
      const res = await fetch('/buscar?q=' + encodeURIComponent(q));
      const data = await res.json();
      if (!data.resultados.length) { box.style.display = 'none'; return; }
      const esLocal = data.fuente === 'local';
      box.innerHTML = data.resultados.map((r, i) =>
        '<div class="sugerencia" onclick="seleccionar(' + i + ')">' +
        '<strong>' + r.titulo + ' <span class="badge ' + (esLocal ? '' : 'mb') + '">' + (esLocal ? 'Popular' : 'MusicBrainz') + '</span></strong>' +
        '<small>' + r.artista + (r.album ? ' — ' + r.album : '') + '</small>' +
        '</div>'
      ).join('');
      box.style.display = 'block';
      box._data = data.resultados;
    } catch(e) { box.style.display = 'none'; }
  }, 250);
}

function seleccionar(i) {
  const r = document.getElementById('sugerencias')._data[i];
  document.getElementById('titulo').value = r.titulo;
  document.getElementById('artista').value = r.artista;
  document.getElementById('album').value = r.album || '';
  document.getElementById('sugerencias').style.display = 'none';
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.input-wrap'))
    document.getElementById('sugerencias').style.display = 'none';
});

async function cargar() {
  const res = await fetch('/canciones');
  const data = await res.json();
  if (!data.canciones.length) {
    document.getElementById('lista').innerHTML = '<p style="color:#718096;padding:8px">No hay canciones aun. Agrega una arriba.</p>';
    return;
  }
  document.getElementById('lista').innerHTML = data.canciones.map(function(c) {
    return '<div class="song">' +
      '<span><strong>' + c.titulo + '</strong> — ' + c.artista + (c.album ? ' (' + c.album + ')' : '') + '</span>' +
      '<button class="btn-delete" onclick="eliminar(' + c.id + ')">Eliminar</button>' +
      '</div>';
  }).join('');
}

async function eliminar(id) {
  if (!confirm('Eliminar esta cancion?')) return;
  await fetch('/canciones/' + id, { method: 'DELETE' });
  cargar();
}

async function agregar() {
  const titulo = document.getElementById('titulo').value.trim();
  const artista = document.getElementById('artista').value.trim();
  const album = document.getElementById('album').value.trim();
  if (!titulo || !artista) return;
  await fetch('/canciones', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({titulo: titulo, artista: artista, album: album})
  });
  document.getElementById('titulo').value = '';
  document.getElementById('artista').value = '';
  document.getElementById('album').value = '';
  document.getElementById('sugerencias').style.display = 'none';
  cargar();
}

cargar();
</script>
</body>
</html>"""


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)