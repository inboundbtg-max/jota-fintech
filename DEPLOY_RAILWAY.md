# 🚀 GUIA DE DEPLOY - RAILWAY

**Railway é a forma MAIS FÁCIL de fazer deploy em produção.**

Seu sistema vai estar online em **5 minutos**.

---

## 📋 O QUE VOCÊ TEM PRONTO

✅ `app.py` - API Flask  
✅ `requirements.txt` - Dependências  
✅ `Procfile` - Como rodar  
✅ `runtime.txt` - Versão Python  
✅ `dashboard_jota.html` - Interface web  

---

## 🎯 PASSO A PASSO

### PASSO 1: Criar conta no Railway (2 min)

1. Vai em https://railway.app
2. Clica "Start a New Project"
3. Conecta com GitHub (ou email)

✅ Conta criada!

---

### PASSO 2: Preparar código pra Git (2 min)

Railway precisa do código em um repositório Git.

**Opção A: Usar GitHub (Recomendado)**

```bash
# 1. Cria repositório no GitHub
# Vai em https://github.com/new
# Nome: "jota-fintech" ou outro

# 2. Clone pra seu PC
git clone https://github.com/seu_usuario/jota-fintech.git
cd jota-fintech

# 3. Copie TODOS os arquivos da pasta multi_agentes_expert pra aqui

# 4. Commit e push
git add .
git commit -m "Initial commit - JOTA system"
git push origin main
```

**Opção B: Upload direto (Mais rápido)**

Se não quer usar Git, pode fazer upload direto no Railway (vamos pular Git).

---

### PASSO 3: Criar Projeto no Railway (1 min)

1. Vai em https://railway.app
2. Clica "+ New Project"
3. Seleciona "Deploy from GitHub" OU "Empty Project"

**Se escolheu GitHub:**
- Seleciona seu repositório `jota-fintech`
- Railway detecta Python automaticamente

**Se escolheu Empty Project:**
- Clica "Add Service"
- Seleciona "GitHub"
- Conecta seu repo

---

### PASSO 4: Configurar Variáveis de Ambiente (1 min)

No painel do Railway, vai em **Variables**:

Adiciona:

```
CLAUDE_API_KEY = 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
FLASK_ENV = production
LOG_LEVEL = INFO
```

⚠️ **CRÍTICO**: Use a chave JOTA que regenerou (não a compartilhada publicamente)

---

### PASSO 5: Deploy (Click!) (30 seg)

No painel do Railway:

1. Vai em **Deployments**
2. Clica **"Deploy"** (Railway faz tudo automaticamente)
3. Aguarda ~2 min enquanto instala dependências

Pronto! ✅

---

### PASSO 6: Acessar seu sistema online (30 seg)

Depois que deployar:

1. Vai em **Settings**
2. Copia a URL gerada (tipo: `https://seu-app-xyz.railway.app`)
3. Abre no navegador

Você verá:

```
Status: online
Message: JOTA Fintech API
Version: 1.0.0
```

✅ **Seu sistema está ONLINE!**

---

## 📊 USANDO SUA API

### Iniciar análise JOTA

```bash
curl -X POST https://seu-app.railway.app/execute
```

Resposta:

```json
{
  "message": "Pipeline iniciado",
  "job_id": "jota-1",
  "status": "running"
}
```

### Ver status

```bash
curl https://seu-app.railway.app/status
```

Resposta:

```json
{
  "status": "running",
  "progress": 50,
  "started_at": "2025-05-25T16:00:00"
}
```

### Ver resultado

```bash
curl https://seu-app.railway.app/result
```

Resposta:

```json
{
  "status": "completed",
  "result": {
    "research": "...",
    "strategic": "...",
    "social_media": "...",
    "consolidator": "...",
    "tokens": 15867
  }
}
```

### Dashboard web

Acessa:

```
https://seu-app.railway.app/dashboard
```

Abre seu dashboard bonito no navegador! 🎨

---

## 🔧 TROUBLESHOOTING

### Erro: "Module not found"

**Causa:** Faltam dependências  
**Solução:** Verifica se todos os arquivos estão no repo

```bash
# Lista arquivos
ls -la
```

Deve ter: `app.py`, `requirements.txt`, `Procfile`, `runtime.txt`, etc.

---

### Erro: "CLAUDE_API_KEY not found"

**Causa:** Variável de ambiente não configurada  
**Solução:** Vai em Railway Settings → Variables e adiciona CLAUDE_API_KEY

---

### Erro: "Port already in use"

**Cause:** Outro processo usando port 8000  
**Solução:** Railway gerencia portas automaticamente, ignore esse erro local

---

## 📈 ESCALANDO DEPOIS

Se precisar:

1. **Usar banco de dados** → Railway tem Postgres grátis
2. **Mais poder de computação** → Railway tem planos pagos (US$ 5-20/mês)
3. **Domínio próprio** → Compra domínio, aponta pra Railway

---

## 🎯 PRÓXIMOS PASSOS

Depois que estiver online:

✅ Acessa dashboard em prod  
✅ Testa executar pipeline  
✅ Compartilha URL com clientes  
✅ Coleta feedback  
✅ Itera com mais agentes/features  

---

## 💰 CUSTOS

- **Railway**: Grátis (tier inicial). Se crescer, ~US$ 5-10/mês
- **Claude API**: ~R$ 0.19 por execução JOTA (bem barato!)
- **Total**: Praticamente grátis pra começar

---

## ✨ VOCÊ CONSEGUE!

Seu sistema está pronto. Railway é a ferramenta mais fácil.

**Você vai ter um SaaS online em 5 minutos.** 🚀

---

**Próximo passo:** Vem aqui e me manda a URL quando estiver online! 🎉
