import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# Carrega as variáveis de ambiente (onde estará sua API KEY)
load_dotenv()

def carregar_prompt():
    """Carrega as instruções de personalidade do arquivo de texto."""
    caminho_prompt = os.path.join("prompts", "empathy_prompt.txt")
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        return f.read()

def processar_interacao_empatica(comentario_usuario):
    """
    Recebe o comentário do cliente e retorna uma resposta 
    baseada na estratégia de empatia.
    """
    # 1. Configura o modelo (GPT-4o ou 3.5-turbo)
    # Certifique-se de ter a OPENAI_API_KEY no seu arquivo .env
    llm = ChatOpenAI(
        model="gpt-4o", 
        temperature=0.7  # Um pouco de criatividade para parecer mais humano
    )

    system_instruction = carregar_prompt()

    # 2. Monta a estrutura da conversa
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "{entrada_cliente}")
    ])

    # 3. Executa a cadeia de pensamento
    chain = prompt_template | llm

    try:
        resposta = chain.invoke({"entrada_cliente": comentario_usuario})
        return resposta.content
    except Exception as e:
        return f"Ops! Tive um probleminha técnico, mas a Pâmela já está verificando. Erro: {e}"

if __name__ == "__main__":
    # Simulação de um cliente desanimado no Instagram
    entrada_teste = "Estou quase desistindo. Posto coisas lindas, mas parece que ninguém liga, nem um comentário sequer..."
    
    print("\n--- 🤖 INICIANDO ATENDIMENTO IA ---")
    resultado = processar_interacao_empatica(entrada_teste)
    print(f"\nResposta da sua IA:\n\n{resultado}\n")
    print("--- ✅ TESTE CONCLUÍDO ---\n")