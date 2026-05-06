import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from database import criar_tabela, salvar_lead, buscar_leads

# Configurações da Conecta Ti
st.set_page_config(page_title="Conecta Ti - Diagnóstico IA", page_icon="🚀")
load_dotenv()
criar_tabela()

def processar_ia(comentario_contextualizado):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview", 
        temperature=1.0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_prompt = os.path.join(caminho_base, "prompts", "empathy_prompt.txt")
    
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        system_instruction = f.read()

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "{entrada}")
    ])
    
    chain = prompt_template | llm
    resultado = chain.invoke({"entrada": comentario_contextualizado})
    
    # --- NOVA LÓGICA DE LIMPEZA À PROVA DE ERROS ---
    # 1. Se for o objeto de mensagem do LangChain
    if hasattr(resultado, 'content'):
        return resultado.content
    
    # 2. Se for uma lista (o que causou o erro no print)
    if isinstance(resultado, list):
        if len(resultado) > 0 and isinstance(resultado[0], dict):
            return resultado[0].get('text', str(resultado))
        return str(resultado[0])
    
    # 3. Fallback para qualquer outro caso
    return str(resultado)

# --- INTERFACE ---
st.title("🚀 Conecta Ti - Diagnóstico")
st.markdown("### Transformando seu Instagram com IA")

with st.sidebar:
    st.header("Filtros do Lead")
    nicho = st.selectbox("Nicho:", ["Varejo", "Distribuidora", "Roupas e Acessórios", "Outros"])
    dor = st.radio("Objetivo:", ["Mais Engajamento", "Atendimento Rápido"])

# Pergunta personalizada
dificuldade = st.text_area("Qual a sua maior dificuldade?", placeholder="Ex: Sinto que falo sozinha nos meus posts...")

if st.button("Gerar Insight ✨"):
    if dificuldade:
        with st.spinner('A IA da Conecta Ti está gerando seu diagnóstico...'):
            contexto = f"Nicho: {nicho}, Dor: {dor}. Dificuldade: {dificuldade}"
            try:
                resposta_final = processar_ia(contexto)
                
                # Exibe a mensagem limpinha
                st.chat_message("assistant").write(resposta_final)
                
                # OS BALÕES! 🎈🎈🎈
                st.balloons()
                
                # Salva no seu CRM
                salvar_lead(nicho, dor, dificuldade, resposta_final)
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Me conta sua dificuldade para eu poder te ajudar!")

# Histórico
st.markdown("---")
if st.checkbox("Ver Leads Salvos"):
    for l in buscar_leads()[:3]:
        with st.expander(f"Lead de {l[2]} - {l[1]}"):
            st.write(l[5])
