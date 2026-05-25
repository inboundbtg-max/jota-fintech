# 🎼 ORQUESTRADOR (Coordena todos os agentes)
from agents import StrategicAgent, SocialMediaAgent, ConsolidatorAgent
from logger import setup_logger
from pydantic import BaseModel

logger = setup_logger(__name__)


class OrchestratorState(BaseModel):
    """Estado compartilhado entre agentes (tipo um 'balde' que passa dados)"""
    briefing: str
    strategic_output: str = ""
    social_output: str = ""
    final_report: str = ""


class Orchestrator:
    """
    Coordena a execução sequencial dos agentes.

    Padrão:
    1. Agente 1 (Strategic) recebe briefing
    2. Agente 2 (Social) recebe output de Agente 1
    3. Agente 3 (Consolidador) consolida tudo

    Este é o padrão BÁSICO. Depois refatoraremos com LangGraph.
    """

    def __init__(self):
        self.strategic = StrategicAgent()
        self.social = SocialMediaAgent()
        self.consolidator = ConsolidatorAgent()
        logger.info("✅ Orquestrador inicializado com 3 agentes")

    def execute(self, briefing: str) -> OrchestratorState:
        """
        Executa o fluxo completo.

        Args:
            briefing: Briefing do cliente

        Returns:
            OrchestratorState: Estado final com todos os outputs
        """
        logger.info("=" * 60)
        logger.info("🚀 INICIANDO FLUXO MULTI-AGENTE")
        logger.info("=" * 60)

        state = OrchestratorState(briefing=briefing)

        # PASSO 1: Agente Estratégico
        logger.info("\n📍 PASSO 1: Executando Agente Estratégico...")
        strategic_result = self.strategic.execute({
            "briefing": briefing
        })

        if strategic_result.error:
            logger.error(f"❌ Agente Estratégico falhou: {strategic_result.error}")
            return state

        state.strategic_output = strategic_result.content
        logger.info(f"✅ Agente Estratégico concluído ({strategic_result.tokens_used} tokens)")

        # PASSO 2: Agente Social Media
        logger.info("\n📍 PASSO 2: Executando Agente Social Media...")
        social_result = self.social.execute({
            "estrategia_base": state.strategic_output[:500],  # Passa resumo
            "briefing": briefing
        })

        if social_result.error:
            logger.error(f"❌ Agente Social Media falhou: {social_result.error}")
            return state

        state.social_output = social_result.content
        logger.info(f"✅ Agente Social Media concluído ({social_result.tokens_used} tokens)")

        # PASSO 3: Agente Consolidador
        logger.info("\n📍 PASSO 3: Executando Agente Consolidador...")
        consolidation_result = self.consolidator.execute({
            "plano_estrategico": state.strategic_output[:500],
            "insights_social": state.social_output[:500],
            "briefing_original": briefing
        })

        if consolidation_result.error:
            logger.error(f"❌ Agente Consolidador falhou: {consolidation_result.error}")
            return state

        state.final_report = consolidation_result.content
        logger.info(f"✅ Agente Consolidador concluído ({consolidation_result.tokens_used} tokens)")

        logger.info("\n" + "=" * 60)
        logger.info("✅ FLUXO MULTI-AGENTE CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)

        return state
