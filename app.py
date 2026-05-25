# 🚀 API FLASK - JOTA FINTECH SYSTEM
# ============================================================
# Expõe o sistema multi-agente como API REST
# Deploy: Railway, Heroku, DigitalOcean, etc

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import time
import threading
from typing import TypedDict
from langgraph.graph import StateGraph

from agents_claude import (
    StrategicAgentClaude,
    SocialMediaAgentClaude,
    ConsolidatorAgentClaude
)
from research_agent import ResearchAgent
from logger import setup_logger
from monitoring import monitor

# Setup
app = Flask(__name__)
CORS(app)
logger = setup_logger(__name__)

# ============================================================
# ESTADO GLOBAL (simples, sem banco de dados)
# ============================================================

class JotaGraphState(TypedDict):
    """Estado compartilhado entre agentes"""
    briefing: str
    research_output: str
    strategic_output: str
    social_media_output: str
    final_report: str
    total_tokens: int
    execution_times: dict
    status: str


# Global state
current_job = {
    "status": "idle",  # idle, running, completed, error
    "progress": 0,
    "result": None,
    "error": None,
    "started_at": None,
    "completed_at": None
}


# ============================================================
# FUNÇÕES DOS AGENTES (copiadas de main_jota.py)
# ============================================================

def node_research_agent(state: JotaGraphState) -> JotaGraphState:
    """Agente 1: Research"""
    logger.info("🔬 Research Agent iniciando...")
    current_job["progress"] = 20
    current_job["status"] = "running"

    researcher = ResearchAgent()
    task = {
        "topic": """
        PESQUISA: Banking Conversacional + Growth Strategy para Fintechs Brasil 2025

        Pesquise e forneça benchmarks de CAC, LTV, análise de retenção, competidores e tendências.
        Seja específico. Use números. Estruture bem.
        """,
        "depth": "profundo",
        "format": "relatório estruturado"
    }

    output = researcher.execute(task)
    state["research_output"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def node_strategic_agent(state: JotaGraphState) -> JotaGraphState:
    """Agente 2: Strategic"""
    logger.info("📊 Strategic Agent iniciando...")
    current_job["progress"] = 40

    strategist = StrategicAgentClaude()
    task = {
        "research_insights": state["research_output"][:2000],
        "requirement": "Com base na pesquisa, estruture mix de canais, personas, positioning, KPIs, roadmap e budget allocation."
    }

    output = strategist.execute(task)
    state["strategic_output"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def node_social_media_agent(state: JotaGraphState) -> JotaGraphState:
    """Agente 3: Social Media"""
    logger.info("📱 Social Media Agent iniciando...")
    current_job["progress"] = 60

    content_strategist = SocialMediaAgentClaude()
    task = {
        "strategic_context": state["strategic_output"][:2000],
        "requirement": "Crie plano de conteúdo multi-canal com 100+ ideias, influencers, calendário 90 dias."
    }

    output = content_strategist.execute(task)
    state["social_media_output"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def node_consolidator_agent(state: JotaGraphState) -> JotaGraphState:
    """Agente 4: Consolidator"""
    logger.info("📋 Consolidator Agent iniciando...")
    current_job["progress"] = 80

    consolidator = ConsolidatorAgentClaude()
    task = {
        "research_analysis": state["research_output"][:1500],
        "strategic_plan": state["strategic_output"][:1500],
        "content_strategy": state["social_media_output"][:1500],
        "requirement": "Consolide em executive briefing profissional com KPIs, riscos, projeções."
    }

    output = consolidator.execute(task)
    state["final_report"] = output.content
    state["total_tokens"] += output.tokens_used

    return state


def build_jota_graph():
    """Constrói grafo"""
    graph = StateGraph(JotaGraphState)
    graph.add_node("research", node_research_agent)
    graph.add_node("strategic", node_strategic_agent)
    graph.add_node("social_media", node_social_media_agent)
    graph.add_node("consolidator", node_consolidator_agent)

    graph.set_entry_point("research")
    graph.add_edge("research", "strategic")
    graph.add_edge("strategic", "social_media")
    graph.add_edge("social_media", "consolidator")
    graph.set_finish_point("consolidator")

    return graph.compile()


def execute_jota_pipeline():
    """Executa pipeline em background"""
    try:
        current_job["status"] = "running"
        current_job["started_at"] = datetime.now().isoformat()

        initial_state = JotaGraphState(
            briefing="JOTA Fintech - Banking Conversacional via WhatsApp",
            research_output="",
            strategic_output="",
            social_media_output="",
            final_report="",
            total_tokens=0,
            execution_times={
                "research": 0,
                "strategic": 0,
                "social_media": 0,
                "consolidator": 0
            },
            status="running"
        )

        graph = build_jota_graph()
        result = graph.invoke(initial_state)

        current_job["status"] = "completed"
        current_job["progress"] = 100
        current_job["result"] = {
            "research": result["research_output"],
            "strategic": result["strategic_output"],
            "social_media": result["social_media_output"],
            "consolidator": result["final_report"],
            "tokens": result["total_tokens"]
        }
        current_job["completed_at"] = datetime.now().isoformat()
        logger.info("✅ Pipeline concluído com sucesso!")

    except Exception as e:
        logger.error(f"❌ Erro no pipeline: {str(e)}")
        current_job["status"] = "error"
        current_job["error"] = str(e)


# ============================================================
# ROTAS API
# ============================================================

@app.route('/', methods=['GET'])
def home():
    """Rota raiz - Status da API"""
    return jsonify({
        "status": "online",
        "message": "JOTA Fintech API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Status da API",
            "GET /health": "Health check",
            "POST /execute": "Executar pipeline JOTA",
            "GET /status": "Status do job atual",
            "GET /result": "Resultado do job",
            "GET /dashboard": "Abre dashboard"
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/execute', methods=['POST'])
def execute():
    """Inicia execução do pipeline"""
    global current_job

    if current_job["status"] == "running":
        return jsonify({
            "error": "Pipeline já está rodando",
            "progress": current_job["progress"]
        }), 400

    # Reset job
    current_job = {
        "status": "running",
        "progress": 0,
        "result": None,
        "error": None,
        "started_at": datetime.now().isoformat(),
        "completed_at": None
    }

    # Executa em thread background (não bloqueia API)
    thread = threading.Thread(target=execute_jota_pipeline)
    thread.daemon = True
    thread.start()

    return jsonify({
        "message": "Pipeline iniciado",
        "job_id": "jota-1",
        "status": "running"
    }), 202


@app.route('/status', methods=['GET'])
def get_status():
    """Status do job atual"""
    return jsonify({
        "status": current_job["status"],
        "progress": current_job["progress"],
        "started_at": current_job["started_at"],
        "completed_at": current_job["completed_at"]
    })


@app.route('/result', methods=['GET'])
def get_result():
    """Resultado do job"""
    if current_job["status"] == "running":
        return jsonify({
            "status": "running",
            "progress": current_job["progress"],
            "message": "Pipeline ainda está rodando..."
        }), 202

    if current_job["status"] == "error":
        return jsonify({
            "status": "error",
            "error": current_job["error"]
        }), 500

    if current_job["status"] == "completed":
        return jsonify({
            "status": "completed",
            "result": current_job["result"],
            "completed_at": current_job["completed_at"]
        })

    return jsonify({
        "status": "idle",
        "message": "Nenhum job executado ainda"
    })


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Retorna dashboard HTML"""
    # Você pode servir o arquivo HTML daqui
    try:
        with open('dashboard_jota.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return """
        <h1>Dashboard não encontrado</h1>
        <p>Coloque dashboard_jota.html na mesma pasta que app.py</p>
        """, 404


@app.route('/api/execute', methods=['POST'])
def api_execute():
    """Versão estruturada da execução"""
    data = request.get_json()

    # Aqui você poderia aceitar customizações do briefing
    briefing = data.get('briefing', 'JOTA Fintech - Banking Conversacional')

    if current_job["status"] == "running":
        return jsonify({
            "error": "Pipeline já está rodando",
            "progress": current_job["progress"]
        }), 400

    current_job["status"] = "running"
    current_job["progress"] = 0
    current_job["started_at"] = datetime.now().isoformat()

    thread = threading.Thread(target=execute_jota_pipeline)
    thread.daemon = True
    thread.start()

    return jsonify({
        "message": "Pipeline iniciado",
        "briefing": briefing,
        "status_url": "/status",
        "result_url": "/result"
    }), 202


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Rota não encontrada"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Erro interno do servidor"}), 500


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    # Determina porta (Railway usa PORT env var)
    port = int(os.environ.get('PORT', 8000))

    logger.info(f"🚀 API iniciando na porta {port}")
    logger.info(f"📊 Acesse http://localhost:{port}")
    logger.info(f"📋 Dashboard: http://localhost:{port}/dashboard")

    # Executa Flask
    app.run(
        host='0.0.0.0',  # Importante pra Railway
        port=port,
        debug=False  # Production mode
    )
