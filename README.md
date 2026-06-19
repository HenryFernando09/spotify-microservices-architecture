# Spotify Microservices Architecture

Proyecto académico basado en una arquitectura de microservicios inspirada en plataformas de streaming musical como Spotify.

---

# Objetivo

Implementar una arquitectura distribuida utilizando microservicios desarrollados en Python y Flask, integrando tecnologías modernas como Docker, Docker Compose, GitHub, Kafka y Ubuntu Server.

El proyecto busca aplicar conceptos de:

- Arquitectura de Microservicios
- Contenedores Docker
- Comunicación entre servicios
- Seguridad básica en APIs
- Monitoreo y escalabilidad
- Virtualización en Linux

---

#  Arquitectura del Proyecto

El sistema está dividido en varios microservicios independientes:

| Microservicio | Función |
|---|---|
| Auth Service | Registro y autenticación de usuarios |
| Music Service | Gestión de canciones |
| Playlist Service | Administración de playlists |
| Notification Service | Simulación de notificaciones |

---

#  Tecnologías Utilizadas

- Python 3
- Flask
- Docker
- Docker Compose
- Ubuntu Server
- Git & GitHub
- Apache Kafka
- Grafana
- SQLite

---

#  Contenedorización

Cada microservicio se ejecuta dentro de un contenedor Docker independiente, permitiendo:

- Aislamiento de servicios
- Escalabilidad
- Fácil despliegue
- Portabilidad del sistema

---

#  Seguridad Implementada

## Vulnerabilidades identificadas

Durante el desarrollo del proyecto se detectaron algunas vulnerabilidades en el `auth-service`.

### Problemas encontrados

- Contraseñas almacenadas en texto plano
- Comunicación HTTP sin cifrado
- Falta de validaciones de seguridad

### Soluciones aplicadas

- Implementación de hash de contraseñas con `werkzeug.security`
- Uso de `generate_password_hash()`
- Validación segura con `check_password_hash()`
- Recomendación de implementación HTTPS con SSL/TLS

---

#  Estructura del Proyecto

```bash
spotify-microservices-architecture/
│
├── auth-service/
├── music-service/
├── playlist-service/
├── notification-service/
├── docker/
├── docs/
├── evidencias/
└── README.md
```

---

#  Ejecución del Proyecto

## Clonar repositorio

```bash
git clone https://github.com/HenryFernando09/spotify-microservices-architecture.git
```

## Levantar contenedores

```bash
docker-compose up --build
```

---

#  Estado del Proyecto

 Proyecto en desarrollo académico.

Actualmente se encuentra en implementación de:

- Comunicación entre microservicios
- Monitoreo con Grafana
- Integración con Kafka
- Seguridad y autenticación

---

#  Integrantes

- Henry 
- Leidy
- Jersy
- Mijael

---

