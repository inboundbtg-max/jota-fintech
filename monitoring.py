# 📊 MONITORAMENTO E MÉTRICAS
import time
from typing import Dict, List
from datetime import datetime
from schemas import ExecutionMetrics, SystemMetrics
from logger import setup_logger

logger = setup_logger(__name__)


class PerformanceMonitor:
    """
    Monitora performance dos agentes.

    Rastreia:
    - Tempo de execução
    - Tokens utilizados
    - Taxa de sucesso
    - Custos (estimado)
    """

    def __init__(self):
        self.executions: List[ExecutionMetrics] = []
        self.start_time = datetime.now()

    def record_execution(
        self,
        agent_name: str,
        execution_time: float,
        tokens_used: int,
        status: str,
        error_message: str = None,
        retry_count: int = 0
    ) -> ExecutionMetrics:
        """
        Registra uma execução.

        Args:
            agent_name: Nome do agente
            execution_time: Tempo em segundos
            tokens_used: Tokens utilizados
            status: "success" ou "failed"
            error_message: Mensagem de erro se falhou
            retry_count: Quantas vezes tentou

        Returns:
            ExecutionMetrics: Métrica registrada
        """
        metric = ExecutionMetrics(
            agent_name=agent_name,
            execution_time=execution_time,
            tokens_used=tokens_used,
            status=status,
            error_message=error_message,
            retry_count=retry_count
        )
        self.executions.append(metric)

        # Log
        log_msg = f"📊 [{agent_name}] {status.upper()} | "
        log_msg += f"⏱️ {execution_time:.2f}s | 🔤 {tokens_used} tokens"
        if retry_count > 0:
            log_msg += f" | 🔄 {retry_count} retries"

        if status == "success":
            logger.info(log_msg)
        else:
            logger.error(log_msg + f" | ❌ {error_message}")

        return metric

    def get_system_metrics(self) -> SystemMetrics:
        """Retorna métricas gerais do sistema"""
        total = len(self.executions)
        successful = sum(1 for e in self.executions if e.status == "success")
        failed = total - successful

        avg_time = (
            sum(e.execution_time for e in self.executions) / total
            if total > 0 else 0
        )

        total_tokens = sum(e.tokens_used for e in self.executions)

        return SystemMetrics(
            total_executions=total,
            successful_executions=successful,
            failed_executions=failed,
            average_execution_time=avg_time,
            total_tokens_used=total_tokens
        )

    def get_agent_metrics(self, agent_name: str) -> Dict:
        """Retorna métricas de um agente específico"""
        agent_execs = [e for e in self.executions if e.agent_name == agent_name]

        if not agent_execs:
            return {"error": f"Nenhuma execução encontrada para {agent_name}"}

        successful = sum(1 for e in agent_execs if e.status == "success")
        failed = len(agent_execs) - successful

        avg_time = sum(e.execution_time for e in agent_execs) / len(agent_execs)
        total_tokens = sum(e.tokens_used for e in agent_execs)
        avg_tokens = total_tokens / len(agent_execs)
        total_retries = sum(e.retry_count for e in agent_execs)

        return {
            "agent": agent_name,
            "total_executions": len(agent_execs),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(agent_execs)) * 100,
            "avg_execution_time": avg_time,
            "avg_tokens": avg_tokens,
            "total_tokens": total_tokens,
            "total_retries": total_retries
        }

    def print_report(self):
        """Imprime relatório bonito de performance"""
        metrics = self.get_system_metrics()

        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DE PERFORMANCE")
        print("=" * 70)

        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print(f"  Total de execuções: {metrics.total_executions}")
        print(f"  ✅ Bem-sucedidas: {metrics.successful_executions}")
        print(f"  ❌ Falhadas: {metrics.failed_executions}")
        print(f"  📊 Taxa de sucesso: {metrics.success_rate:.1f}%")
        print(f"  ⏱️  Tempo médio: {metrics.average_execution_time:.2f}s")
        print(f"  🔤 Total de tokens: {metrics.total_tokens_used}")

        # Métricas por agente
        print(f"\n🤖 MÉTRICAS POR AGENTE:")
        agents = set(e.agent_name for e in self.executions)
        for agent in agents:
            agent_metrics = self.get_agent_metrics(agent)
            print(f"\n  {agent}:")
            print(f"    Execuções: {agent_metrics['total_executions']}")
            print(f"    Taxa de sucesso: {agent_metrics['success_rate']:.1f}%")
            print(f"    Tempo médio: {agent_metrics['avg_execution_time']:.2f}s")
            print(f"    Tokens médios: {agent_metrics['avg_tokens']:.0f}")
            print(f"    Total de retries: {agent_metrics['total_retries']}")

        # Custos estimados (Ollama local = grátis, então mostramos 0)
        print(f"\n💰 CUSTOS ESTIMADOS:")
        print(f"  Ollama local: R$ 0,00 (sem custos)")
        print(f"  API Claude: R$ 0,00 (não usado)")
        print(f"  Total: R$ 0,00")

        print("\n" + "=" * 70 + "\n")


# Instância global
monitor = PerformanceMonitor()
