# 🤖 AGENTES ESPECÍFICOS COM CLAUDE API
# ====================================================
# Versão profissional: 3 agentes usando Claude Sonnet

from base_agent_claude import BaseAgentClaude
from prompts import (
    PROMPT_AGENTE_ESTRATEGICO,
    PROMPT_AGENTE_SOCIAL_MEDIA,
    PROMPT_AGENTE_CONSOLIDADOR
)
from config import CLAUDE_MODEL  # ← Pega modelo do config.py


class StrategicAgentClaude(BaseAgentClaude):
    """
    Agente estratégico: Analisa briefing, propõe estratégia.

    MUDANÇA: Agora usa Claude (antes usava TinyLlama via Ollama)

    IMPACTO:
    ✅ Resposta muito melhor qualidade
    ✅ Entende contexto complexo
    ✅ Mais rápido (~3s vs 30s)

    EXEMPLO:
        agent = StrategicAgentClaude()
        task = {
            "briefing": "Preciso aumentar leads do Google Ads em 40% em 3 meses",
            "current_cpc": 12.50,
            "monthly_budget": 5000
        }
        output = agent.execute(task)
        print(output.content)  # Estratégia detalhada com números reais
    """

    def __init__(self):
        super().__init__(
            name="STRATEGIC_PLANNER",
            system_prompt=PROMPT_AGENTE_ESTRATEGICO,
            model=CLAUDE_MODEL
        )


class SocialMediaAgentClaude(BaseAgentClaude):
    """
    Agente de mídia social: Cria conteúdo e estratégia.

    MUDANÇA: Agora usa Claude API

    Responsabilidades:
    - Criar conteúdo para Instagram, TikTok, LinkedIn
    - Sugerir horários de postagem
    - Estratégia de hashtags
    - Tone of voice adequado

    VANTAGEM sobre TinyLlama:
    → TinyLlama: "Poste conteúdo bom" (vago)
    → Claude: "Poste 3x/dia, horários 9-12-19h, use CTA 'Clique aqui'..." (específico)
    """

    def __init__(self):
        super().__init__(
            name="SOCIAL_MEDIA_SPECIALIST",
            system_prompt=PROMPT_AGENTE_SOCIAL_MEDIA,
            model=CLAUDE_MODEL
        )


class ConsolidatorAgentClaude(BaseAgentClaude):
    """
    Agente consolidador: Junta insights de todos os agentes.

    MUDANÇA: Agora usa Claude API

    O que faz:
    - Sintetiza output dos 2 agentes anteriores
    - Cria recomendações finais
    - Estrutura como relatório executivo
    - Identifica conflitos ou oportunidades

    CRÍTICO: Esse agente é o "maestro" que transforma múltiplos
    outputs em um relatório coerente e acionável.
    """

    def __init__(self):
        super().__init__(
            name="CONSOLIDATOR",
            system_prompt=PROMPT_AGENTE_CONSOLIDADOR,
            model=CLAUDE_MODEL
        )


# ====================================================
# COMO USAR (Exemplo completo)
# ====================================================
if __name__ == "__main__":
    # Teste individual de cada agente

    # 1️⃣ Agente Estratégico
    print("=" * 70)
    print("1️⃣ TESTANDO STRATEGIC AGENT")
    print("=" * 70)

    strategic = StrategicAgentClaude()
    task_strategic = {
        "briefing": "Precisamos aumentar leads de Google Ads em 40%",
        "current_budget": 5000,
        "target_cpc": 10.00
    }

    output_strategic = strategic.execute(task_strategic)
    print(f"\n✅ Status: {output_strategic.error if output_strategic.error else 'Sucesso'}")
    print(f"📊 Tokens usados: {output_strategic.tokens_used}")
    print(f"\n📝 Resposta:\n{output_strategic.content[:500]}...")  # Primeiros 500 chars

    # 2️⃣ Agente Social Media
    print("\n" + "=" * 70)
    print("2️⃣ TESTANDO SOCIAL MEDIA AGENT")
    print("=" * 70)

    social = SocialMediaAgentClaude()
    task_social = {
        "platform": "Instagram",
        "target_audience": "Empresários 25-40 anos",
        "product_type": "SaaS de gestão de projetos"
    }

    output_social = social.execute(task_social)
    print(f"\n✅ Status: {output_social.error if output_social.error else 'Sucesso'}")
    print(f"📊 Tokens usados: {output_social.tokens_used}")
    print(f"\n📝 Resposta:\n{output_social.content[:500]}...")

    # 3️⃣ Agente Consolidador
    print("\n" + "=" * 70)
    print("3️⃣ TESTANDO CONSOLIDATOR AGENT")
    print("=" * 70)

    consolidator = ConsolidatorAgentClaude()
    task_consolidator = {
        "strategic_analysis": output_strategic.content[:200],
        "social_insights": output_social.content[:200]
    }

    output_consolidator = consolidator.execute(task_consolidator)
    print(f"\n✅ Status: {output_consolidator.error if output_consolidator.error else 'Sucesso'}")
    print(f"📊 Tokens usados: {output_consolidator.tokens_used}")
    print(f"\n📝 Resposta:\n{output_consolidator.content[:500]}...")
