# 📋 SCHEMAS ROBUSTOS (Validação Completa)
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# =====================================================
# INPUTS (O que entra no sistema)
# =====================================================

class BriefingInput(BaseModel):
    """
    Schema para validar um briefing de cliente.

    Exemplo:
        briefing = BriefingInput(
            client_name="Acme Corp",
            objective="Aumentar vendas 40%",
            budget=50000,
            timeline_months=6
        )
    """
    client_name: str = Field(..., min_length=3, description="Nome do cliente")
    objective: str = Field(..., min_length=10, description="Objetivo principal")
    budget: float = Field(..., gt=0, description="Orçamento em R$")
    timeline_months: int = Field(..., ge=1, le=24, description="Timeline em meses")
    target_audience: Optional[str] = Field(None, description="Público-alvo")

    @validator("budget")
    def budget_must_be_reasonable(cls, v):
        """Validação customizada: orçamento tem que fazer sentido"""
        if v > 1_000_000:
            raise ValueError("Orçamento muito alto (max R$ 1 milhão)")
        if v < 1_000:
            raise ValueError("Orçamento muito baixo (min R$ 1 mil)")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "client_name": "E-commerce XYZ",
                "objective": "Aumentar vendas em 40% em 6 meses",
                "budget": 50000,
                "timeline_months": 6,
                "target_audience": "Mulheres 25-40 anos"
            }
        }


# =====================================================
# OUTPUTS (O que sai do sistema)
# =====================================================

class AgentOutput(BaseModel):
    """Output estruturado de qualquer agente"""
    content: str = Field(default="", description="Conteúdo gerado pelo agente (vazio se erro)")
    tokens_used: int = Field(default=0, description="Tokens utilizados")
    execution_time: float = Field(default=0.0, description="Tempo em segundos")
    error: Optional[str] = Field(None, description="Mensagem de erro se falhou")
    retry_count: int = Field(default=0, description="Quantas vezes tentou")

    # ← REMOVIDO: validator que exigia content não-vazio
    # Razão: Quando API falha, content="" é esperado e error tem a mensagem


class ConsolidatedReport(BaseModel):
    """Report final consolidado dos 3 agentes"""
    strategic_analysis: str = Field(..., description="Análise estratégica")
    social_insights: str = Field(..., description="Insights de social media")
    executive_summary: str = Field(..., description="Resumo executivo")
    recommendations: List[str] = Field(default_factory=list, description="Recomendações")
    next_steps: List[str] = Field(default_factory=list, description="Próximos passos")
    total_tokens: int = Field(default=0, description="Total de tokens usados")
    total_execution_time: float = Field(default=0.0, description="Tempo total em segundos")
    generated_at: datetime = Field(default_factory=datetime.now, description="Data de geração")

    @validator("recommendations", "next_steps", pre=True, always=True)
    def ensure_list(cls, v):
        """Garante que seja lista"""
        if isinstance(v, str):
            return [v]
        return v or []


# =====================================================
# METRICS (Para monitoramento)
# =====================================================

class ExecutionMetrics(BaseModel):
    """Métricas de execução para monitoramento"""
    agent_name: str
    execution_time: float
    tokens_used: int
    status: str  # "success" ou "failed"
    error_message: Optional[str] = None
    retry_count: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)

    @validator("status")
    def status_valid(cls, v):
        """Status deve ser 'success' ou 'failed'"""
        if v not in ["success", "failed"]:
            raise ValueError("Status deve ser 'success' ou 'failed'")
        return v


class SystemMetrics(BaseModel):
    """Métricas gerais do sistema"""
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time: float = 0.0
    total_tokens_used: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        """Calcula taxa de sucesso"""
        if self.total_executions == 0:
            return 0.0
        return (self.successful_executions / self.total_executions) * 100
