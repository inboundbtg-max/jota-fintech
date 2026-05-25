# 🧪 TESTES AUTOMATIZADOS (pytest)
import pytest
from schemas import BriefingInput, AgentOutput, ConsolidatedReport
from agents import StrategicAgent, SocialMediaAgent, ConsolidatorAgent
from error_handler import retry_with_backoff, RetryConfig, ErrorMetrics
from logger import setup_logger

logger = setup_logger(__name__)


# =====================================================
# TESTES DE SCHEMAS (Validação)
# =====================================================

class TestSchemas:
    """Testa validação de schemas"""

    def test_briefing_input_valid(self):
        """Briefing válido deve passar"""
        briefing = BriefingInput(
            client_name="Acme Corp",
            objective="Aumentar vendas em 40%",
            budget=50000,
            timeline_months=6
        )
        assert briefing.client_name == "Acme Corp"
        assert briefing.budget == 50000

    def test_briefing_input_invalid_name(self):
        """Briefing com nome curto deve falhar"""
        with pytest.raises(ValueError):
            BriefingInput(
                client_name="Ab",  # Muito curto (min_length=3)
                objective="Aumentar vendas",
                budget=50000,
                timeline_months=6
            )

    def test_briefing_input_invalid_budget(self):
        """Briefing com orçamento inválido deve falhar"""
        with pytest.raises(ValueError):
            BriefingInput(
                client_name="Acme Corp",
                objective="Aumentar vendas",
                budget=500,  # Muito baixo (min=1000)
                timeline_months=6
            )

    def test_agent_output_empty_content(self):
        """AgentOutput com conteúdo vazio deve falhar"""
        with pytest.raises(ValueError):
            AgentOutput(content="")  # Não pode estar vazio

    def test_agent_output_valid(self):
        """AgentOutput válido deve passar"""
        output = AgentOutput(
            content="Análise realizada",
            tokens_used=1000,
            execution_time=45.3
        )
        assert output.tokens_used == 1000
        assert output.error is None


# =====================================================
# TESTES DE AGENTES (Funcionamento)
# =====================================================

class TestAgents:
    """Testa execução dos agentes"""

    def test_strategic_agent_initialization(self):
        """Agente estratégico deve inicializar"""
        agent = StrategicAgent()
        assert agent.name == "STRATEGIC_PLANNER"
        assert agent.llm is not None

    def test_strategic_agent_execute(self):
        """Agente estratégico deve executar e retornar output válido"""
        agent = StrategicAgent()
        result = agent.execute({"briefing": "Cliente quer aumentar vendas"})

        # Assertions
        assert isinstance(result, AgentOutput)
        assert result.content is not None
        assert len(result.content) > 0
        assert result.error is None
        logger.info(f"✅ Agent execution: {result.tokens_used} tokens in {result.execution_time}s")

    def test_social_media_agent_execute(self):
        """Agente de social media deve executar"""
        agent = SocialMediaAgent()
        result = agent.execute({"briefing": "E-commerce de roupas"})

        assert isinstance(result, AgentOutput)
        assert result.error is None

    def test_consolidator_agent_execute(self):
        """Agente consolidador deve executar"""
        agent = ConsolidatorAgent()
        result = agent.execute({
            "plano_estrategico": "Aumentar presença online",
            "insights_social": "Tendência de reels curtos"
        })

        assert isinstance(result, AgentOutput)
        assert result.error is None


# =====================================================
# TESTES DE ERROR HANDLING
# =====================================================

class TestErrorHandling:
    """Testa retry e tratamento de erros"""

    def test_retry_success_first_attempt(self):
        """Função bem-sucedida na 1ª tentativa"""
        call_count = 0

        @retry_with_backoff()
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_function()
        assert result == "success"
        assert call_count == 1

    def test_retry_fails_then_succeeds(self):
        """Função falha 1x, depois sucede"""
        call_count = 0

        @retry_with_backoff(config=RetryConfig(max_retries=3, initial_delay=0.1))
        def sometimes_fails():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Erro temporário")
            return "success"

        result = sometimes_fails()
        assert result == "success"
        assert call_count == 2

    def test_retry_exhausts_attempts(self):
        """Função sempre falha, retry se exaure"""
        call_count = 0

        @retry_with_backoff(config=RetryConfig(max_retries=2, initial_delay=0.05))
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise ValueError("Erro persistente")

        with pytest.raises(ValueError):
            always_fails()

        assert call_count == 3  # 0, 1, 2 (total 3)

    def test_error_metrics(self):
        """ErrorMetrics deve rastrear erros"""
        metrics = ErrorMetrics()
        metrics.record_error("my_function", "ValueError", "Erro de validação")
        metrics.record_error("my_function", "ValueError", "Outro erro")
        metrics.record_error("other_function", "ConnectionError", "Conexão falhou")

        report = metrics.get_report()
        assert report["total_errors"] == 3
        assert report["errors_by_type"]["ValueError"] == 2
        assert report["errors_by_type"]["ConnectionError"] == 1
        assert report["errors_by_function"]["my_function"] == 2


# =====================================================
# TESTES DE INTEGRAÇÃO
# =====================================================

class TestIntegration:
    """Testa fluxo completo"""

    def test_full_pipeline(self):
        """Pipeline completo deve funcionar"""
        briefing = BriefingInput(
            client_name="Test Corp",
            objective="Testar sistema",
            budget=30000,
            timeline_months=3
        )

        # Agente 1
        agent1 = StrategicAgent()
        output1 = agent1.execute({"briefing": briefing.objective})
        assert output1.error is None

        # Agente 2
        agent2 = SocialMediaAgent()
        output2 = agent2.execute({"briefing": briefing.objective})
        assert output2.error is None

        # Agente 3
        agent3 = ConsolidatorAgent()
        output3 = agent3.execute({
            "plano_estrategico": output1.content[:200],
            "insights_social": output2.content[:200]
        })
        assert output3.error is None

        logger.info("✅ Full pipeline test passed!")


# =====================================================
# COMO RODAR OS TESTES
# =====================================================
"""
No PowerShell:

1. Instalar pytest:
   pip install pytest

2. Rodar todos os testes:
   pytest test_agents.py -v

3. Rodar apenas um teste:
   pytest test_agents.py::TestSchemas::test_briefing_input_valid -v

4. Rodar com coverage (cobertura):
   pip install pytest-cov
   pytest test_agents.py --cov=. --cov-report=html

5. Rodar com output detalhado:
   pytest test_agents.py -v -s
"""
