# 🔬 RESEARCH AGENT - Claude como Pesquisador Autônomo
# ====================================================
# Este agente trabalha SOZINHO fazendo análises profundas
# Diferente dos outros agentes que recebem contexto,
# este toma SUAS PRÓPRIAS DECISÕES de pesquisa

from base_agent_claude import BaseAgentClaude
from config import CLAUDE_MODEL
from logger import setup_logger
from schemas import AgentOutput
import time

logger = setup_logger(__name__)


class ResearchAgent(BaseAgentClaude):
    """
    Agente de Pesquisa Autônoma.

    Diferença vs StrategicAgent:
    - Strategic: "Analise este contexto" (recebe dados prontos)
    - Research: "Pesquise X" (faz análise profunda SOZINHO)

    Exemplo:
        researcher = ResearchAgent()
        task = {
            "topic": "Google Ads CPM Brasil 2025",
            "depth": "profundo",
            "format": "relatório estruturado"
        }
        result = researcher.execute(task)
        print(result.content)
    """

    def __init__(self):
        # Prompt customizado para pesquisa autônoma
        research_prompt = """
        Você é um pesquisador especializado em marketing digital e Google Ads.

        Sua tarefa é analisar e pesquisar tópicos COM PROFUNDIDADE:
        - Colete dados e benchmarks reais
        - Identifique tendências do mercado
        - Cite fontes quando possível
        - Estruture em seções claras
        - Forneça números, percentuais, estimativas
        - Seja específico para o contexto brasileiro

        Trabalhe autonomamente. Não espere inputs do usuário - tome suas próprias decisões
        sobre o que pesquisar para responder completamente.
        """

        super().__init__(
            name="RESEARCH_AGENT",
            system_prompt=research_prompt,
            model=CLAUDE_MODEL
        )

    def execute(self, task: dict) -> AgentOutput:
        """
        Executa pesquisa autônoma.

        Args:
            task: {
                "topic": "O que pesquisar",
                "depth": "rápido" | "profundo",
                "format": "paragrafos" | "lista" | "relatório"
            }

        Returns:
            AgentOutput com análise detalhada
        """
        try:
            logger.info(f"🔬 [{self.name}] Iniciando pesquisa autônoma: {task.get('topic', 'indefinido')}")

            # Constrói prompt com instruções de pesquisa
            topic = task.get("topic", "Análise geral")
            depth = task.get("depth", "profundo")
            format_type = task.get("format", "relatório")

            prompt = f"""
            PESQUISE E ANALISE ESTE TÓPICO:

            Tema: {topic}
            Profundidade: {depth}
            Formato: {format_type}

            Instruções:
            1. Faça uma análise COMPLETA e INDEPENDENTE
            2. Inclua dados, benchmarks, tendências
            3. Se for "profundo", vá além do óbvio
            4. Estruture bem a resposta
            5. Seja específico para Brasil quando relevante

            Comece a pesquisa agora:
            """

            start_time = time.time()

            # Chama Claude API (que tem acesso a conhecimento até data de corte)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,  # Mais tokens pra pesquisa longa
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            execution_time = time.time() - start_time
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            logger.info(f"✅ [{self.name}] Pesquisa concluída | Tokens: {tokens_used} | Tempo: {execution_time:.1f}s")

            return AgentOutput(
                content=content,
                tokens_used=tokens_used,
                error=None,
                execution_time=execution_time
            )

        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ [{self.name}] Erro na pesquisa: {error_msg}")
            return AgentOutput(
                content="",
                tokens_used=0,
                error=error_msg,
                execution_time=0
            )


# ====================================================
# TESTE
# ====================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🔬 TESTANDO RESEARCH AGENT (Pesquisador Autônomo)")
    print("=" * 70)

    researcher = ResearchAgent()

    # Tarefa de pesquisa
    task = {
        "topic": "Google Ads CPM e CPC no Brasil em 2025 - Tendências e Benchmarks",
        "depth": "profundo",
        "format": "relatório"
    }

    print(f"\n🔍 Pesquisando: {task['topic']}")
    print(f"⏳ Aguarde (pode levar 30-60 segundos)...\n")

    result = researcher.execute(task)

    if result.error:
        print(f"❌ Erro: {result.error}")
    else:
        print(f"✅ Pesquisa Concluída!")
        print(f"📊 Tokens: {result.tokens_used}")
        print(f"⏱️  Tempo: {result.execution_time:.1f}s")
        print(f"\n📝 RESULTADO:\n")
        print(result.content)
