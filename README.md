# RAG with LangChain + OpenAI + Pinecone (EN / ES)

**EN:** Retrieval-Augmented Generation over your local docs using **OpenAI** for embeddings & generation and **Pinecone** for vector search.  
**ES:** RAG sobre tus documentos locales usando **OpenAI** (embeddings y generación) y **Pinecone** para la búsqueda vectorial.

---

## 1) Architecture / Arquitectura

**EN**
- **Ingest:** Load files → split into chunks → embed (OpenAI) → upsert to Pinecone.
- **Query:** Question → retrieve top-k from Pinecone → prompt the LLM with those chunks → answer.

**ES**
- **Ingesta:** Cargar archivos → dividir en fragmentos → *embed* (OpenAI) → upsert a Pinecone.
- **Consulta:** Pregunta → recuperar *top-k* de Pinecone → *prompt* al LLM con esos fragmentos → respuesta.

```
[PDF/TXT/MD] ──load──▶ split ──embed──▶ Pinecone (index)
                                  ▲                       │
                                  └──── retrieve (k) ◀────┘
                                            │
                                        prompt LLM
                                            │
                                         answer + sources
```

---

## 2) Prerequisites / Prerrequisitos

- Python 3.9+  
- OpenAI API key (`OPENAI_API_KEY`)  
- Pinecone API key (`PINECONE_API_KEY`)

> **Embedding dims:** `text-embedding-3-small` = **1536**. If you switch model, adjust index `dimension`.

---

## 3) Setup / Configuración

### A) Virtual env
**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### B) Install deps / Instalar dependencias
```bash
pip install -r requirements.txt
```

### C) Environment / Variables de entorno
Copia `.env.example` → `.env` y completa:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

PINECONE_API_KEY=pcn-...
PINECONE_INDEX=rag-quickstart
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
PINECONE_NAMESPACE=default
```

---

## 4) Ingest your data / Ingesta de datos

1) Coloca tus documentos en `./data/` (`.pdf`, `.txt`, `.md`).  
2) Ejecuta:
```bash
python src/ingest.py
```
Deberías ver algo como **“✅ Ingesta completada.”**

---

## 5) Ask questions / Consultas

```bash
python src/rag.py
```

Ejemplo:
```
Q> What does the syllabus say about grading?
A> The syllabus states that...

---
Sources:
- data/syllabus.pdf
- data/notes/week1.txt
```

---

## 6) Troubleshooting / Solución de problemas

- **Import errors:** Mantén la familia LangChain alineada (todas `0.3.x`).  
- **Index dimension mismatch:** Asegura que la dimensión del índice Pinecone coincide con tu modelo de embedding.  
- **No docs found:** Verifica archivos en `./data/`.  
- **Rate limits:** Reduce `k` del retriever o usa un modelo de embedding más pequeño.

---

## 7) Repo hygiene / Organización

- `src/ingest.py`: pipeline de ingesta.  
- `src/rag.py`: consulta interactiva y listado de fuentes.  
- `data/`: tus documentos.  
- `requirements.txt` + `.env.example`: reproducibilidad.

---

## 8) Next steps / Siguientes pasos

- Citar fragmentos con `metadata` (páginas y offsets).  
- Re-ranking o filtros semánticos.  
- Evaluación de RAG (exact match / faithfulness).  
- Endpoint FastAPI/Flask para UI.
