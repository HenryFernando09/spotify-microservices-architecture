from flask import Flask, jsonify, request
import mysql.connector
import time
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

# --- Canciones populares locales (busqueda instantanea) ---
CANCIONES_POPULARES = [
    {"titulo": "Blinding Lights", "artista": "The Weeknd", "album": "After Hours"},
    {"titulo": "Shape of You", "artista": "Ed Sheeran", "album": "Divide"},
    {"titulo": "Bohemian Rhapsody", "artista": "Queen", "album": "A Night at the Opera"},
    {"titulo": "Levitating", "artista": "Dua Lipa", "album": "Future Nostalgia"},
    {"titulo": "Stay", "artista": "The Kid LAROI & Justin Bieber", "album": "F*CK LOVE 3"},
    {"titulo": "Peaches", "artista": "Justin Bieber", "album": "Justice"},
    {"titulo": "Good 4 U", "artista": "Olivia Rodrigo", "album": "SOUR"},
    {"titulo": "drivers license", "artista": "Olivia Rodrigo", "album": "SOUR"},
    {"titulo": "Montero", "artista": "Lil Nas X", "album": "Montero"},
    {"titulo": "Industry Baby", "artista": "Lil Nas X", "album": "Montero"},
    {"titulo": "Save Your Tears", "artista": "The Weeknd", "album": "After Hours"},
    {"titulo": "Dynamite", "artista": "BTS", "album": "Dynamite"},
    {"titulo": "Butter", "artista": "BTS", "album": "Butter"},
    {"titulo": "Permission to Dance", "artista": "BTS", "album": "Permission to Dance"},
    {"titulo": "As It Was", "artista": "Harry Styles", "album": "Harry's House"},
    {"titulo": "Watermelon Sugar", "artista": "Harry Styles", "album": "Fine Line"},
    {"titulo": "Anti-Hero", "artista": "Taylor Swift", "album": "Midnights"},
    {"titulo": "Shake It Off", "artista": "Taylor Swift", "album": "1989"},
    {"titulo": "Blank Space", "artista": "Taylor Swift", "album": "1989"},
    {"titulo": "Bad Blood", "artista": "Taylor Swift", "album": "1989"},
    {"titulo": "Cruel Summer", "artista": "Taylor Swift", "album": "Lover"},
    {"titulo": "Bad Guy", "artista": "Billie Eilish", "album": "When We All Fall Asleep"},
    {"titulo": "Happier Than Ever", "artista": "Billie Eilish", "album": "Happier Than Ever"},
    {"titulo": "Flowers", "artista": "Miley Cyrus", "album": "Endless Summer Vacation"},
    {"titulo": "Unholy", "artista": "Sam Smith & Kim Petras", "album": "Gloria"},
    {"titulo": "Heat Waves", "artista": "Glass Animals", "album": "Dreamland"},
    {"titulo": "Easy On Me", "artista": "Adele", "album": "30"},
    {"titulo": "Hello", "artista": "Adele", "album": "25"},
    {"titulo": "Rolling in the Deep", "artista": "Adele", "album": "21"},
    {"titulo": "Someone Like You", "artista": "Adele", "album": "21"},
    {"titulo": "Uptown Funk", "artista": "Mark Ronson ft. Bruno Mars", "album": "Uptown Special"},
    {"titulo": "That's What I Like", "artista": "Bruno Mars", "album": "24K Magic"},
    {"titulo": "Locked Out of Heaven", "artista": "Bruno Mars", "album": "Unorthodox Jukebox"},
    {"titulo": "Despacito", "artista": "Luis Fonsi ft. Daddy Yankee", "album": "Vida"},
    {"titulo": "Con Calma", "artista": "Daddy Yankee", "album": "Con Calma"},
    {"titulo": "Gasolina", "artista": "Daddy Yankee", "album": "Barrio Fino"},
    {"titulo": "Tusa", "artista": "Karol G & Nicki Minaj", "album": "Tusa"},
    {"titulo": "Bichota", "artista": "Karol G", "album": "KG0516"},
    {"titulo": "MAMIII", "artista": "Becky G & Karol G", "album": "MAMIII"},
    {"titulo": "Hawai", "artista": "Maluma", "album": "Papi Juancho"},
    {"titulo": "Dakiti", "artista": "Bad Bunny & Jhay Cortez", "album": "El Ultimo Tour Del Mundo"},
    {"titulo": "Yonaguni", "artista": "Bad Bunny", "album": "El Ultimo Tour Del Mundo"},
    {"titulo": "Me Porto Bonito", "artista": "Bad Bunny & Chencho Corleone", "album": "Un Verano Sin Ti"},
    {"titulo": "Noche de Anoche", "artista": "Bad Bunny & Rosalia", "album": "El Ultimo Tour Del Mundo"},
    {"titulo": "Motomami", "artista": "Rosalia", "album": "Motomami"},
    {"titulo": "Shakira: Bzrp Music Sessions 53", "artista": "Bizarrap & Shakira", "album": "Bzrp Music Sessions"},
    {"titulo": "Waka Waka", "artista": "Shakira", "album": "She Wolf"},
    {"titulo": "Hips Don't Lie", "artista": "Shakira ft. Wyclef Jean", "album": "Oral Fixation"},
    {"titulo": "Thriller", "artista": "Michael Jackson", "album": "Thriller"},
    {"titulo": "Billie Jean", "artista": "Michael Jackson", "album": "Thriller"},
    {"titulo": "Beat It", "artista": "Michael Jackson", "album": "Thriller"},
    {"titulo": "Smells Like Teen Spirit", "artista": "Nirvana", "album": "Nevermind"},
    {"titulo": "Hotel California", "artista": "Eagles", "album": "Hotel California"},
    {"titulo": "Stairway to Heaven", "artista": "Led Zeppelin", "album": "Led Zeppelin IV"},
    {"titulo": "Sweet Child O Mine", "artista": "Guns N Roses", "album": "Appetite for Destruction"},
    {"titulo": "November Rain", "artista": "Guns N Roses", "album": "Use Your Illusion I"},
    {"titulo": "Lose Yourself", "artista": "Eminem", "album": "8 Mile Soundtrack"},
    {"titulo": "Without Me", "artista": "Eminem", "album": "The Eminem Show"},
    {"titulo": "Stan", "artista": "Eminem", "album": "The Marshall Mathers LP"},
    {"titulo": "God's Plan", "artista": "Drake", "album": "Scorpion"},
    {"titulo": "One Dance", "artista": "Drake", "album": "Views"},
    {"titulo": "Hotline Bling", "artista": "Drake", "album": "Views"},
    {"titulo": "SICKO MODE", "artista": "Travis Scott", "album": "Astroworld"},
    {"titulo": "Rockstar", "artista": "Post Malone", "album": "Beerbongs & Bentleys"},
    {"titulo": "Sunflower", "artista": "Post Malone & Swae Lee", "album": "Spider-Man: Into the Spider-Verse"},
    {"titulo": "Circles", "artista": "Post Malone", "album": "Hollywood's Bleeding"},
    {"titulo": "Old Town Road", "artista": "Lil Nas X ft. Billy Ray Cyrus", "album": "7 EP"},
    {"titulo": "We Will Rock You", "artista": "Queen", "album": "News of the World"},
    {"titulo": "Don't Stop Me Now", "artista": "Queen", "album": "Jazz"},
    {"titulo": "Under Pressure", "artista": "Queen & David Bowie", "album": "Hot Space"},
    {"titulo": "Let It Be", "artista": "The Beatles", "album": "Let It Be"},
    {"titulo": "Hey Jude", "artista": "The Beatles", "album": "Hey Jude"},
    {"titulo": "Come Together", "artista": "The Beatles", "album": "Abbey Road"},
    {"titulo": "Yesterday", "artista": "The Beatles", "album": "Help!"},
    {"titulo": "Imagine", "artista": "John Lennon", "album": "Imagine"},
    {"titulo": "Superstition", "artista": "Stevie Wonder", "album": "Talking Book"},
    {"titulo": "Purple Rain", "artista": "Prince", "album": "Purple Rain"},
    {"titulo": "We dont talk anymore", "artista": "Charlie Puth", "album": "Nine Track Mind"},
    {"titulo": "Attention", "artista": "Charlie Puth", "album": "Voicenotes"},
    {"titulo": "See You Again", "artista": "Wiz Khalifa ft. Charlie Puth", "album": "Furious 7 Soundtrack"},
    {"titulo": "Perfect", "artista": "Ed Sheeran", "album": "Divide"},
    {"titulo": "Thinking Out Loud", "artista": "Ed Sheeran", "album": "X"},
    {"titulo": "Photograph", "artista": "Ed Sheeran", "album": "X"},
]

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

@app.route('/canciones/<int:id>', methods=['DELETE'])
def delete_cancion(id):
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
    q = request.args.get('q', '').strip().lower()
    if len(q) < 2:
        return jsonify({"resultados": [], "fuente": "none"})

    # 1. Busqueda local instantanea (por titulo O artista)
    locales = [
        c for c in CANCIONES_POPULARES
        if q in c["titulo"].lower() or q in c["artista"].lower()
    ][:6]

    if locales:
        return jsonify({"resultados": locales, "fuente": "local"})

    # 2. Si no hay resultados locales, consulta MusicBrainz como respaldo
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
.badge { font-size: 0.65rem; background: #1DB954; color: #fff; border-radius: 4px;
         padding: 1px 6px; margin-left: 6px; vertical-align: middle; }
.badge.mb { background: #553c9a; }
</style>
</head>
<body>
<div class="header">
<h1>&#127925; Music Service — Running</h1>
<p>Microservicio de canciones · Puerto 5001 · Sugerencias: canciones populares + MusicBrainz</p>
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
        `<div class="sugerencia" onclick="seleccionar(${i})">
          <strong>${r.titulo} <span class="badge ${esLocal ? '' : 'mb'}">${esLocal ? 'Popular' : 'MusicBrainz'}</span></strong>
          <small>${r.artista}${r.album ? ' — ' + r.album : ''}</small>
        </div>`
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

document.addEventListener('click', (e) => {
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
  document.getElementById('lista').innerHTML = data.canciones.map(c =>
    `<div class="song">
      <span><strong>${c.titulo}</strong> — ${c.artista}${c.album ? ' (' + c.album + ')' : ''}</span>
      <button class="btn-delete" onclick="eliminar(${c.id})">Eliminar</button>
    </div>`
  ).join('');
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
    body: JSON.stringify({titulo, artista, album})
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