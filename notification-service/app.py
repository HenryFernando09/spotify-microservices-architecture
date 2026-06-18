from flask import Flask, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración básica para el envío de correos (notificaciones)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com' 
app.config['MAIL_PASSWORD'] = 'tu_contraseña'        

mail = Mail(app)

@app.route('/')
def home():
    return jsonify({"mensaje": "Servicio de Notificaciones Activo"}), 200

# Ruta principal para recibir alertas de otros microservicios
@app.route('/notificar', methods=['POST'])
def enviar_notificacion():
    datos = request.get_json()
    
    # Validamos que nos envíen un correo y un mensaje
    destino = datos.get('correo')
    asunto = datos.get('asunto', 'Alerta del Sistema')
    contenido = datos.get('mensaje')
    
    if not destino or not contenido:
        return jsonify({"error": "Faltan datos requeridos (correo o mensaje)"}), 400
        
    try:
        # Creamos y enviamos el correo electrónico
        msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[destino])
        msg.body = contenido
        mail.send(msg)
        return jsonify({"estado": "Notificación enviada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo enviar la notificación: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
