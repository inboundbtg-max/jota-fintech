# 🧠 CLASSE BASE DE AGENTE (Padrão Senior)
from typing import Optional
from langchain_community.llms import Ollama
from logger import setup_logger
from config import LLM_MODEL, OLLAMA_BASE_URL
from schemas import AgentOutput  # ✅ Importa do schemas, não duplica

logger = setup_logger(__name__)


class BaseAgent:
    """
    Classe base para todos os agentes.

    Padrão: Agent recebe um Task (dict) e retorna um Output estruturado.

    Exemplo:
        agent = StrategicAgent()
        output = agent.execute({"briefing": "..."})
        print(output.content)
    """

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = Ollama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        logger.info(f"✅ Agente '{self.name}' inicializado com modelo: {LLM_MODEL}")

    def execute(self, task: dict) -> AgentOutput:
        """
        Executa a tarefa do agente.

        Args:
            task: Dicionário com os dados da tarefa

        Returns:
            AgentOutput: Output estruturado
        """
        try:
            logger.info(f"🔄 [{self.name}] Iniciando execução...")

            # Prepara o prompt com system + conteúdo da task
            prompt = self._build_prompt(task)

            # Chama o LLM
            logger.info(f"🤖 [{self.name}] Chamando LLM...")
            response = self.llm.invoke(prompt)

            logger.info(f"✅ [{self.name}] Execução concluída")

            return AgentOutput(
                content=response,
                tokens_used=len(response.split()),  # Estimativa simples
                error=None
            )

        except Exception as e:
            logger.error(f"❌ [{self.name}] Erro: {str(e)}")
            return AgentOutput(
                content="",
                tokens_used=0,
                error=str(e)
            )

    def _build_prompt(self, task: dict) -> str:
        """Constrói o prompt completo (system + user input)"""
        task_str = "\n".join(f"- {k}: {v}" for k, v in task.items())
        return f"{self.system_prompt}\n\n{task_str}"
