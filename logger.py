# 📝 LOGGING ESTRUTURADO (Padrão Senior)
import logging
import sys
from config import LOG_LEVEL

def setup_logger(name):
    """
    Cria um logger estruturado com timestamp, nível e mensagem.

    Exemplo:
        logger = setup_logger(__name__)
        logger.info("Agente iniciado")
        logger.error("Erro ao conectar")
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Formato com informações úteis
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # Handler para console
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
