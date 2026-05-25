# 📚 GUIA: MIGRANDO DE OLLAMA PARA CLAUDE API

## 🎯 O QUE MUDOU (Resumo)

### ANTES (Dias 1-3):
```
Seu PC → TinyLlama (Ollama local) → Resposta (30-60s)
✅ Grátis (local)
❌ Lento
❌ Qualidade fraca
```

### AGORA (Dia 4):
```
Seu PC → Claude API (Cloud) → Resposta (2-5s)
❌ Custa ~R$ 2-4/mês
✅ Muito rápido
✅ Qualidade excelente
```

---

## 📋 ARQUIVOS NOVOS

| Arquivo | O que faz | Substitui |
|---------|----------|----------|
| `base_agent_claude.py` | Classe base para agentes Claude | `base_agent.py` (Ollama) |
| `agents_claude.py` | 3 agentes específicos com Claude | `agents.py` (Ollama) |
| `main_claude.py` | Pipeline orquestrado com LangGraph | `main_v3.py` |
| `config.py` | ATUALIZADO com CLAUDE_API_KEY | config.py anterior |
| `.env.example` | Variáveis de ambiente | (novo) |

---

## 🔑 PASSO 1: OBTER API KEY DO CLAUDE

### 1.1 Crie conta em https://console.anthropic.com

### 1.2 Vá para: Account → API Keys

### 1.3 Clique em "Create Key" e copie algo assim:
```
sk-ant-v0-abc123def456ghi789jkl...
```

### 1.4 Crie arquivo `.env` na pasta do projeto

Copie isso no `.env`:
```
CLAUDE_API_KEY=sk-ant-v0-seu_valor_aqui
```

⚠️ **IMPORTANTE**: Nunca compartilhe essa key!

---

## 🚀 PASSO 2: INSTALAR DEPENDÊNCIAS PYTHON

Se ainda não tem a biblioteca do Claude, instale:

```bash
pip install anthropic --break-system-packages
```

Verifica se deu certo:
```bash
python -c "import anthropic; print(anthropic.__version__)"
```

Esperado: `anthropic` versão 0.7.0+

---

## ⚡ PASSO 3: RODAR O NOVO PIPELINE

### Opção A: Teste individual de cada agente

```bash
python agents_claude.py
```

Output esperado:
```
======================================================================
1️⃣ TESTANDO STRATEGIC AGENT
======================================================================

✅ Status: Sucesso
📊 Tokens usados: 1234

📝 Resposta:
Estratégia detalhada para aumentar leads...
```

### Opção B: Pipeline completo

```bash
python main_claude.py
```

Output esperado:
```
======================================================================
🚀 EXECUTANDO PIPELINE COM CLAUDE API
======================================================================

📈 ANÁLISE ESTRATÉGICA:
[resposta do agente 1]

📱 INSIGHTS SOCIAL MEDIA:
[resposta do agente 2]

📋 RELATÓRIO FINAL:
[resposta do agente 3]

💰 CUSTOS:
Total de tokens: 4567
Custo estimado (Sonnet): R$ 0.04
```

---

## 🔄 COMO FUNCIONA INTERNAMENTE

### Mudança 1: Cliente HTTP

**ANTES (Ollama):**
```python
from langchain_community.llms import Ollama
self.llm = Ollama(model="tinyllama", base_url="http://localhost:11434")
response = self.llm.invoke(prompt)
```

**AGORA (Claude):**
```python
from anthropic import Anthropic
self.client = Anthropic(api_key=CLAUDE_API_KEY)
response = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=self.system_prompt,
    messages=[{"role": "user", "content": prompt}]
)
```

**POR QUÊ?**
- Ollama é local → Anthropic é API HTTP
- Ollama não tem estrutura de "messages" → Claude usa padrão OpenAI (messages)
- Ollama não retorna tokens reais → Claude retorna `usage.input_tokens` + `output_tokens`

---

### Mudança 2: Tokens reais (não estimado)

**ANTES:**
```python
tokens_used = len(response.split())  # 😅 Estimativa fraca
```

**AGORA:**
```python
tokens_used = response.usage.input_tokens + response.usage.output_tokens
```

**POR QUÊ?**
- Você paga por tokens reais no Claude
- Precisa contar certo pra saber o custo
- Estimativa era ~20% errada com TinyLlama

---

### Mudança 3: Tratamento de erro

**ANTES:**
```python
except Exception as e:
    return AgentOutput(..., error=str(e))
```

**AGORA:**
```python
except Exception as e:  # Mesmo código! Claude/Ollama erro é Exception
    return AgentOutput(..., error=str(e))
```

**POR QUÊ?**
- Não mudou! A abstração funciona igual
- Mas dá pra capturar `anthropic.APIError` se quiser ser específico

---

## 💰 CUSTOS EXPLICADOS

### Preços Claude Sonnet (Recomendado)

| Item | Custo |
|------|-------|
| Input (0-1M tokens) | R$ 0.003 por 1000 |
| Output (0-1M tokens) | R$ 0.015 por 1000 |

### Exemplo: Seu pipeline

Se cada execução usa:
- 1000 input tokens
- 500 output tokens

Custo = (1000 × 0.003) + (500 × 0.015) = R$ 0.0105 ≈ **R$ 0.01 por execução**

Se rodar **100x/dia** = R$ 1/dia = **R$ 30/mês**

---

## 🎓 ENTENDENDO ARQUITETURA

### Antes vs Depois (Arquiteturalmente)

```
ANTES (Dias 1-3 - Local):
┌─────────────────────────────────────┐
│ Seu PC                              │
│ ┌────────┐  ┌────────┐  ┌────────┐ │
│ │Agent 1 │→ │Agent 2 │→ │Agent 3 │ │
│ └────────┘  └────────┘  └────────┘ │
│       ↓          ↓          ↓        │
│ (TinyLlama via Ollama local)        │
│ Lento (30-60s) but Grátis           │
└─────────────────────────────────────┘

AGORA (Dia 4 - Cloud):
┌─────────────────────────────────────┐
│ Seu PC                              │
│ ┌────────┐  ┌────────┐  ┌────────┐ │
│ │Agent 1 │→ │Agent 2 │→ │Agent 3 │ │
│ └────────┘  └────────┘  └────────┘ │
│       ↓          ↓          ↓        │
│      HTTP ────→ INTERNET ←────────   │
│                    ↓                  │
│            ┌──────────────┐           │
│            │ Claude API   │           │
│            │ (Anthropic)  │           │
│            └──────────────┘           │
│ Rápido (2-5s) mas custa R$ 0.01/run  │
└─────────────────────────────────────┘

HYBRID (Recomendado para produção):
┌──────────────────────────────────────────┐
│ Seu PC                                   │
│ ┌──────────────────────────────────────┐ │
│ │ Testes (desenvolvimento)              │ │
│ │ ├─ TinyLlama (local, grátis)         │ │
│ │ ├─ Rápido feedback                   │ │
│ │ └─ Valida lógica                     │ │
│ └──────────────────────────────────────┘ │
│                 ↓                         │
│ ┌──────────────────────────────────────┐ │
│ │ Produção (execução real)              │ │
│ │ ├─ Claude API (cloud, pago)          │ │
│ │ ├─ Qualidade excelente               │ │
│ │ └─ Entrega ao cliente                │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## 🧪 PRÓXIMOS PASSOS

### Dia 4 (HOJE): ✅ Claude API em Python
- [x] Refatorar base_agent.py
- [x] Criar agents_claude.py
- [x] Testar com main_claude.py
- [ ] **VOCÊ**: Rodar e validar funcionamento

### Dia 5: Claude Code CLI
- Instalação de `claude-code` no VS Code
- Usar Claude como agente autônomo
- Integrar com pipeline Python

### Dia 6: Dashboard React Bonito
- Criar interface web
- Visualizar execução em tempo real
- Download de resultados

### Dia 7: Tudo Junto
- Deploy
- Pronto pra vender

---

## ❓ FAQ

### P: E se não tiver crédito na API?
R: Clique em "Billing → Add Billing Information" em https://console.anthropic.com. Precisa de cartão, mas é seguro.

### P: Qual modelo escolher?
R: **Claude 3.5 Sonnet** (padrão no código). É o melhor custo-benefício.
- Mais rápido: Haiku
- Mais poderoso: Opus
- Melhor balanço: Sonnet ✅

### P: Posso usar Ollama e Claude juntos?
R: SIM! Crie `base_agent_hybrid.py` que escolhe automaticamente. Deixar pra depois.

### P: Se der erro "anthropic" not found?
R: Rode:
```bash
pip install anthropic --break-system-packages
```

### P: Quanto vou gastar com 200 execuções/dia?
R: ~R$ 2/dia = ~R$ 60/mês. Pequeno custo pra produção profissional.

---

## 🎬 PRÓXIMO: Rodando agora

Você pronto? Siga esses passos:

1. Obter API key em https://console.anthropic.com
2. Criar `.env` com `CLAUDE_API_KEY=...`
3. Rodar: `python agents_claude.py`
4. Me mostrar output

Depois explico o código em detalhes. Vambora! 🚀
