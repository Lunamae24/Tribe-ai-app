# Quick Start Guide

Get your Tribe AI Application up and running in minutes!

## Prerequisites

Choose one of the following options:

### Option 1: Docker (Recommended - Easiest)
- Docker and Docker Compose installed
- API keys for OpenAI and/or Anthropic

### Option 2: Local Python
- Python 3.11 or higher
- pip package manager
- API keys for OpenAI and/or Anthropic

## Quick Start with Docker (5 minutes)

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/Lunamae24/Tribe-ai-app.git
cd Tribe-ai-app

# Create environment file
cp .env.example .env
```

### 2. Edit `.env` file

Open `.env` and update at minimum:
```env
OPENAI_API_KEY=your_actual_openai_key_here
SECRET_KEY=generate_a_random_32_character_string
```

To generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Start the Application

```bash
docker-compose up -d
```

### 4. Verify It's Running

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2024-..."}
```

### 5. Test the API

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

### 6. Access Documentation

Open in your browser:
- API Docs: http://localhost:8000/api/docs
- Main endpoint: http://localhost:8000

## Quick Start without Docker (10 minutes)

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/Lunamae24/Tribe-ai-app.git
cd Tribe-ai-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Create environment file
cp .env.example .env

# Edit .env with your editor
nano .env  # or vim, code, etc.
```

Update these required fields:
```env
OPENAI_API_KEY=your_actual_openai_key
SECRET_KEY=your_32_character_secret
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

### 4. Test It

```bash
# In another terminal
curl http://localhost:8000/health
```

## Using Make Commands (Developer Friendly)

If you have `make` installed:

```bash
# Setup (copy .env.example to .env)
make setup

# Install dependencies
make install

# Run development server
make dev

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Start with Docker
make docker-up

# Stop Docker
make docker-down

# View logs
make docker-logs

# Check health
make health
```

## Common Issues and Solutions

### Issue: "Module not found"
**Solution**: Make sure you installed dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution**: Port 8000 is occupied. Either:
1. Stop the other service using port 8000
2. Change APP_PORT in .env to a different port

### Issue: "API key not configured"
**Solution**: Check your .env file has valid API keys
```bash
cat .env | grep API_KEY
```

### Issue: Docker containers won't start
**Solution**: Check Docker logs
```bash
docker-compose logs
```

## Next Steps

### 1. Explore the API

Visit http://localhost:8000/api/docs for interactive API documentation

### 2. Run Tests

```bash
# With Docker
docker-compose exec app pytest

# Without Docker
pytest
```

### 3. Read the Documentation

- [API Documentation](docs/API.md) - Learn about all endpoints
- [Deployment Guide](docs/DEPLOYMENT.md) - Deploy to production
- [Architecture](docs/ARCHITECTURE.md) - Understand the system
- [Go-Live Checklist](docs/GO_LIVE_CHECKLIST.md) - Production readiness

### 4. Development

Start making changes:
```bash
# The app will auto-reload with changes (if using --reload flag)
# Edit files in app/ directory
# Tests in tests/ directory
```

## Production Deployment

When ready to deploy to production:

1. Review [GO_LIVE_CHECKLIST.md](docs/GO_LIVE_CHECKLIST.md)
2. Follow [DEPLOYMENT.md](docs/DEPLOYMENT.md)
3. Update domain in CNAME file: `tribe-ai.it.com`
4. Configure production secrets securely
5. Enable HTTPS
6. Set up monitoring

## Quick Reference

### Health Checks
- Basic: `GET /health`
- Detailed: `GET /health/detailed`
- Ready: `GET /health/ready`
- Live: `GET /health/live`

### AI Endpoints
- Chat: `POST /api/v1/ai/chat`
- Models: `GET /api/v1/ai/models`

### Useful Commands

```bash
# Check app status
curl http://localhost:8000/health

# View logs (Docker)
docker-compose logs -f

# Restart app (Docker)
docker-compose restart

# Stop app (Docker)
docker-compose down

# Run tests
pytest tests/

# Format code
black app tests

# Lint code
flake8 app tests
```

## Getting Help

- 📖 Check the [README](README.md)
- 📚 Read the [documentation](docs/)
- 🐛 Found a bug? [Open an issue](https://github.com/Lunamae24/Tribe-ai-app/issues)
- 💬 Questions? Check [CONTRIBUTING.md](CONTRIBUTING.md)

## What's Included

✅ FastAPI web framework  
✅ OpenAI & Anthropic AI integration  
✅ Docker containerization  
✅ Health monitoring  
✅ Security best practices  
✅ Comprehensive documentation  
✅ Testing infrastructure  
✅ CI/CD pipeline  
✅ Production-ready configuration  

## Success! 🎉

You're now running the Tribe AI Application!

Try sending a chat message:
```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is artificial intelligence?",
    "model": "gpt-4"
  }'
```

Happy coding! 🚀
