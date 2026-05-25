# 🤖 AGENTES ESPECÍFICOS DO DESAFIO 1
from base_agent import BaseAgent
from prompts import (
    PROMPT_AGENTE_ESTRATEGICO,
    PROMPT_AGENTE_SOCIAL_MEDIA,
    PROMPT_AGENTE_CONSOLIDADOR
)
from logger import setup_logger

logger = setup_logger(__name__)


class StrategicAgent(BaseAgent):
    """Agente especialista em planejamento estratégico"""

    def __init__(self):
        super().__init__(
            name="STRATEGIC_PLANNER",
            system_prompt=PROMPT_AGENTE_ESTRATEGICO
        )


class SocialMediaAgent(BaseAgent):
    """Agente especialista em análise de social media"""

    def __init__(self):
        super().__init__(
            name="SOCIAL_MEDIA_ANALYST",
            system_prompt=PROMPT_AGENTE_SOCIAL_MEDIA
        )


class ConsolidatorAgent(BaseAgent):
    """Agente que consolida outputs em relatório executivo"""

    def __init__(self):
        super().__init__(
            name="CONSOLIDATOR",
            system_prompt=PROMPT_AGENTE_CONSOLIDADOR
        )
