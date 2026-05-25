# 🚀 ENTRY POINT - DESAFIO 1 (Dia 1)
from orchestrator import Orchestrator
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Executa o sistema completo"""

    # EXEMPLO DE BRIEFING (você pode mudar isso depois)
    briefing = """
    Cliente: E-commerce de Roupas (Moda Feminina)
    Objetivo: Aumentar vendas em 40% nos próximos 6 meses
    Orçamento: R$ 50.000/mês
    Público-alvo: Mulheres 25-40 anos, classe média-alta, urbanas
    Desafio principal: Competição com grandes players (Shein, Renner, etc)
    Pontos fortes: Produtos sustentáveis, design exclusivo, atendimento personalizado
    """

    # Inicia orquestrador
    orchestrator = Orchestrator()

    # Executa fluxo completo
    state = orchestrator.execute(briefing)

    # Exibe resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL - RELATÓRIO CONSOLIDADO")
    print("=" * 70)
    print(state.final_report)
    print("=" * 70)

    return state


if __name__ == "__main__":
    main()
