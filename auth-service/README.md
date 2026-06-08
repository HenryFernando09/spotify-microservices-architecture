# Auth Service

Microservicio encargado de la autenticación de usuarios dentro de la arquitectura de microservicios del proyecto.

## Funcionalidades iniciales

* Verificación del estado del servicio
* Respuesta HTTP básica mediante Flask

## Tecnologías

* Python
* Flask

## Endpoints disponibles

### Verificación del servicio

GET http://127.0.0.1:5000/

Respuesta:

{
  "service": "Auth Service",
  "status": "running"
}

### Consulta de usuarios

GET http://127.0.0.1:5000/users


### Registro de usuarios

POST http://127.0.0.1:5000/register

Body:

{
  "username": "henry",
  "password": "123456"
}

### Inicio de sesión

POST http://127.0.0.1:5000/login

Body:

{
  "username": "henry",
  "password": "123456"
}

Nota: Los endpoints POST /register y /login deben probarse con Thunder Client, Postman o curl, ya que requieren enviar datos JSON en el cuerpo de la solicitud.
