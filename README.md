# LangChain LLM Chain – Quickstart (EN / ES)

**EN** — Minimal example of a LangChain *LLM Chain* using **OpenAI**.  
**ES** — Ejemplo mínimo de un *LLM Chain* de LangChain usando **OpenAI**.

---

## 1) What is this? / ¿Qué es?

**EN:** A tiny pipeline that takes your prompt, sends it to an OpenAI Chat model, and returns plain text.  
**ES:** Un pipeline pequeño que toma tu *prompt*, lo envía a un modelo Chat de OpenAI y devuelve texto plano.

```
User text ──▶ Prompt template ──▶ ChatOpenAI ──▶ StrOutputParser ──▶ Answer
```

---

## 2) Repository layout / Estructura del repositorio

```
lc-llm-chain-basics/
├─ src/
│  └─ main.py
├─ .env.example
├─ requirements.txt
└─ README.md
```

- `src/main.py`: script principal con el *LLM Chain*.
- `.env.example`: plantilla de variables de entorno.
- `requirements.txt`: dependencias de Python.
- `README.md`: este archivo.

---

## 3) Prerequisites / Prerrequisitos

- Python **3.9+**
- Una clave de API de OpenAI (**OPENAI_API_KEY**)
- Conexión a internet para dependencias

> **Tip:** Nunca subas tu `.env` a Git; usa `.env.example` para compartir la plantilla.

---

## 4) Setup / Configuración

### A) Create & activate a virtual env / Crear y activar entorno virtual

**Windows (PowerShell)**
```powershell
python -m venv .venv
. .venv\\Scripts\\Activate.ps1
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### B) Install dependencies / Instalar dependencias
```bash
pip install -r requirements.txt
```

### C) Environment variables / Variables de entorno

Copia `.env.example` → `.env` y completa tu clave:

```ini
# .env
OPENAI_API_KEY=sk-...
# optional / opcional
OPENAI_MODEL=gpt-4o-mini
```

> Puedes cargar `.env` con `python-dotenv` dentro del script.

---

## 5) Run / Ejecutar

```bash
python src/main.py
```

**Expected output / Salida esperada (example):**
```
It will probably rain later this afternoon.
```

---

## 6) Code (reference) / Código (referencia)

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
llm = ChatOpenAI(model=model_name, temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant."),
    ("user", "Rewrite the following text in plain English:\n\n{text}")
])

chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    user_text = "The precipitation will likely manifest later this afternoon."
    print(chain.invoke({"text": user_text}))
```

**EN:** We compose a chain with the `|` operator: prompt → model → parser.  
**ES:** Componemos una cadena con el operador `|`: *prompt* → modelo → *parser*.

---

## 7) Troubleshooting / Solución de problemas

- **ImportError / ModuleNotFoundError**: Asegúrate de instalar `requirements.txt` dentro del entorno virtual activo.
- **Invalid API key**: Verifica `OPENAI_API_KEY` en `.env` y que tu script cargue variables (p. ej., `python-dotenv`).
- **Proxy/Firewall**: Si estás en red corporativa, configura variables de entorno `HTTP_PROXY`/`HTTPS_PROXY` si aplica.

---

## 8) How to contribute / Cómo contribuir

1. Crea una rama: `git checkout -b feat/your-change`
2. Haz tu cambio y añade tests si aplica.
3. Abre un PR describiendo la motivación y el impacto.

---

## 9) References / Referencias

- LangChain — LLM Chain tutorial: https://python.langchain.com/docs/tutorials/llm_chain/
- LangChain + OpenAI package: https://python.langchain.com/docs/integrations/llms/openai
- OpenAI API keys: https://platform.openai.com/account/api-keys

---

## 10) License / Licencia

MIT — siéntete libre de usar y adaptar este contenido para tu laboratorio.
