# Tribe AI Application

A production-ready AI application built with FastAPI, designed for scalability and reliability.

## Features

- 🤖 Multi-model AI support (OpenAI, Anthropic)
- 🚀 FastAPI-based REST API
- 🐳 Docker containerization
- 🔒 Security best practices
- 📊 Health monitoring and logging
- 🔄 CI/CD pipeline with GitHub Actions
- 🌐 Nginx reverse proxy with SSL
- 💾 PostgreSQL and Redis integration

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- API keys for OpenAI and/or Anthropic

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lunamae24/Tribe-ai-app.git
   cd Tribe-ai-app
   ```

2. **Create and configure environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys and configuration
   ```

3. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API documentation: http://localhost:8000/api/docs

### Docker Deployment

1. **Build and start services**
   ```bash
   docker-compose up -d
   ```

2. **Check health**
   ```bash
   curl http://localhost:8000/health
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

## Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions.

## API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system metrics
- `GET /health/ready` - Readiness probe
- `GET /health/live` - Liveness probe

### AI Endpoints
- `POST /api/v1/ai/chat` - Chat with AI models
- `GET /api/v1/ai/models` - List available models

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

### Required Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `SECRET_KEY` - Application secret key
- `DATABASE_URL` - PostgreSQL connection string

## Security

- API keys stored in environment variables (never committed)
- HTTPS enforced in production
- Rate limiting on API endpoints
- Security headers configured
- Regular security scans in CI/CD

## Monitoring

- Health check endpoints for Kubernetes/Docker
- Sentry integration for error tracking
- Structured logging with JSON format
- System metrics in detailed health check

## Development

### Running Tests
```bash
pytest tests/ --cov=app
```

### Code Formatting
```bash
black app
```

### Linting
```bash
flake8 app
```

### Type Checking
```bash
mypy app
```

## CI/CD

The project includes a GitHub Actions workflow that:
- Runs tests and linting
- Performs security scans
- Builds and pushes Docker images
- Deploys to production (on main branch)

## Support

For issues and questions, please open a GitHub issue.

## License

MIT License - see LICENSE file for details