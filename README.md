# jarvis
# 🤖 Jarvis - Intelligent Agent Framework

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

**An intelligent multi-agent task execution system with LLM-powered planning, execution, and review capabilities**

[Quick Start](#-quick-start) • [Installation](#-installation) • [API Docs](#-api-endpoints) • [Contributing](#-contributing) • [License](#-license)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start--30-seconds)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

Jarvis is an advanced AI-powered task management and execution system built with FastAPI, LangChain, and LLaMA Index. It leverages multi-agent orchestration to plan, execute, and review complex tasks with memory capabilities powered by Qdrant vector database.

**Use cases:**
- Autonomous task execution workflows
- Complex decision-making systems
- Task planning and optimization
- Knowledge retrieval and memory management
- Multi-step process automation

---

## 🌟 Features

- ✅ **Intelligent Task Planning** - LLM-based planner that breaks down complex tasks into actionable steps
- ✅ **Automated Execution** - Execute tasks with LangChain agents and tools
- ✅ **Quality Review** - Automated review system to validate task execution and results
- ✅ **Memory & RAG** - Vector-based memory system using Qdrant for semantic context retrieval
- ✅ **Multi-Agent Orchestration** - Planner, Executer, and Reviewer agents working in harmony
- ✅ **RESTful API** - Clean FastAPI endpoints for task management
- ✅ **Persistent Storage** - SQLAlchemy ORM with database integration
- ✅ **Advanced Embeddings** - HuggingFace BAAI/bge-small-en for semantic search
- ✅ **Graph-Based Workflows** - LangGraph support for complex agent workflows
- ✅ **Production Ready** - Error handling, logging, and monitoring

---

## 🏗️ Architecture

```
System Flow:
User Request
    ↓
[FastAPI Endpoint] (/tasks)
    ↓
[Task Manager] (Receives & Validates)
    ↓
[Agent Manager]
    ├─→ [Planner Agent] (Break down task)
    ├─→ [Memory Retrieval] (Get context via RAG)
    ├─→ [Executer Agent] (Execute planned steps)
    ├─→ [Memory Storage] (Store execution history)
    └─→ [Reviewer Agent] (Validate results)
    ↓
[Response] (Return results to user)

Project Structure:
app/
├── agent/                    # Multi-agent orchestration
│   ├── planner.py           # Task planning agent
│   ├── executer.py          # Task execution agent
│   ├── reviewer.py          # Quality review agent
│   └── manager.py           # Orchestration manager
├── memory/                   # Memory & RAG system
│   ├── vector_store.py      # Qdrant vector store
│   ├── service.py           # Memory operations
│   ├── rag_service.py       # RAG retrieval
│   └── behavior.py          # Memory behavior tracking
├── llm/                      # LLM integration layer
│   ├── llm_client.py        # LLM client wrapper
│   ├── llm_service.py       # LLM operations
│   ├── provider.py          # Provider management
│   └── llm_exception.py     # Error handling
├── task/                     # Task management
│   ├── models.py            # Task data models
│   └── store.py             # Task persistence
├── db/                       # Database layer
│   └── db.py                # Database configuration
├── service/                  # Business logic
│   └── task_service.py      # Task CRUD operations
├── prompts/                  # LLM prompt templates
│   ├── planner_prompts.py
│   ├── executer_prompts.py
│   ├── reviewer_prompts.py
│   └── registry.py
├── dto/                      # Data transfer objects
│   └── dto.py               # Pydantic models
├── routers/                  # API route handlers
│   └── routers.py           # FastAPI routes
├── core/                     # Core utilities
│   ├── config.py            # Configuration management
│   └── logging.py           # Logging setup
├── graph/                    # Workflow graphs
│   └── graph.py             # LangGraph workflows
└── main.py                   # FastAPI entry point
```

---

## 🚀 Quick Start (30 seconds)

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (or SQLite)
- Docker (for Qdrant)

### Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd python-project

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Start services
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant  # Terminal 1
uvicorn app.main:app --reload                        # Terminal 2

# 6. Access application
open http://localhost:8000/docs
```

**Done!** 🎉 Your Jarvis instance is running.

---

## 📋 Installation

### System Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Runtime environment |
| PostgreSQL | 12+ | Database (optional: use SQLite) |
| Docker | Latest | Running Qdrant |
| RAM | 8GB min | LLM operations |

### Step-by-Step Installation

#### 1. Prerequisites Setup

**Windows:**
```bash
# Install Python 3.10+
# Download from https://www.python.org/downloads/

# Install PostgreSQL
# Download from https://www.postgresql.org/download/windows/

# Install Docker
# Download from https://www.docker.com/products/docker-desktop
```

**macOS:**
```bash
brew install python@3.10 postgresql@15
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install python3.10 python3.10-venv postgresql
curl -fsSL https://get.docker.com | sudo sh
```

#### 2. Clone Repository

```bash
git clone <your-repository-url>
cd python-project
```

#### 3. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3.10 -m venv .venv
source .venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 5. Database Setup

**PostgreSQL:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE USER jarvis_user WITH PASSWORD 'jarvis_password';
CREATE DATABASE jarvis_db OWNER jarvis_user;
GRANT ALL PRIVILEGES ON DATABASE jarvis_db TO jarvis_user;

# Exit
\q
```

**Or use SQLite (development only):**
```bash
# Set in .env: DATABASE_URL=sqlite:///jarvis.db
# SQLite database will be created automatically
```

#### 6. Qdrant Vector Database Setup

**Using Docker (Recommended):**
```bash
docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant

# Verify
curl http://localhost:6333/health
```

#### 7. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Database
DATABASE_URL=postgresql://jarvis_user:jarvis_password@localhost:5432/jarvis_db

# Qdrant
QDRANT_HOST=127.0.0.1
QDRANT_PORT=6333
QDRANT_COLLECTION=agent_memory

# LLM
OPENAI_API_KEY=sk-your-key-here

# Application
API_PORT=8000
LOG_LEVEL=INFO
```

#### 8. Verify Installation

```bash
# Test Python environment
python --version

# Test imports
python -c "import fastapi; import langchain; print('✓ OK')"

# Test database
python -c "from app.db.db import engine; print('✓ Database OK')"

# Test Qdrant
python -c "from app.memory.vector_store import client; print('✓ Qdrant OK')"
```

#### 9. Run Application

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Docker Deployment (Optional)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: jarvis_user
      POSTGRES_PASSWORD: jarvis_password
      POSTGRES_DB: jarvis_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://jarvis_user:jarvis_password@postgres:5432/jarvis_db
      QDRANT_HOST: qdrant
      QDRANT_PORT: 6333
    depends_on:
      - postgres
      - qdrant
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:
  qdrant_data:
```

Run with: `docker-compose up -d`

---

## ⚙️ Configuration

### Environment Variables

```env
# ===== DATABASE =====
DATABASE_URL=postgresql://user:password@localhost:5432/jarvis_db

# ===== QDRANT VECTOR DATABASE =====
QDRANT_HOST=127.0.0.1
QDRANT_PORT=6333
QDRANT_COLLECTION=agent_memory

# ===== LLM CONFIGURATION =====
OPENAI_API_KEY=sk-your-api-key
OLLAMA_HOST=http://localhost:11434

# ===== EMBEDDINGS =====
EMBEDDING_MODEL=BAAI/bge-small-en
HUGGINGFACE_TOKEN=your_token

# ===== APPLICATION =====
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# ===== LOGGING =====
LOG_LEVEL=INFO
LOG_FILE=logs/jarvis.log

# ===== MEMORY SETTINGS =====
MEMORY_TOP_K=3

# ===== AGENT MODELS =====
PLANNER_MODEL=gpt-4
EXECUTOR_MODEL=gpt-3.5-turbo
REVIEWER_MODEL=gpt-3.5-turbo
```

---

## 📡 API Endpoints

### Core Endpoints

#### 1. Get Next Action
```
GET /next-action
```
Get the next planned action for task execution

**Response Example:**
```json
{
  "task_id": 1,
  "action": "Process invoice",
  "description": "Extract and validate invoice data"
}
```

#### 2. Create Task
```
POST /tasks
```
Create a new task

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "created_at": "2024-01-16T10:00:00"
}
```

#### 3. List Tasks
```
GET /tasks
```
Retrieve all tasks

**Response:**
```json
[
  {
    "id": 1,
    "title": "Task 1",
    "status": "completed",
    "created_at": "2024-01-16T10:00:00"
  }
]
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Examples

**Create Task:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analyze Data",
    "description": "Analyze sales data and generate report"
  }'
```

**Get Tasks:**
```bash
curl -X GET "http://localhost:8000/tasks"
```

**Get Next Action:**
```bash
curl -X GET "http://localhost:8000/next-action"
```

---

## 📚 Usage Examples

### Python API

```python
# Retrieve memory
from app.memory.service import retrieve_memory
result = retrieve_memory("failed tasks")
print(result)

# Store memory
from app.memory.service import store_memory
store_memory(
    text="Process invoice",
    result="Successfully processed",
    review="Valid output",
    success=True
)

# Get next action
from app.agent.manager import decide_next_action
from app.db.db import SessionLocal

db = SessionLocal()
action = decide_next_action(db)
db.close()
```

### REST API

**Create Task:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "Do something"}'
```

**Python Requests:**
```python
import requests

# Create task
response = requests.post(
    "http://localhost:8000/tasks",
    json={
        "title": "Analyze Data",
        "description": "Process sales data"
    }
)
task = response.json()

# Get tasks
response = requests.get("http://localhost:8000/tasks")
tasks = response.json()
```

---

## 🛠️ Development

### Code Style

Follow PEP 8 with these additions:
- Max line length: 100 characters
- Use type hints for all functions
- Use Google-style docstrings

**Example:**
```python
def retrieve_memory(query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant memories using semantic search.
    
    Args:
        query: Search query string
        top_k: Number of top results to return
        
    Returns:
        String representation of retrieved memories
    """
    query_engine = vector_store_index.as_query_engine(similarity_top_k=top_k)
    result = query_engine.query(query)
    return str(result)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_agent.py::test_planner_creates_plan
```

### Code Quality Tools

```bash
# Format with black
black app/

# Sort imports
isort app/

# Check with flake8
flake8 app/

# Type checking
mypy app/
```

### Adding New Agents

1. Create agent file in `app/agent/`
```python
# app/agent/my_agent.py
class MyAgent:
    def run(self, input: str) -> str:
        # Implementation
        pass
```

2. Define prompts in `app/prompts/`
```python
# app/prompts/my_agent_prompts.py
MY_AGENT_PROMPT = """Your custom prompt..."""
```

3. Register in `app/agent/manager.py`

### Project Structure

| Folder | Purpose |
|--------|---------|
| `app/agent/` | Multi-agent orchestration |
| `app/memory/` | Vector store & RAG |
| `app/llm/` | LLM provider integration |
| `app/task/` | Task models & persistence |
| `app/db/` | Database configuration |
| `app/service/` | Business logic |
| `app/prompts/` | LLM prompts |
| `app/dto/` | Data models (Pydantic) |
| `app/routers/` | API endpoints |
| `app/core/` | Utilities & config |

---

## 🐛 Troubleshooting

### Connection Issues

**Qdrant Connection Refused**
```bash
# Check if running
curl http://127.0.0.1:6333/health

# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant
```

**Database Connection Error**
```bash
# Check PostgreSQL status
# Windows: Services app
# macOS: brew services list
# Linux: sudo systemctl status postgresql

# Verify DATABASE_URL in .env
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clear cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `uvicorn app.main:app --port 8001` |
| Module not found | Activate venv: `source .venv/bin/activate` |
| Database locked | Restart PostgreSQL service |
| Qdrant won't connect | Ensure running and COLLECTION_NAME correct |
| .pyc files causing issues | `find . -type f -name "*.pyc" -delete` |

### Debug Mode

```python
# In .env
LOG_LEVEL=DEBUG

# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🤝 Contributing

### Getting Started

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/your-feature`
5. Open Pull Request

### Code Standards

- Follow PEP 8
- Add type hints
- Write docstrings
- Include tests
- Update docs

### Commit Messages

```
Add new feature

- Detailed description of changes
- Why the change is needed
- Any related issues

Fixes #123
```

### Pull Request Checklist

- [ ] Code follows PEP 8
- [ ] Tests pass: `pytest`
- [ ] Code formatted: `black app/`
- [ ] Types checked: `mypy app/`
- [ ] Documentation updated
- [ ] No breaking changes

---

## 📦 Dependencies

### Core Stack

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | ^0.104 | Web framework |
| LangChain | ^0.1 | LLM framework |
| LangGraph | ^0.0.34 | Workflow graphs |
| LLaMA Index | ^0.9 | Data indexing |
| Qdrant | ^2.7 | Vector database |
| SQLAlchemy | ^2.0 | ORM |
| Pydantic | ^2.5 | Data validation |
| Uvicorn | ^0.24 | ASGI server |

See `requirements.txt` for complete list.

---

## 🔐 Security

### Best Practices

- ✅ Use environment variables for secrets (API keys, passwords)
- ✅ Never commit `.env` files (add to `.gitignore`)
- ✅ Validate all inputs with Pydantic
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Keep dependencies updated
- ✅ Regular security audits

### Environment Variables

Never expose:
- Database passwords
- API keys
- Authentication tokens
- Private keys

Always use `.env.example` as template.

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Jarvis AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

## 🤝 Support & Contributing

### Getting Help

- 📖 **Documentation**: See this README
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 **Email**: your-email@example.com

### Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest

# Format code
black app/

# Check quality
flake8 app/
mypy app/
```

---

## 🙏 Acknowledgments

Built with ❤️ using:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [LangChain](https://langchain.com/) - LLM framework
- [LLaMA Index](https://www.llamaindex.ai/) - Data indexing & retrieval
- [Qdrant](https://qdrant.tech/) - Vector database
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

## 📊 Project Status

| Component | Status | Version |
|-----------|--------|---------|
| Core Framework | ✅ Active | 0.1.0 |
| API | ✅ Stable | 1.0 |
| Documentation | ✅ Complete | 1.0 |
| Testing | ✅ Ready | - |
| Production Ready | ✅ Yes | - |

---

<div align="center">

**[⬆ back to top](#-jarvis---intelligent-agent-framework)**

Made with ❤️ by Atul Kumar

</div>

