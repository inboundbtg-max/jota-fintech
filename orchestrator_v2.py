# 🎼 ORQUESTRADOR V2 (Com LangGraph - Padrão Senior)
from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents import StrategicAgent, SocialMediaAgent, ConsolidatorAgent
from logger import setup_logger

logger = setup_logger(__name__)


# =====================================================
# 1️⃣ DEFINIR O ESTADO (TypedDict - tipo Python)
# =====================================================
class GraphState(TypedDict):
    """
    Estado compartilhado entre todos os nós do grafo.

    Cada agente pode ler e escrever neste dicionário.
    É como um "balde" que passa dados entre agentes.
    """
    briefing: str
    strategic_output: str
    social_output: str
    final_report: str


# =====================================================
# 2️⃣ DEFINIR OS NÓS (Cada agente é um nó)
# =====================================================

def node_strategic_agent(state: GraphState) -> GraphState:
    """
    Nó 1: Agente Estratégico

    Entrada: briefing
    Saída: strategic_output
    """
    logger.info("📍 Nó 1: Executando Agente Estratégico...")

    agent = StrategicAgent()
    result = agent.execute({"briefing": state["briefing"]})

    if result.error:
        logger.error(f"❌ Nó 1 falhou: {result.error}")
        state["strategic_output"] = ""
    else:
        state["strategic_output"] = result.content
        logger.info(f"✅ Nó 1 concluído ({result.tokens_used} tokens)")

    return state


def node_social_media_agent(state: GraphState) -> GraphState:
    """
    Nó 2: Agente Social Media

    Entrada: strategic_output + briefing
    Saída: social_output
    """
    logger.info("📍 Nó 2: Executando Agente Social Media...")

    # Validação: se Nó 1 falhou, pular
    if not state["strategic_output"]:
        logger.warning("⚠️ Nó 1 não produziu output. Pulando Nó 2.")
        state["social_output"] = ""
        return state

    agent = SocialMediaAgent()
    result = agent.execute({
        "estrategia_base": state["strategic_output"][:500],
        "briefing": state["briefing"]
    })

    if result.error:
        logger.error(f"❌ Nó 2 falhou: {result.error}")
        state["social_output"] = ""
    else:
        state["social_output"] = result.content
        logger.info(f"✅ Nó 2 concluído ({result.tokens_used} tokens)")

    return state


def node_consolidator_agent(state: GraphState) -> GraphState:
    """
    Nó 3: Agente Consolidador

    Entrada: strategic_output + social_output + briefing
    Saída: final_report
    """
    logger.info("📍 Nó 3: Executando Agente Consolidador...")

    # Validação: se Nó 2 falhou, pular
    if not state["social_output"]:
        logger.warning("⚠️ Nó 2 não produziu output. Pulando Nó 3.")
        state["final_report"] = ""
        return state

    agent = ConsolidatorAgent()
    result = agent.execute({
        "plano_estrategico": state["strategic_output"][:500],
        "insights_social": state["social_output"][:500],
        "briefing_original": state["briefing"]
    })

    if result.error:
        logger.error(f"❌ Nó 3 falhou: {result.error}")
        state["final_report"] = ""
    else:
        state["final_report"] = result.content
        logger.info(f"✅ Nó 3 concluído ({result.tokens_used} tokens)")

    return state


# =====================================================
# 3️⃣ CONSTRUIR O GRAFO
# =====================================================

def build_graph():
    """
    Cria o grafo LangGraph.

    Estrutura:
        [START] → Nó 1 → Nó 2 → Nó 3 → [END]
    """

    # Criar StateGraph
    graph = StateGraph(GraphState)

    # Adicionar nós
    graph.add_node("strategic_agent", node_strategic_agent)
    graph.add_node("social_media_agent", node_social_media_agent)
    graph.add_node("consolidator_agent", node_consolidator_agent)

    # Conectar nós (edges)
    graph.add_edge("__start__", "strategic_agent")  # Começa em strategic
    graph.add_edge("strategic_agent", "social_media_agent")
    graph.add_edge("social_media_agent", "consolidator_agent")
    graph.add_edge("consolidator_agent", "__end__")  # Termina

    # Compilar
    compiled_graph = graph.compile()

    return compiled_graph


# =====================================================
# 4️⃣ EXECUTAR O GRAFO
# =====================================================

class OrchestratorV2:
    """
    Orquestrador usando LangGraph.

    Benefícios:
    - ✅ Visualização clara do fluxo
    - ✅ Reutilizável
    - ✅ Fácil de debugar
    - ✅ Padrão profissional
    """

    def __init__(self):
        self.graph = build_graph()
        logger.info("✅ Orquestrador V2 (LangGraph) inicializado")

    def execute(self, briefing: str) -> GraphState:
        """
        Executa o grafo completo.

        Args:
            briefing: Briefing do cliente

        Returns:
            GraphState: Estado final com todos os outputs
        """
        logger.info("=" * 60)
        logger.info("🚀 INICIANDO FLUXO MULTI-AGENTE (LangGraph)")
        logger.info("=" * 60)

        # Estado inicial
        initial_state: GraphState = {
            "briefing": briefing,
            "strategic_output": "",
            "social_output": "",
            "final_report": ""
        }

        # Executar grafo
        final_state = self.graph.invoke(initial_state)

        logger.info("\n" + "=" * 60)
        logger.info("✅ FLUXO MULTI-AGENTE CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)

        return final_state

    def visualize(self):
        """
        Visualiza o grafo (para debug).

        Uso:
            orch = OrchestratorV2()
            orch.visualize()  # Imprime a estrutura
        """
        print("\n📊 ESTRUTURA DO GRAFO:")
        print(self.graph.get_graph().draw_ascii())
