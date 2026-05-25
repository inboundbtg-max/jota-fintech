# 🧪 TESTE DE MODELOS DISPONÍVEIS
from anthropic import Anthropic
from config import CLAUDE_API_KEY

client = Anthropic(api_key=CLAUDE_API_KEY)

# Lista de modelos pra testar
models_to_test = [
    "claude-opus-4-1",
    "claude-opus-4",
    "claude-3-5-sonnet-20241022",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-opus-4-20250805",
]

print("🧪 TESTANDO MODELOS DISPONÍVEIS...\n")

for model in models_to_test:
    try:
        print(f"Testando: {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ FUNCIONA!\n")
        print(f"  Modelo: {model}")
        print(f"  Use este no config.py\n")
        break
    except Exception as e:
        error_msg = str(e)
        if "not_found_error" in error_msg:
            print(f"❌ Não encontrado")
        elif "Invalid API Key" in error_msg or "Unauthorized" in error_msg:
            print(f"❌ CHAVE INVÁLIDA!")
            print(f"\n⚠️  Sua chave pode estar expirada ou inválida.")
            print(f"Vá em: https://console.anthropic.com/account/keys\n")
            break
        elif "insufficient_quota" in error_msg:
            print(f"❌ Sem crédito")
        else:
            print(f"❌ Erro: {error_msg[:50]}...")

print("\nSe TODOS falharem com '❌ Não encontrado':")
print("→ Sua conta pode estar em Trial SEM acesso a modelos")
print("→ Você precisa ativar Billing em https://console.anthropic.com/account/billing")
