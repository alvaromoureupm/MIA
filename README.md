# MIA: Asistente Legal Basado en IA

MIA es un asistente legal inteligente que utiliza técnicas de procesamiento de lenguaje natural y recuperación aumentada por IA para responder consultas legales basadas en documentos oficiales. El proyecto está desarrollado en Python y emplea tecnologías como LangChain, ChromaDB y OpenAI.

## Características principales
- **Interfaz web**: Aplicación Streamlit con chat interactivo.
- **Recuperación de información**: Utiliza embeddings y búsqueda semántica sobre documentos legales (PDFs, BOE, BOPA, etc.).
- **ETL modular**: Extracción y procesamiento de documentos oficiales.
- **Integración con modelos LLM**: Respuestas generadas por modelos de lenguaje (OpenAI GPT).
- **CLI**: Herramienta de línea de comandos para gestión y procesamiento de documentos.

## Estructura del proyecto

```
src/mia/
  main.py                # CLI principal
  backend/
    streamlit_app.py      # Interfaz web
    chroma/               # Vector store y gestión de embeddings
    etl/                  # Extracción y procesamiento de datos
    llm/                  # Lógica de modelos de lenguaje y prompts
  frontend/
    assets/               # Imágenes y recursos visuales
tests/                    # Pruebas unitarias
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/alvaromoureupm/MIA.git
   cd MIA
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   O usando [uv](https://github.com/astral-sh/uv):
   ```bash
   uv pip install -r requirements.txt
   ```
3. Configura las variables de entorno en un archivo `.env` si es necesario (por ejemplo, claves de OpenAI).

## Uso

### Interfaz Web
Ejecuta la aplicación Streamlit:
```bash
streamlit run src/mia/backend/streamlit_app.py
```

### CLI
Ejecuta el CLI para gestión de documentos:
```bash
python src/mia/main.py --help
```

### Pruebas
Run the tests:
```bash
pytest
```

## Processed Documents
- BOE (Boletín Oficial del Estado)
- BOPA (Boletín Oficial del Principado de Asturias)
- Legal PDFs

## Main Dependencies
- Python >= 3.12
- beautifulsoup4
- fastembed
- langchain, langchain-chroma, langchain-openai
- langgraph
- lxml
- onnxruntime
- python-dotenv
- streamlit

## License
© 2025 MIA Legal Assistant. All rights reserved.
