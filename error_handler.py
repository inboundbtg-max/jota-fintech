# 🛡️ ERROR HANDLING COM RETRY AUTOMÁTICO
import time
from functools import wraps
from typing import Callable, Any
from logger import setup_logger

logger = setup_logger(__name__)


class RetryConfig:
    """Configuração para retry automático"""
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
        exponential_base: float = 2.0
    ):
        """
        Args:
            max_retries: Máximo de tentativas
            initial_delay: Delay inicial em segundos (exponencial)
            max_delay: Delay máximo em segundos
            exponential_base: Base exponencial (2.0 = dobra a cada tentativa)

        Exemplo:
            # Tenta 3 vezes: 1s, 2s, 4s
            config = RetryConfig(max_retries=3, initial_delay=1.0)
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base


def retry_with_backoff(
    func: Callable = None,
    config: RetryConfig = None,
    exceptions: tuple = (Exception,)
):
    """
    Decorator para retry automático com backoff exponencial.

    Uso:
        @retry_with_backoff(config=RetryConfig(max_retries=3))
        def my_function():
            return llm.invoke(prompt)

    Behavior:
        1ª tentativa: executa
        Se falhar:
            espera 1s → 2ª tentativa
            Se falhar:
                espera 2s → 3ª tentativa
                Se falhar:
                    levanta exception
    """
    if config is None:
        config = RetryConfig()

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            delay = config.initial_delay

            for attempt in range(config.max_retries + 1):
                try:
                    logger.info(f"🔄 [{f.__name__}] Tentativa {attempt + 1}/{config.max_retries + 1}")

                    result = f(*args, **kwargs)

                    if attempt > 0:
                        logger.info(f"✅ [{f.__name__}] Sucesso na tentativa {attempt + 1}")

                    return result

                except exceptions as e:
                    last_exception = e
                    logger.warning(f"⚠️ [{f.__name__}] Erro: {str(e)}")

                    # Se é a última tentativa, não espera
                    if attempt == config.max_retries:
                        logger.error(f"❌ [{f.__name__}] Falhou após {config.max_retries + 1} tentativas")
                        break

                    # Calcula delay com backoff exponencial
                    wait_time = min(
                        config.initial_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    logger.info(f"⏳ Aguardando {wait_time:.1f}s antes da próxima tentativa...")
                    time.sleep(wait_time)

            # Se chegou aqui, todas as tentativas falharam
            raise last_exception

        return wrapper

    # Se usado sem parênteses: @retry_with_backoff
    if func is not None:
        return decorator(func)

    # Se usado com parênteses: @retry_with_backoff(config=...)
    return decorator


class ErrorMetrics:
    """Rastreia erros para análise"""
    def __init__(self):
        self.total_errors = 0
        self.errors_by_type = {}
        self.errors_by_function = {}

    def record_error(self, function_name: str, error_type: str, error_msg: str):
        """Registra um erro"""
        self.total_errors += 1

        # Por tipo
        if error_type not in self.errors_by_type:
            self.errors_by_type[error_type] = 0
        self.errors_by_type[error_type] += 1

        # Por função
        if function_name not in self.errors_by_function:
            self.errors_by_function[function_name] = []
        self.errors_by_function[function_name].append({
            "error_type": error_type,
            "message": error_msg,
            "timestamp": time.time()
        })

        logger.warning(f"📊 Error recorded: {function_name} | {error_type} | {error_msg}")

    def get_report(self) -> dict:
        """Retorna relatório de erros"""
        return {
            "total_errors": self.total_errors,
            "errors_by_type": self.errors_by_type,
            "errors_by_function": {
                k: len(v) for k, v in self.errors_by_function.items()
            }
        }


# Instância global
error_metrics = ErrorMetrics()
