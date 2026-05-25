# 🚀 ENTRY POINT V2 - DESAFIO 1 COM LANGGRAPH
from orchestrator_v2 import OrchestratorV2
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Executa o sistema completo com LangGraph"""

    # Briefing de exemplo
    briefing = """
    Cliente: E-commerce de Roupas (Moda Feminina)
    Objetivo: Aumentar vendas em 40% nos próximos 6 meses
    Orçamento: R$ 50.000/mês
    Público-alvo: Mulheres 25-40 anos, classe média-alta, urbanas
    Desafio principal: Competição com grandes players (Shein, Renner, etc)
    Pontos fortes: Produtos sustentáveis, design exclusivo, atendimento personalizado
    """

    # Inicializa orquestrador com LangGraph
    orchestrator = OrchestratorV2()

    # Opcional: visualizar o grafo
    # orchestrator.visualize()

    # Executa fluxo completo
    state = orchestrator.execute(briefing)

    # Exibe resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL - RELATÓRIO CONSOLIDADO")
    print("=" * 70)

    if state["final_report"]:
        print(state["final_report"])
    else:
        print("❌ Nenhum relatório foi gerado (erro no fluxo)")

    print("=" * 70)

    return state


if __name__ == "__main__":
    main()
