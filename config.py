# ⚙️ CONFIGURAÇÕES CENTRALIZADAS
import os
from dotenv import load_dotenv

load_dotenv()

# 🤖 Modelo LLM - Ollama Local
LLM_MODEL = "tinyllama"  # Você pode trocar para "mistral", "tinyllama"
OLLAMA_BASE_URL = "http://localhost:11434"

# 🤖 Modelo Claude API - Profissional
# OBTER API KEY: https://console.anthropic.com/account/keys
# 1. Criar conta em https://console.anthropic.com
# 2. Gerar API key (grátis, mas precisa de crédito)
# 3. Adicionar em .env file como: CLAUDE_API_KEY=sk-ant-...
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")

# Modelos disponíveis no Claude
# claude-opus-4-1 ⭐ FUNCIONANDO (Opus 4.1 - melhor modelo disponível)
# Outros modelos testados falharam com not_found_error
CLAUDE_MODEL = "claude-opus-4-1"

# 📊 Logging
LOG_LEVEL = "INFO"

# 🔌 API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
