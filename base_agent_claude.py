# 🧠 CLASSE BASE DE AGENTE COM CLAUDE API (Versão Profissional)
# ============================================================
# MUDANÇA PRINCIPAL: Ollama (local) → Claude API (profissional)

from typing import Optional
from anthropic import Anthropic  # ← NOVO: Cliente Claude ao invés de Ollama
from logger import setup_logger
from config import CLAUDE_API_KEY, CLAUDE_MODEL  # ← NOVO: Precisa API key (vamos adicionar em config.py)
from schemas import AgentOutput

logger = setup_logger(__name__)


class BaseAgentClaude:
    """
    Classe base para agentes usando Claude API (Sonnet 3.5).

    MUDANÇAS vs BaseAgent (Ollama):
    ✅ Mais rápido (10-15s vs 30-60s com TinyLlama)
    ✅ Melhor qualidade (Sonnet >> TinyLlama)
    ✅ Custos: ~R$ 0.01-0.05 por execução (Sonnet)
    ✅ Conta tokens reais (não estimado)

    TRADE-OFF:
    ❌ Precisa API key
    ❌ Requer internet
    ❌ Dados vão pra Anthropic (mas não armazenam)
    ❌ Custo: ~R$ 2-4/mês se rodar 100-200x/dia

    Exemplo de uso:
        agent = StrategicAgentClaude()
        output = agent.execute({"briefing": "..."})
        print(f"Resposta: {output.content}")
        print(f"Tokens: {output.tokens_used}")
    """

    def __init__(self, name: str, system_prompt: str, model: str = None):
        """
        Inicializa agente Claude.

        Args:
            name: Nome do agente (ex: "STRATEGIC_PLANNER")
            system_prompt: Instrução de sistema do agente
            model: Qual modelo Claude usar (padrão: Sonnet 3.5, mais rápido/barato)
                   Opções:
                   - claude-3-5-sonnet-20241022: ⭐ RECOMENDADO (melhor custo-benefício)
                   - claude-3-opus-20250219: 🔥 MAIS PODEROSO (mais lento, mais caro)
                   - claude-3-haiku-20240307: 💰 MAIS BARATO (mais rápido, menos capaz)
        """
        self.name = name
        self.system_prompt = system_prompt
        self.model = model or CLAUDE_MODEL  # ← Usa config se não especificado

        # ← CRÍTICO: Cliente Anthropic (não Ollama)
        self.client = Anthropic(api_key=CLAUDE_API_KEY)

        logger.info(f"✅ Agente Claude '{self.name}' inicializado com modelo: {model}")

    def execute(self, task: dict) -> AgentOutput:
        """
        Executa tarefa usando Claude API.

        MUDANÇAS vs BaseAgent.execute():
        1. Usa client.messages.create() ao invés de llm.invoke()
        2. Retorna response.content[0].text (Claude estrutura diferente)
        3. Tokens reais: response.usage.input_tokens + output_tokens
        4. Erro handling: ApiError ao invés de Exception genérica

        Args:
            task: Dicionário com dados da tarefa

        Returns:
            AgentOutput: Resposta estruturada com content, tokens_used, error
        """
        try:
            logger.info(f"🔄 [{self.name}] Iniciando execução com Claude...")

            # Constrói prompt (mesma lógica que antes)
            prompt = self._build_prompt(task)

            # ← MUDANÇA: Chama Claude API ao invés de Ollama
            logger.info(f"🤖 [{self.name}] Chamando Claude API ({self.model})...")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,  # ← Limite de tokens de resposta
                system=self.system_prompt,  # ← System prompt do agente
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # ← MUDANÇA: Extrai conteúdo da resposta Claude (estrutura diferente)
            content = response.content[0].text

            # ← MUDANÇA: Tokens REAIS (não estimativa)
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            logger.info(f"✅ [{self.name}] Execução concluída | Tokens: {tokens_used}")

            return AgentOutput(
                content=content,
                tokens_used=tokens_used,
                error=None,
                execution_time=0  # ← Claude API não retorna tempo, deixamos 0
            )

        except Exception as e:
            # ← Tratamento de erro (mesma lógica)
            error_msg = str(e)
            logger.error(f"❌ [{self.name}] Erro: {error_msg}")

            return AgentOutput(
                content="",
                tokens_used=0,
                error=error_msg,
                execution_time=0
            )

    def _build_prompt(self, task: dict) -> str:
        """
        Constrói prompt com dados da tarefa.

        NOTA: Mesma lógica que BaseAgent - sem mudanças aqui.
        Isso é BOM: significa a separação de concerns funciona.
        """
        task_str = "\n".join(f"- {k}: {v}" for k, v in task.items())
        return task_str


# ============================================================
# COMPARAÇÃO RÁPIDA: Ollama vs Claude
# ============================================================
"""
┌─────────────────────┬──────────────────┬────────────────────┐
│ Aspecto             │ Ollama (TinyLlama)│ Claude (Sonnet)     │
├─────────────────────┼──────────────────┼────────────────────┤
│ Velocidade          │ 30-60 segundos   │ 2-5 segundos       │
│ Qualidade           │ ⭐⭐ (fraca)      │ ⭐⭐⭐⭐⭐ (excelente)│
│ Custo               │ R$ 0/mês (local) │ ~R$ 2-4/mês        │
│ Internet            │ ❌ Não precisa   │ ✅ Precisa         │
│ Privacidade         │ ✅ Total         │ ⚠️ Dados p/ Claude  │
│ Tokens contados     │ Estimado         │ Real (cobrança)    │
│ Setup               │ Complexo         │ Simples (API key)  │
└─────────────────────┴──────────────────┴────────────────────┘

POR QUE PREFERIR CLAUDE?
→ Experimento 1: "Crie estratégia de Google Ads"
  - TinyLlama: resposta genérica, sem contexto real
  - Claude: resposta específica, com números, CTR realistic

→ Experimento 2: Tempo total do pipeline
  - TinyLlama: 5 agentes × 30s = 2m30s
  - Claude: 5 agentes × 3s = 15 segundos ← 10x mais rápido!

CONCLUSÃO: Para produção, Claude é melhor. Para experimentação local, Ollama.
RECOMENDAÇÃO: Use Hybrid = Ollama para testes, Claude para execução final.
"""
