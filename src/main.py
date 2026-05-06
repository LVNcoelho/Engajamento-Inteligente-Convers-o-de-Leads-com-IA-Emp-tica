import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Carrega as variáveis de ambiente (GOOGLE_API_KEY)
load_dotenv()

def carregar_prompt():
    """Carrega as instruções de personalidade do arquivo de texto."""
    # Garante que o caminho funcione independente de onde o script é chamado
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_prompt = os.path.join(caminho_base, "prompts", "empathy_prompt.txt")
    
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        return f.read()

def processar_interacao_empatica(comentario_usuario):
    """
    Recebe o comentário do cliente e retorna uma resposta 
    baseada na estratégia de empatia usando o Gemini.
    """
    # 1. Configura o modelo Gemini 1.5 Flash
    # Ajustado para ChatGoogleGenerativeAI para alinhar com o import
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    try:
        system_instruction = carregar_prompt()

        # 2. Monta a estrutura da conversa
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("human", "{entrada_cliente}")
        ])

        # 3. Executa a cadeia
        chain = prompt_template | llm

        resposta = chain.invoke({"entrada_cliente": comentario_usuario})
        return resposta.content
    except FileNotFoundError:
        return "Erro: O arquivo 'empathy_prompt.txt' não foi encontrado na pasta 'prompts'."
    except Exception as e:
        # Mantendo o toque personalizado que você já tinha colocado
        return f"Ops! Tive um probleminha técnico, mas a Pâmela já está verificando. Erro: {e}"

if __name__ == "__main__":
    # Simulação de um cliente desanimado no Instagram
    entrada_teste = "Estou quase desistindo. Posto coisas lindas, mas parece que ninguém liga, nem um comentário sequer..."
    
    print("\n--- 🤖 INICIANDO ATENDIMENTO IA (GEMINI) ---")
    resultado = processar_interacao_empatica(entrada_teste)
    print(f"\nResposta da sua IA:\n\n{resultado}\n")
    print("--- ✅ TESTE CONCLUÍDO ---\n")