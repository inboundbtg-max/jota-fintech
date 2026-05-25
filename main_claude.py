# 🚀 PIPELINE COMPLETO COM CLAUDE API
# ============================================================
# Executa 3 agentes em sequência, usando LangGraph para orquestração

import time
from typing import TypedDict
from langgraph.graph import StateGraph
from agents_claude import (
    StrategicAgentClaude,
    SocialMediaAgentClaude,
    ConsolidatorAgentClaude
)
from logger import setup_logger
from monitoring import monitor

logger = setup_logger(__name__)


# ============================================================
# DEFINIR O ESTADO (mesma coisa que antes, só que com Claude)
# ============================================================

class GraphState(TypedDict):
    """Estado compartilhado entre agentes"""
    briefing: str
    strategic_analysis: str
    social_insights: str
    final_report: str
    total_tokens: int


# ============================================================
# DEFINIR OS NÓS (cada nó = um agente executando)
# ============================================================

def node_strategic_agent(state: GraphState) -> GraphState:
    """Nó 1: Agente Estratégico analisa o briefing"""
    logger.info("🤖 Executando: STRATEGIC AGENT")

    agent = StrategicAgentClaude()
    task = {
        "briefing": state["briefing"]
    }

    start_time = time.time()
    output = agent.execute(task)
    execution_time = time.time() - start_time

    # Registra métrica
    monitor.record_execution(
        agent_name="STRATEGIC_PLANNER",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    state["strategic_analysis"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def node_social_media_agent(state: GraphState) -> GraphState:
    """Nó 2: Agente Social Media cria estratégia baseada na análise"""
    logger.info("🤖 Executando: SOCIAL MEDIA AGENT")

    agent = SocialMediaAgentClaude()
    task = {
        "strategic_context": state["strategic_analysis"],
        "briefing": state["briefing"]
    }

    start_time = time.time()
    output = agent.execute(task)
    execution_time = time.time() - start_time

    # Registra métrica
    monitor.record_execution(
        agent_name="SOCIAL_MEDIA_SPECIALIST",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    state["social_insights"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def node_consolidator_agent(state: GraphState) -> GraphState:
    """Nó 3: Consolidador junta tudo em um relatório final"""
    logger.info("🤖 Executando: CONSOLIDATOR AGENT")

    agent = ConsolidatorAgentClaude()
    task = {
        "strategic_analysis": state["strategic_analysis"],
        "social_insights": state["social_insights"],
        "briefing": state["briefing"]
    }

    start_time = time.time()
    output = agent.execute(task)
    execution_time = time.time() - start_time

    # Registra métrica
    monitor.record_execution(
        agent_name="CONSOLIDATOR",
        execution_time=execution_time,
        tokens_used=output.tokens_used,
        status="success" if not output.error else "failed",
        error_message=output.error
    )

    state["final_report"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


# ============================================================
# COMPILAR GRAFO (mesma coisa que orchestrator_v2.py)
# ============================================================

def build_graph():
    """Constrói e compila o grafo de execução"""
    graph = StateGraph(GraphState)

    # Adiciona nós
    graph.add_node("strategic_agent", node_strategic_agent)
    graph.add_node("social_media_agent", node_social_media_agent)
    graph.add_node("consolidator_agent", node_consolidator_agent)

    # Conecta nós em sequência
    graph.set_entry_point("strategic_agent")
    graph.add_edge("strategic_agent", "social_media_agent")
    graph.add_edge("social_media_agent", "consolidator_agent")
    graph.set_finish_point("consolidator_agent")

    return graph.compile()


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def execute_pipeline(briefing: str) -> dict:
    """
    Executa pipeline completo com Claude API.

    Args:
        briefing: Descrição do desafio/projeto

    Returns:
        dict com:
        - strategic_analysis: Análise estratégica
        - social_insights: Insights de social media
        - final_report: Relatório consolidado
        - total_tokens: Tokens gastos total
    """
    logger.info("🚀 Iniciando pipeline com Claude API...")

    # Cria estado inicial
    initial_state = GraphState(
        briefing=briefing,
        strategic_analysis="",
        social_insights="",
        final_report="",
        total_tokens=0
    )

    # Compila grafo
    graph = build_graph()

    # Executa
    start_time = time.time()
    final_state = graph.invoke(initial_state)
    total_time = time.time() - start_time

    logger.info(f"✅ Pipeline completo em {total_time:.2f}s | Total tokens: {final_state['total_tokens']}")

    return final_state


# ============================================================
# TESTE (executar: python main_claude.py)
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 EXECUTANDO PIPELINE COM CLAUDE API")
    print("=" * 70)

    # Briefing de teste (mesmo do Dia 1-3)
    briefing = """
    Contexto: Cliente é agência de marketing em São Paulo.
    Desafio: Aumentar leads qualificados do Google Ads em 40% nos próximos 3 meses.

    Dados atuais:
    - Orçamento mensal: R$ 5.000
    - CPC atual: R$ 12,50
    - Taxa de conversão: 2.5%
    - Leads/mês: ~40

    Meta: 56+ leads/mês mantendo CPC ≤ R$ 10

    Restrições:
    - Sem orçamento extra (máximo R$ 5k)
    - Precisa de implementação em 2 semanas
    """

    # Executa
    result = execute_pipeline(briefing)

    # Mostra resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)

    print(f"\n📈 ANÁLISE ESTRATÉGICA:\n{result['strategic_analysis'][:500]}...")
    print(f"\n📱 INSIGHTS SOCIAL MEDIA:\n{result['social_insights'][:500]}...")
    print(f"\n📋 RELATÓRIO FINAL:\n{result['final_report'][:500]}...")

    print(f"\n💰 CUSTOS:")
    print(f"  Total de tokens: {result['total_tokens']}")
    print(f"  Custo estimado (Sonnet): R$ {result['total_tokens'] * 0.000008:.2f}")
    # (Aproximação: R$ 0.000008 por token em média para Sonnet)

    # Mostra relatório de performance
    print("\n" + "=" * 70)
    monitor.print_report()
