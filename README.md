# Tribe AI Platform

A comprehensive multi-model AI platform that brings together the power of GPT-5, Claude, and Gemini in one unified interface.

## 🚀 Features

- **AI Chat**: Multi-model support (GPT-5, Claude 4, Gemini 2.5 Pro)
- **Image Generation**: OpenAI gpt-image-1 for stunning visuals
- **Code Assistant**: GPT-5 powered code generation
- **Dual Auth**: JWT + Google OAuth authentication

## 🛠️ Tech Stack

- **Frontend**: React 19, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, Motor (MongoDB)
- **Database**: MongoDB
- **AI**: OpenAI, Anthropic, Google (via Emergent LLM key)

## 📦 Quick Start

### Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
yarn install
yarn start
\`\`\`

## ⚙️ Configuration

Create \`.env\` files:

**backend/.env:**
\`\`\`
MONGO_URL=mongodb://localhost:27017
DB_NAME=ai_platform_db
JWT_SECRET=your-secure-secret
EMERGENT_LLM_KEY=your-key
\`\`\`

**frontend/.env:**
\`\`\`
REACT_APP_BACKEND_URL=http://localhost:8001
\`\`\`

## 🔗 Live

**Website**: https://tribe-ai.it.com

---

Built by [donaldderouen24-code](https://github.com/donaldderouen24-code)
