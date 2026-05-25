# 🤖 Sistema Multi-Agentico Expert (Semana Intensiva)

## Estrutura do Projeto (DIA 1)

```
multi_agentes_expert/
├── main.py                 # Entry point (roda tudo)
├── orchestrator.py         # 🎼 Coordena os 3 agentes
├── agents.py              # 🤖 Classes dos agentes específicos
├── base_agent.py          # 🧠 Classe base para todos agentes
├── prompts.py             # 📋 Prompts externalizados
├── config.py              # ⚙️ Configurações centralizadas
├── logger.py              # 📝 Logging estruturado
├── requirements.txt       # 📦 Dependências
└── README.md              # Este arquivo
```

## Como Funciona (Padrão Senior)

### 1️⃣ AGENTE ESTRATÉGICO
- Recebe: Briefing do cliente
- Faz: Análise estratégica profunda
- Retorna: Plano estratégico estruturado

### 2️⃣ AGENTE SOCIAL MEDIA
- Recebe: Output do Agente 1 + briefing
- Faz: Análise de social media e tendências
- Retorna: Insights de redes digitais

### 3️⃣ AGENTE CONSOLIDADOR
- Recebe: Outputs dos Agentes 1 e 2
- Faz: Consolida tudo em relatório executivo
- Retorna: Relatório final estruturado

## Fluxo de Dados

```
Briefing
   ↓
[Agente 1: Estratégico] → Strategic Output
   ↓
[Agente 2: Social Media] + Strategic Output → Social Output
   ↓
[Agente 3: Consolidador] + Todos outputs → Relatório Final
```

## Como Rodar (DIА 1)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Rodar o Sistema
```bash
python main.py
```

Você verá os 3 agentes executando em sequência, com logs estruturados mostrando o progresso.

## Conceitos Aprendidos (DIA 1)

✅ **BaseAgent**: Classe base reutilizável  
✅ **Agent Output**: Schema Pydantic (validação)  
✅ **Prompts Externalizados**: Separa lógica de conteúdo  
✅ **Logger Estruturado**: Rastreabilidade profissional  
✅ **Orquestrador**: Coordena múltiplos agentes  
✅ **State Pattern**: Dados trafegam entre agentes  

## Próximos Passos (DIAS 2-7)

- **Dia 2**: Adicionar Tools (web search, sentiment analysis)
- **Dia 3**: Refatorar com LangGraph (visualização de grafo)
- **Dia 4**: Gerar PPTX/DOCX automático
- **Dia 5-6**: Desafio 2 (APIs reais + aprovações)
- **Dia 7**: Deployment e casos reais

---

**Versão**: 0.1 (Dia 1)  
**Status**: ✅ Funcionando  
**Próxima**: Adicionar validação + error handling (Dia 3)
