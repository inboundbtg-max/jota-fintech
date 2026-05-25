# 🚀 ENTRY POINT V3 - LANGGRAPH + PPTX AUTOMÁTICO
from orchestrator_v2 import OrchestratorV2
from pptx_generator import generate_pptx_from_report
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """
    Executa o sistema completo:
    1. LangGraph orquestra os 3 agentes
    2. Gera PPTX automático com os resultados
    """

    # Briefing de exemplo
    briefing = """
    Cliente: E-commerce de Roupas (Moda Feminina)
    Objetivo: Aumentar vendas em 40% nos próximos 6 meses
    Orçamento: R$ 50.000/mês
    Público-alvo: Mulheres 25-40 anos, classe média-alta, urbanas
    Desafio principal: Competição com grandes players (Shein, Renner, etc)
    Pontos fortes: Produtos sustentáveis, design exclusivo, atendimento personalizado
    """

    print("\n" + "=" * 70)
    print("🚀 INICIANDO SISTEMA MULTI-AGENTE COM LANGGRAPH + PPTX")
    print("=" * 70 + "\n")

    # ===== PASSO 1: EXECUTAR LANGGRAPH =====
    logger.info("📍 PASSO 1: Executando orquestrador (LangGraph)...")
    orchestrator = OrchestratorV2()
    state = orchestrator.execute(briefing)

    # ===== PASSO 2: VALIDAR RESULTADO =====
    if not state["final_report"]:
        logger.error("❌ Nenhum relatório foi gerado!")
        return

    logger.info("✅ Relatório gerado com sucesso")

    # ===== PASSO 3: GERAR PPTX =====
    logger.info("📍 PASSO 2: Gerando PPTX profissional...")
    pptx_file = generate_pptx_from_report(
        briefing=briefing,
        report=state["final_report"],
        filename="relatorio_estrategico.pptx"
    )

    # ===== RESULTADO FINAL =====
    print("\n" + "=" * 70)
    print("✅ SUCESSO! Sistema executado com sucesso")
    print("=" * 70)
    print(f"\n📄 Arquivo PPTX gerado: {pptx_file}")
    print(f"📍 Localização: C:\\Users\\lucas\\Downloads\\multi_agentes_expert\\{pptx_file}")
    print("\n" + "=" * 70 + "\n")

    return state, pptx_file


if __name__ == "__main__":
    main()
