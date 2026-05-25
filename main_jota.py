# 🚀 PIPELINE JOTA - 4 AGENTES INTEGRADOS
# ============================================================
# Research → Strategic → Social Media → Consolidator
# Resultado: Case profissional pronto pra apresentar

import time
from typing import TypedDict
from langgraph.graph import StateGraph
from agents_claude import (
    StrategicAgentClaude,
    SocialMediaAgentClaude,
    ConsolidatorAgentClaude
)
from research_agent import ResearchAgent
from logger import setup_logger
from monitoring import monitor

logger = setup_logger(__name__)


# ============================================================
# DEFINIR O ESTADO (tudo que flui entre agentes)
# ============================================================

class JotaGraphState(TypedDict):
    """Estado compartilhado entre os 4 agentes JOTA"""
    briefing: str
    research_output: str
    strategic_output: str
    social_media_output: str
    final_report: str
    total_tokens: int
    execution_times: dict


# ============================================================
# NÓ 1: RESEARCH AGENT
# ============================================================

def node_research_agent(state: JotaGraphState) -> JotaGraphState:
    """
    Agente 1: Pesquisa profunda sobre mercado de fintechs

    Pesquisa:
    - CAC benchmarks por canal
    - LTV:CAC viáveis
    - Competidores
    - Tendências 2025-2026
    """
    logger.info("=" * 70)
    logger.info("🔬 AGENTE 1: RESEARCH AGENT - PESQUISA DE MERCADO")
    logger.info("=" * 70)

    researcher = ResearchAgent()

    task = {
        "topic": """
        PESQUISA: Banking Conversacional + Growth Strategy para Fintechs Brasil 2025

        Contexto: JOTA é uma fintech de banking conversacional (WhatsApp) com US$ 8.9M em funding.
        Meta: Crescer 5x em 2026.

        PESQUISE E FORNEÇA:

        1. BENCHMARKS DE AQUISIÇÃO (CAC)
           - CAC médio por canal (Google, Meta, TikTok, Influencers, Referral)
           - CAC esperado para fintech conversacional
           - LTV:CAC viáveis (qual ratio torna viável?)

        2. ANÁLISE DE RETENÇÃO
           - Churn esperado D7, D30, estável
           - Fatores que afetam retenção em banking conversacional

        3. ANÁLISE DE COMPETIÇÃO
           - Quem são competidores diretos? (Wally, outros?)
           - Como se diferenciarem?

        4. TENDÊNCIAS 2025-2026
           - Crescimento de pagamentos conversacionais
           - Open Finance + Embedded Finance
           - IA em banking
           - Regulação (Marco IA)

        5. RECOMENDAÇÕES
           - Qual canal tem melhor ROAS para fintech?
           - Qual é o mix ideal de canais?

        Seja específico. Use números. Cite benchmarks reais. Estruture bem.
        """,
        "depth": "profundo",
        "format": "relatório estruturado"
    }

    start_time = time.time()
    output = researcher.execute(task)
    execution_time = time.time() - start_time

    monitor.record_execution(
        agent_name="RESEARCH_AGENT",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    logger.info(f"✅ Research completo | Tokens: {output.tokens_used} | Tempo: {execution_time:.1f}s")

    state["research_output"] = output.content
    state["total_tokens"] += output.tokens_used
    state["execution_times"]["research"] = execution_time

    return state


# ============================================================
# NÓ 2: STRATEGIC AGENT
# ============================================================

def node_strategic_agent(state: JotaGraphState) -> JotaGraphState:
    """
    Agente 2: Estratégia integrada baseada em research

    Propõe:
    - Mix de canais (Google, Meta, TikTok, Influencers, Referral)
    - Personas-alvo
    - Positioning statement
    - KPIs por canal
    - Budget allocation
    - Roadmap 30/60/90
    """
    logger.info("=" * 70)
    logger.info("📊 AGENTE 2: STRATEGIC AGENT - ESTRATÉGIA INTEGRADA")
    logger.info("=" * 70)

    strategist = StrategicAgentClaude()

    task = {
        "research_insights": state["research_output"][:2000],  # Resumir research pra não ficar muito grande
        "company_brief": """
            JOTA Fintech:
            - Produto: Banking Conversacional via WhatsApp
            - Funding: US$ 8.9M
            - Estágio: Pré-Série A
            - Meta 2026: Crescer 5x
            - Budget: US$ 8.9M para 24 meses (aprox R$ 1.2M/mês)
            - Usuários atuais: Desconhecido (estimado 10-50k)
            - Problema: Brand awareness zero, educação de mercado necessária
        """,
        "requirement": """
        COM BASE NA PESQUISA ACIMA, ESTRUTURE:

        1. MIX DE CANAIS (alocação de budget)
           - Google Ads: qual % e por quê?
           - Meta Ads: qual % e por quê?
           - TikTok: qual % e por quê?
           - Influencers: qual % e por quê?
           - Referral: qual % e por quê?
           - Justifique com dados de research

        2. PERSONAS-ALVO
           - Persona 1: Nome, idade, income, pain, mensagem, canal
           - Persona 2: Nome, idade, income, pain, mensagem, canal
           - Persona 3: Nome, idade, income, pain, mensagem, canal

        3. POSITIONING STATEMENT
           - 1 frase que resume o posicionamento único
           - Diferenciador vs Nubank/Inter/PagBank

        4. KPIs POR CANAL
           - Leads/dia esperados
           - CAC alvo
           - ROAS esperado
           - CPC/CPM esperado

        5. ROADMAP 30/60/90
           - O que fazer mês 1?
           - O que fazer mês 2?
           - O que fazer mês 3?
           - Métricas esperadas em cada período

        6. BUDGET ALLOCATION DETALHADO
           - Mês 1-6: quanto por canal?
           - Mês 7-12: quanto por canal?
           - Mês 13-24: quanto por canal?

        Seja específico. Use números realistas. Justifique cada decisão.
        """
    }

    start_time = time.time()
    output = strategist.execute(task)
    execution_time = time.time() - start_time

    monitor.record_execution(
        agent_name="STRATEGIC_AGENT",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    logger.info(f"✅ Strategy completo | Tokens: {output.tokens_used} | Tempo: {execution_time:.1f}s")

    state["strategic_output"] = output.content
    state["total_tokens"] += output.tokens_used
    state["execution_times"]["strategic"] = execution_time

    return state


# ============================================================
# NÓ 3: SOCIAL MEDIA AGENT
# ============================================================

def node_social_media_agent(state: JotaGraphState) -> JotaGraphState:
    """
    Agente 3: Estratégia de conteúdo e social

    Cria:
    - 100+ ideias de conteúdo
    - Por canal (TikTok, Instagram, LinkedIn, YouTube)
    - Influencers recomendados
    - Calendário 90 dias
    - Copy e messaging
    """
    logger.info("=" * 70)
    logger.info("📱 AGENTE 3: SOCIAL MEDIA AGENT - CONTEÚDO & DISTRIBUIÇÃO")
    logger.info("=" * 70)

    content_strategist = SocialMediaAgentClaude()

    task = {
        "strategic_context": state["strategic_output"][:2000],
        "requirement": """
        COM BASE NA ESTRATÉGIA ACIMA, CRIE PLANO DE CONTEÚDO:

        1. ESTRATÉGIA TIKTOK (Gen-Z, viralização)
           - Qual é o tom?
           - Temas principais?
           - 20 ideias de posts (específicas, criativas)
           - Hashtags?
           - Horários ideais?

        2. ESTRATÉGIA INSTAGRAM (Millennials, confiança)
           - Qual é o tom?
           - Formatos principais (reels, carrossel, stories)?
           - 15 ideias de posts
           - Hashtags?
           - Frequência?

        3. ESTRATÉGIA LINKEDIN (Confiança, B2B)
           - Qual é o tom?
           - Temas educacionais?
           - 10 ideias de posts
           - Frequência?

        4. ESTRATÉGIA YOUTUBE (Educação, tutorials)
           - Que tipo de conteúdo?
           - 5 ideias de vídeos
           - Duração?
           - Frequência?

        5. INFLUENCERS RECOMENDADOS
           - Tier 1: Mega influencers (1M+)
           - Tier 2: Macro (100k-1M)
           - Tier 3: Micro (10k-100k)
           - Por cada tier: 3-5 nomes específicos (pessoas reais)

        6. CALENDÁRIO 90 DIAS
           - Semana 1-4: o que postar?
           - Semana 5-8: o que postar?
           - Semana 9-12: o que postar?
           - Distribuição por canal

        7. TEMAS EDUCACIONAIS
           - Porque banking conversacional é novo
           - 5 temas para educar o mercado
           - Copy sugerido para cada tema

        Seja criativo. Use gíria Gen-Z. Pense em viralização.
        """
    }

    start_time = time.time()
    output = content_strategist.execute(task)
    execution_time = time.time() - start_time

    monitor.record_execution(
        agent_name="SOCIAL_MEDIA_SPECIALIST",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    logger.info(f"✅ Social Media completo | Tokens: {output.tokens_used} | Tempo: {execution_time:.1f}s")

    state["social_media_output"] = output.content
    state["total_tokens"] += output.tokens_used
    state["execution_times"]["social_media"] = execution_time

    return state


# ============================================================
# NÓ 4: CONSOLIDATOR AGENT
# ============================================================

def node_consolidator_agent(state: JotaGraphState) -> JotaGraphState:
    """
    Agente 4: Consolidador - Executive Briefing

    Consolida:
    - Research + Strategy + Social em 1 relatório
    - Estrutura como apresentação executiva
    - KPIs, riscos, timeline
    - Pronto pra apresentar
    """
    logger.info("=" * 70)
    logger.info("📋 AGENTE 4: CONSOLIDATOR AGENT - EXECUTIVE BRIEFING")
    logger.info("=" * 70)

    consolidator = ConsolidatorAgentClaude()

    task = {
        "research_analysis": state["research_output"][:1500],
        "strategic_plan": state["strategic_output"][:1500],
        "content_strategy": state["social_media_output"][:1500],
        "requirement": """
        CONSOLIDE TUDO ACIMA EM UM EXECUTIVE BRIEFING PROFISSIONAL:

        ESTRUTURA (tipo PPTX/Documento):

        1. EXECUTIVE SUMMARY (1 parágrafo)
           - Problema | Solução | Resultado esperado

        2. OPORTUNIDADE DE MERCADO
           - Tamanho do mercado
           - Crescimento esperado
           - Posição de JOTA

        3. ANÁLISE COMPETITIVA
           - Benchmarks
           - Diferenciadores JOTA

        4. ESTRATÉGIA (resumida)
           - Personas
           - Positioning
           - Mix de canais
           - KPIs

        5. PLANO DE EXECUÇÃO
           - Roadmap 30/60/90 dias
           - Budget allocation
           - Responsáveis (sugestão)

        6. PROJEÇÕES FINANCEIRAS
           - Usuários esperados mês 1-12
           - MRR esperado
           - CAC vs LTV
           - Break-even quando?

        7. RISCOS & MITIGAÇÕES
           - Risco 1: Alto churn Gen-Z
           - Mitigação: programa de retenção
           - Risco 2: Falta diferenciador
           - Mitigação: Foco em Pix por Voz + IA
           - Risco 3: Regulação IA
           - Mitigação: Compliance desde início

        8. PRÓXIMOS PASSOS
           - O que fazer na semana 1?
           - Quem é responsável?
           - Qual é o prazo?

        9. CONCLUSÃO
           - Por que essa estratégia funciona?
           - Quando esperamos ver resultados?

        Estruture como se fosse um deck executivo.
        Use números, dados concretos.
        Pronto pra apresentar ao board ou investidores.
        """
    }

    start_time = time.time()
    output = consolidator.execute(task)
    execution_time = time.time() - start_time

    monitor.record_execution(
        agent_name="CONSOLIDATOR",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    logger.info(f"✅ Consolidation completo | Tokens: {output.tokens_used} | Tempo: {execution_time:.1f}s")

    state["final_report"] = output.content
    state["total_tokens"] += output.tokens_used
    state["execution_times"]["consolidator"] = execution_time

    return state


# ============================================================
# COMPILAR GRAFO
# ============================================================

def build_jota_graph():
    """Constrói e compila o grafo de execução JOTA"""
    graph = StateGraph(JotaGraphState)

    # Adiciona nós
    graph.add_node("research", node_research_agent)
    graph.add_node("strategic", node_strategic_agent)
    graph.add_node("social_media", node_social_media_agent)
    graph.add_node("consolidator", node_consolidator_agent)

    # Conecta em sequência
    graph.set_entry_point("research")
    graph.add_edge("research", "strategic")
    graph.add_edge("strategic", "social_media")
    graph.add_edge("social_media", "consolidator")
    graph.set_finish_point("consolidator")

    return graph.compile()


# ============================================================
# EXECUTAR
# ============================================================

def execute_jota_pipeline():
    """Executa o pipeline completo JOTA com 4 agentes"""

    logger.info("\n" + "🚀 " * 35)
    logger.info("INICIANDO PIPELINE JOTA - CASO REAL DE FINTECH")
    logger.info("4 Agentes: Research → Strategic → Social → Consolidator")
    logger.info("🚀 " * 35 + "\n")

    # Estado inicial
    initial_state = JotaGraphState(
        briefing="""
        Cliente: JOTA Fintech
        Produto: Banking Conversacional via WhatsApp
        Funding: US$ 8.9M
        Meta: Crescer 5x em 2026
        Problema: Brand awareness zero + educação de mercado
        """,
        research_output="",
        strategic_output="",
        social_media_output="",
        final_report="",
        total_tokens=0,
        execution_times={
            "research": 0,
            "strategic": 0,
            "social_media": 0,
            "consolidator": 0
        }
    )

    # Compila e executa
    graph = build_jota_graph()
    start_time = time.time()
    final_state = graph.invoke(initial_state)
    total_time = time.time() - start_time

    # Mostra resultados
    print("\n" + "=" * 70)
    print("✅ PIPELINE JOTA CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  Total de tokens gerados: {final_state['total_tokens']:,}")
    print(f"  Custo estimado (Opus 4.1): ~R$ {final_state['total_tokens'] * 0.000012:.2f}")
    print(f"  Tempo total: {total_time:.1f}s")
    print(f"\n  ⏱️ Breakdown:")
    print(f"    - Research Agent: {final_state['execution_times']['research']:.1f}s")
    print(f"    - Strategic Agent: {final_state['execution_times']['strategic']:.1f}s")
    print(f"    - Social Media Agent: {final_state['execution_times']['social_media']:.1f}s")
    print(f"    - Consolidator Agent: {final_state['execution_times']['consolidator']:.1f}s")

    # Mostra outputs
    print("\n" + "=" * 70)
    print("🔬 RESULTADO 1: RESEARCH (MERCADO & BENCHMARKS)")
    print("=" * 70)
    print(final_state['research_output'][:1000] + "\n[...continua...]\n")

    print("\n" + "=" * 70)
    print("📊 RESULTADO 2: STRATEGIC (ESTRATÉGIA INTEGRADA)")
    print("=" * 70)
    print(final_state['strategic_output'][:1000] + "\n[...continua...]\n")

    print("\n" + "=" * 70)
    print("📱 RESULTADO 3: SOCIAL MEDIA (CONTEÚDO & DISTRIBUIÇÃO)")
    print("=" * 70)
    print(final_state['social_media_output'][:1000] + "\n[...continua...]\n")

    print("\n" + "=" * 70)
    print("📋 RESULTADO 4: CONSOLIDATOR (EXECUTIVE BRIEFING)")
    print("=" * 70)
    print(final_state['final_report'][:1000] + "\n[...continua...]\n")

    # Performance report
    print("\n" + "=" * 70)
    monitor.print_report()

    return final_state


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    result = execute_jota_pipeline()

    print("\n" + "=" * 70)
    print("✨ CASE JOTA FINALIZADO!")
    print("=" * 70)
    print("\n📄 Você recebeu:")
    print("  ✅ Análise de Mercado (Research)")
    print("  ✅ Estratégia Integrada (Strategic)")
    print("  ✅ Plano de Conteúdo (Social Media)")
    print("  ✅ Executive Briefing (Consolidator)")
    print("\n🎯 Próximo passo: Salvar outputs, criar PPTX, apresentar!")
