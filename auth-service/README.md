# Auth Service

Microservicio encargado de la autenticación de usuarios dentro de la arquitectura de microservicios del proyecto Spotify Microservices Architecture.

## Funcionalidades implementadas

* Verificación del estado del servicio
* Consulta de usuarios registrados
* Registro de usuarios
* Inicio de sesión
* Comunicación HTTP mediante Flask
* Intercambio de datos en formato JSON

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

Body JSON:

{
  "username": "henry",
  "password": "123456"
}



### Inicio de sesión

POST http://127.0.0.1:5000/login

Body JSON:

{
  "username": "henry",
  "password": "123456"
}



## Nota

Los endpoints POST `/register` y `/login` deben probarse utilizando Thunder Client o Postman, ya que requieren el envío de datos JSON en el cuerpo de la solicitud HTTP.

## Ejecución con Docker

Construir la imagen:

```bash
sudo docker build -t auth-service .
```

Ejecutar el contenedor:

```bash
sudo docker run -p 5000:5000 auth-service
```

Luego acceder a:

```text
http://127.0.0.1:5000/
```

## Validación en Ubuntu Server mediante Docker

El microservicio Auth Service fue exportado como imagen Docker utilizando un archivo `.tar` y posteriormente ejecutado exitosamente en una máquina virtual Ubuntu Server sin necesidad de instalar Python ni Flask manualmente.

Se validó el correcto funcionamiento de los siguientes endpoints:

- GET /
- GET /users
- POST /register
- POST /login

La validación se realizó utilizando comandos `curl` directamente desde Ubuntu Server, comprobando la portabilidad y encapsulamiento del entorno mediante Docker.
