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

## Integración de SQLite y persistencia de datos

El microservicio `auth-service` fue actualizado para incorporar SQLite como sistema de almacenamiento local persistente, reemplazando el uso temporal de estructuras en memoria. Para ello, se implementó la creación automática de la base de datos `auth.db` y de la tabla `users` mediante la librería `sqlite3` integrada en Python.

Los endpoints `/register`, `/login` y `/users` fueron modificados para interactuar directamente con la base de datos, permitiendo registrar usuarios, validar credenciales y consultar información almacenada de manera persistente.

Durante las pruebas funcionales se validó correctamente:

* Registro de usuarios mediante `POST /register`
* Inicio de sesión mediante `POST /login`
* Consulta de usuarios mediante `GET /users`
* Persistencia de datos después de reiniciar Flask

Asimismo, el archivo `auth.db` fue excluido del repositorio GitHub utilizando `.gitignore`, debido a que corresponde a una base de datos local utilizada únicamente para pruebas y validaciones del microservicio.

## Implementación de seguridad y hash de contraseñas

El `auth-service` fue actualizado para incorporar mecanismos básicos de seguridad en el manejo de credenciales utilizando la librería `werkzeug.security` de Python.

Para ello, se implementaron las funciones `generate_password_hash()` y `check_password_hash()` con el objetivo de evitar el almacenamiento de contraseñas en texto plano dentro de la base de datos SQLite.

El endpoint `/register` fue modificado para cifrar automáticamente las contraseñas antes de almacenarlas en la tabla `users`, mientras que el endpoint `/login` fue actualizado para validar credenciales utilizando comparación segura mediante hash.

Durante las pruebas funcionales se validó correctamente:

* Registro de usuarios con contraseñas cifradas
* Inicio de sesión exitoso con validación hash
* Rechazo de credenciales incorrectas
* Almacenamiento seguro utilizando algoritmos `scrypt`

Asimismo, se verificó mediante consultas SQLite que los nuevos usuarios registrados almacenan contraseñas cifradas en lugar de texto plano, mejorando significativamente la seguridad del microservicio.


