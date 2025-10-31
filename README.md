# Micro Posts Lab — Monolith → Web App → JWT → (Microservices design)  
**(ES / EN)**  
> **Nota importante:** Este README **omite el paso 7 (despliegue en AWS Lambda)** por inestabilidad del entorno. El diseño/paquetización de microservicios (paso 6) está documentado, pero sin despliegue.

---

## 1) Overview / Descripción

**EN.** This project implements a small **Spring Boot monolith** that lets users post short messages (≤140 chars) into a single global stream (à la Twitter). A minimal **JS frontend (Vite)** consumes the API and is deployed to **Amazon S3 (static website)**. We add **JWT security** (Cognito or HS256 fallback). Finally, we provide a **microservices-by-function design** (Lambda-first) for Users, Streams and Posts (packaging ready), **without** doing the cloud deployment step.

**ES.** Este proyecto implementa un **monolito Spring Boot** para posts cortos (≤140) en un solo stream. Un **frontend JS (Vite)** consume el API y se publica en **Amazon S3**. Se añade **seguridad JWT** (Cognito o HS256 de respaldo). También se incluye el **diseño a microservicios por función** (Lambda-ready) para Usuarios, Streams y Posts, **sin** ejecutar el despliegue en la nube.

---

## 2) Architecture / Arquitectura

- **Domain (3 entidades):**
  - **User** (`id`, `username`, `email`)
  - **StreamTopic** (`id`, `name`) — único stream “general” por defecto
  - **Post** (`id`, `content`, `createdAt`, `userId`, `streamId`)
- **Monolith:** Spring Boot 3, JPA/Hibernate, H2 (dev), REST controllers.
- **Frontend:** Vite + TypeScript. Configurable via `VITE_API_BASE`.
- **Security:** JWT (header `Authorization: Bearer <token>`).  
  - Opción A: **AWS Cognito** (recomendado).  
  - Opción B: **HS256 local** (para pruebas/CI).
- **Microservices-by-function (design-only):**  
  - `lambda-users` · `lambda-streams` · `lambda-posts` (Java 21 + maven-shade, API Gateway HTTP, DynamoDB).

### Minimal logical diagram
```
[Web (S3 + Vite)] --HTTP--> [Monolith (Spring Boot)] --JPA--> [H2 dev]

Microservices design (no deploy):
API Gateway --> Lambda: users/posts/streams --> DynamoDB (tables: users, posts, stream_topic)
```

---

## 3) Repository Layout / Estructura

```
Microservicios-solo/
├─ monolith/                  # Spring Boot app (API + JWT)
│  ├─ src/main/java/...
│  └─ Dockerfile
├─ frontend/                  # Vite app
│  ├─ src/ ...
│  └─ .env.production         # VITE_API_BASE=...
├─ serverless/                # (docs, infra templates opcional)
├─ lambda-posts/              # Ejemplo empaquetado (paso 6, sin despliegue)
│  ├─ pom.xml
│  └─ src/main/java/com/example/posts/PostsHandler.java
└─ README.md
```

---

## 4) Requirements / Requisitos

- **Java 21**, **Maven 3.9+**
- **Node 20+**, **npm 9+**
- (Opcional) **Docker Desktop**
- **AWS account** (para S3, Cognito opcional; CloudShell recomendado)

---

## 5) Monolith — Run / Ejecutar

<img width="230" height="118" alt="Captura de pantalla 2025-10-26 204632" src="https://github.com/user-attachments/assets/ac527eaf-0608-4a04-85c6-954249d3c075" />

### A) Maven (Windows/macOS/Linux)

<img width="1464" height="656" alt="Captura de pantalla 2025-10-26 193257" src="https://github.com/user-attachments/assets/a764d929-5bc5-4cd1-bb61-66b928761fd9" />

```bash
# From: Microservicios-solo/monolith
mvn -q -DskipTests spring-boot:run
# App -> http://localhost:8081
```

### B) Docker (opcional)

<img width="1919" height="958" alt="Captura de pantalla 2025-10-27 205612" src="https://github.com/user-attachments/assets/69fc21e9-7438-4733-a680-06a6d19e3034" />

```bash
# Build
docker build -t micro-monolith:step5 .

# Run (H2 in-memory + data.sql)
docker run --rm -p 8081:8081   -e SPRING_JPA_HIBERNATE_DDL_AUTO=create   -e SPRING_JPA_DEFER_DATASOURCE_INITIALIZATION=true   -e SPRING_SQL_INIT_MODE=always   micro-monolith:step5
```

> **Troubleshooting Docker (Win):** si ves `500 Internal Server Error API route ...` reinicia Docker Desktop, `wsl --shutdown`, vuelve a abrir Docker y comprueba `docker info`.

---

## 6) API (Monolith)

Base URL (dev): `http://localhost:8081`

- `GET  /api/posts` → lista de posts (orden desc por fecha).
- `POST /api/posts` → crea post `{ userId, streamId, content }` (≤140).
- `GET  /api/streams` → lista de streams.
- `GET  /api/users` → lista de usuarios (demo).
- `POST /api/auth/login` → (opcional) devuelve JWT HS256 para pruebas.

### Curl quick test

```bash
curl -s http://localhost:8081/api/posts

curl -s -X POST http://localhost:8081/api/posts   -H "Content-Type: application/json"   -d '{"userId":1,"streamId":1,"content":"hola desde curl"}'
```

---

## 7) Frontend (Vite) — Build & S3

<img width="1058" height="354" alt="Captura de pantalla 2025-10-26 225412" src="https://github.com/user-attachments/assets/341833d7-3317-40cf-b4ad-844df2ddfa00" />

### 7.1 Build

<img width="613" height="227" alt="Captura de pantalla 2025-10-26 204434" src="https://github.com/user-attachments/assets/b0fbec4a-e30f-4591-abe2-91902f5aca60" />

```bash
# From: Microservicios-solo/frontend
# Set your API base (monolith or API Gateway)
echo VITE_API_BASE=http://localhost:8081/api > .env.production

npm install
npm run build    # outputs to dist/
```

### 7.2 Deploy to S3 (dos formas)

- **Consola AWS (sin CLI local):**  
  S3 → bucket (ej. `micro-lab-front-xxx`) → **Upload** → sube **el contenido** de `dist/` (no la carpeta padre). Habilita “Static website hosting” y `index.html` como documento raíz.

- **CloudShell (si prefieres CLI ya autenticada):**
  1) Comprime `dist/` en tu PC y **Upload** a CloudShell.  
  2)
  ```bash
  unzip dist.zip -d dist
  aws s3 sync ./dist/ "s3://<tu-bucket>/" --delete --region us-east-1
  ```

> Si el frontend muestra “Backend: http://localhost:8081 (proxy /api) / HTTP 404”, revisa que `VITE_API_BASE` apunte a la URL correcta (monolith local o tu API Gateway).

---

## 8) Security (JWT)

### Opción A — Cognito (recomendado)
- User Pool + App client (sin secret).
- En backend, añadir **JWT resource server** (lib de Cognito o Nimbus) para validar:
  - Issuer: `https://cognito-idp.<region>.amazonaws.com/<UserPoolId>`
  - Audiencia: App client id.
- Frontend: almacenar `id_token`/`access_token` en memoria (no localStorage para prod).

### Opción B — HS256 simple (dev/CI)
- Backend: propiedad `jwt.secret` (env var `JWT_SECRET`).
- `POST /api/auth/login` retorna un HS256 válido por X minutos.
- Cliente: enviar `Authorization: Bearer <token>`.

> **Rutas públicas**: `GET /api/posts`. **Rutas protegidas**: `POST /api/posts` (ejemplo).

---

## 9) Tests / Pruebas

- **Unit (backend):** servicios, validaciones (≤140 chars), orden por fecha, creación de relaciones `Post→User,Stream`.  
- **Integration (backend):** `@SpringBootTest` con H2, `data.sql`.  
- **Frontend e2e (opcional):** Playwright o Cypress.

### Ejemplos (curl / Postman)

```bash
# Health / bienvenida estática
curl -I http://localhost:8081/

# Lista posts
curl -s http://localhost:8081/api/posts | jq '.[:3]'
```

---

## 10) Step 6 — Split into 3 microservices (design only)  
**(Sin paso 7: no se despliega en AWS por ahora)**

<img width="1504" height="1003" alt="Captura de pantalla 2025-10-27 205452" src="https://github.com/user-attachments/assets/e6cf9fe5-5b04-4c9d-bdbb-1038f380025d" />
<img width="1919" height="986" alt="Captura de pantalla 2025-10-26 211053" src="https://github.com/user-attachments/assets/3303d727-e24a-4987-8de0-6d014985f555" />
<img width="1908" height="960" alt="Captura de pantalla 2025-10-26 212501" src="https://github.com/user-attachments/assets/c49bbaaa-94f5-4856-abc6-0ac86ff55ffe" />

### 10.1 Common patterns
- **Runtime:** Java 21 + `maven-shade-plugin` (fat JAR).
- **Events:** `APIGatewayV2HTTPEvent` → `APIGatewayV2HTTPResponse`.
- **DB:** DynamoDB tablas `users`, `stream_topic`, `posts`.
- **CORS:** headers en respuesta (ALLOW * / métodos GET,POST,OPTIONS).

### 10.2 Example: `lambda-posts/` (empaquetado listo)

`lambda-posts/pom.xml` (shade, Jackson, AWS SDK v2 DynamoDB).

`PostsHandler.java`:
- `GET /api/posts` → `Scan` y mapeo de items.
- `POST /api/posts` → valida longitud ≤140, `PutItem` con `createdAt=Instant.now()`.

**Build (CloudShell o local):**
```bash
# Sin BOM en .java (UTF-8)
mvn -q -DskipTests clean package
# Produce: target/lambda-posts-1.0.0.jar
```

> **Despliegue (omitido)**: cuando el entorno esté estable, crear función Lambda con un **rol existente** que tenga `AWSLambdaBasicExecutionRole` + permisos a DynamoDB; integrar con API Gateway HTTP y probar.

---

## 11) Deliverables / Entregables (Paso 8)

- **Código (GitHub):**
  - `monolith/`, `frontend/`, `lambda-posts/` (y/o `lambda-users`, `lambda-streams` si aplica).
- **Architecture Report / Reporte de Arquitectura** (`/docs/architecture.md`):
  - Diagrama de módulos, modelo de datos, decisiones (DB in-memory vs DynamoDB), seguridad (Cognito/HS256), CORS.
- **Test Report / Reporte de Pruebas** (`/docs/tests.md`):
  - Cobertura y evidencia (capturas de Postman/curl).
- **Demo Video / Video de demostración**:
  - Flujo: crear post en UI → ver en lista → (opcional) token JWT y POST autorizado.
- **README** (este archivo) con:
  - Setup, ejecución local, build frontend, publicación S3, diseño microservicios (sin despliegue).

Checklist:
- [ ] Monolith compila y corre (`:8081`).  
- [ ] Frontend en S3 con `VITE_API_BASE` correcto.  
- [ ] JWT funcionando (Cognito o HS256).  
- [ ] Empaquetado de `lambda-posts` listo (sin errores).  
- [ ] Documentación y video incluidos.

---

## 12) Troubleshooting

- **Docker Desktop (Windows)**
  - `wsl --shutdown` y relanza Docker; verifica `docker context use desktop-linux`.
- **AWS CLI local**  
  - Si ves `Unable to locate credentials`, usa **CloudShell** o configura `aws configure`.
- **BOM error (`\ufeff`) en Java**  
  - Guarda el `.java` como **UTF-8 sin BOM** y recompila (`mvn clean package`).
- **Frontend muestra “HTTP 404”**  
  - Revisa `VITE_API_BASE` en `.env.production` y vuelve a `npm run build`.

