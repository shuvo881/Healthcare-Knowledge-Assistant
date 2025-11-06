# Healthcare Knowledge Assistant

A multilingual RAG (Retrieval-Augmented Generation) backend system for healthcare knowledge management. This FastAPI-based application allows you to ingest medical documents, retrieve relevant information, and generate AI-powered responses in multiple languages.

## Features

- 🌍 **Multilingual Support** - Automatic language detection and translation
- 📄 **Document Ingestion** - Upload and process text documents
- 🔍 **Semantic Search** - FAISS-powered vector similarity search
- 🤖 **AI Generation** - LLM-based response generation with retrieved context
- 🔐 **API Key Authentication** - Secure API access
- 🐳 **Docker Support** - Containerized deployment
- 🚀 **CI/CD Pipeline** - Automated Docker builds via GitHub Actions

## Tech Stack

- **Framework**: FastAPI
- **Vector Store**: FAISS
- **Embeddings**: Sentence Transformers
- **Translation**: Deep Translator
- **Language Detection**: LangDetect
- **Package Manager**: UV
- **Python Version**: 3.13+

## Prerequisites

- Python 3.13 or higher
- UV package manager
- Docker (optional, for containerized deployment)
- API keys for LLM services (if using generation features)

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Healthcare-Knowledge-Assistant.git
   cd Healthcare-Knowledge-Assistant
   ```

2. **Install UV package manager** (if not already installed)
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies**
   ```bash
   uv sync --locked
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```env
   API_KEY=your-api-key-here
   HF_TOKEN=your-huggingface-token-here
   ```

5. **Run the application**
   ```bash
   uv run src
   ```

   The API will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Create `.env` file** with your configuration:
   ```env
   API_KEY=your-api-key-here
   HF_TOKEN=your-huggingface-token-here
   ```

2. **Build and run**
   ```bash
   docker-compose up -d
   ```

3. **Access the API** at `http://localhost:8000`

4. **Stop the container**
   ```bash
   docker-compose down
   ```

### Using Docker CLI

1. **Build the image**
   ```bash
   docker build -t healthcare-knowledge-assistant \
     --build-arg API_KEY=your-api-key \
     --build-arg HF_TOKEN=your-hf-token .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e API_KEY=your-api-key \
     -e HF_TOKEN=your-hf-token \
     --name healthcare-rag \
     healthcare-knowledge-assistant
   ```

### Using Pre-built Image from Docker Hub

```bash
docker pull <dockerhub-username>/healthcare-knowledge-assistant:latest

docker run -d \
  -p 8000:8000 \
  -e API_KEY=your-api-key \
  -e HF_TOKEN=your-hf-token \
  <dockerhub-username>/healthcare-knowledge-assistant:latest
```

## API Documentation

Once the application is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Authentication

All API endpoints require an API key. Include it in the request header:
```
X-API-Key: your-api-key-here
```

### Endpoints

#### 1. Health Check
```http
GET /
```
Returns the status of the API.

#### 2. Ingest Document
```http
POST /ingest/
Content-Type: multipart/form-data
X-API-Key: your-api-key

file: <text-file>
```
Upload and process a text document for indexing.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/ingest/" \
  -H "X-API-Key: your-api-key" \
  -F "file=@document.txt"
```

#### 3. Retrieve Documents
```http
POST /retrieve/
Content-Type: application/json
X-API-Key: your-api-key

{
  "query": "What are the symptoms of diabetes?"
}
```
Retrieve relevant document chunks based on semantic similarity.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/retrieve/" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of diabetes?"}'
```

#### 4. Generate Response
```http
POST /generate/
Content-Type: application/json
X-API-Key: your-api-key

{
  "query": "Explain diabetes treatment options"
}
```
Generate an AI-powered response using retrieved context.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/generate/" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain diabetes treatment options"}'
```

## CI/CD Pipeline

This project includes an automated CI/CD pipeline using GitHub Actions that builds and pushes Docker images to Docker Hub.

### Pipeline Features

- ✅ Automatic builds on push to `main` branch
- ✅ Builds on pull requests
- ✅ Version tagging support (e.g., `v1.0.0`)
- ✅ Multi-platform support (linux/amd64, linux/arm64)
- ✅ Manual workflow dispatch

### Setup Instructions

For detailed CI/CD setup instructions, see [docs/CICD_SETUP.md](docs/CICD_SETUP.md)

**Quick Setup:**

1. Create a Docker Hub access token
2. Add GitHub secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token
   - `API_KEY`: Your API key (for build args)
   - `HF_TOKEN`: Your HuggingFace token (for build args)
3. Push to `main` branch or create a tag

## Project Structure

```
Healthcare-Knowledge-Assistant/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml    # CI/CD pipeline
├── data/                             # Vector store and document storage
│   ├── doc_store.json
│   └── faiss_index.faiss
├── docs/
│   └── CICD_SETUP.md                # CI/CD setup guide
├── media/
│   └── uploads/                      # Uploaded documents
├── src/
│   ├── __main__.py                   # Application entry point
│   ├── app.py                        # FastAPI application
│   ├── rag/                          # RAG implementation
│   │   ├── __init__.py
│   │   ├── llm.py                    # LLM integration
│   │   ├── main.py                   # RAG core logic
│   │   └── translator.py            # Translation utilities
│   └── routers/                      # API endpoints
│       ├── generate.py               # Generation endpoint
│       ├── ingest.py                 # Ingestion endpoint
│       └── retrieve.py               # Retrieval endpoint
├── .env                              # Environment variables (create this)
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker image definition
├── pyproject.toml                    # Project dependencies
├── uv.lock                           # Locked dependencies
└── README.md                         # This file
```

## Development

### Adding Dependencies

Use UV package manager to add new dependencies:

```bash
uv add package-name
```

### Running Tests

```bash
# Add your test commands here
uv run pytest
```

### Code Formatting

```bash
# Add your formatting commands here
uv run black src/
uv run isort src/
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | API key for authentication | Yes |
| `HF_TOKEN` | HuggingFace token for model access | Optional |

## Troubleshooting

### Common Issues

1. **Port 8000 already in use**
   ```bash
   # Change the port in docker-compose.yml or use:
   docker run -p 8001:8000 ...
   ```

2. **Permission denied on uploads directory**
   ```bash
   mkdir -p media/uploads
   chmod 755 media/uploads
   ```

3. **Docker build fails**
   - Ensure `uv.lock` is up to date: `uv lock`
   - Check that all dependencies are in `pyproject.toml`

4. **API key authentication fails**
   - Verify the `X-API-Key` header is included in requests
   - Check that the API key matches the one in `.env`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- FAISS for efficient similarity search
- Sentence Transformers for embeddings
- UV for fast Python package management

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the API docs at `/docs` endpoint

---

**Note**: This is a healthcare knowledge assistant. Always consult qualified healthcare professionals for medical advice.