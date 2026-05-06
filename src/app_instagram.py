import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Configurações de página para o visual do portfólio
st.set_page_config(page_title="Conecta Ti - IA Empática", page_icon="📸")

load_dotenv()

def processar_ia(comentario_contextualizado):
    """Conecta com o Gemini 3 Flash para gerar a resposta."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview", 
        temperature=1.0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Busca o seu prompt de empatia que já está validado
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_prompt = os.path.join(caminho_base, "prompts", "empathy_prompt.txt")
    
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        system_instruction = f.read()

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("human", "{entrada}")
    ])
    
    chain = prompt_template | llm
    return chain.invoke({"entrada": comentario_contextualizado}).content

# --- INTERFACE STREAMLIT ---
st.title("📸 Simulador de Engajamento IA")
st.markdown("### Transformando leads frios em conexões reais")

with st.sidebar:
    st.header("Configurações do Lead")
    nicho = st.selectbox("Nicho do Cliente:", ["Varejo", "Distribuidora", "Roupas e Acessórios", "Outros"])
    dor = st.radio("Principal Dor:", ["Falta de Engajamento", "Demora no Atendimento"])

st.info(f"Configuração atual: **{nicho}** focado em **{dor}**")

comentario_teste = st.text_area("Cole aqui o comentário do Instagram:", placeholder="Ex: Estou quase desistindo, ninguém comenta minhas fotos...")

if st.button("Gerar Resposta Empática ✨"):
    if comentario_teste:
        with st.spinner('A IA da Conecta Ti está analisando o sentimento...'):
            # Criamos o contexto que você planejou para o seu canal
            contexto_full = f"O cliente é do nicho {nicho} e a dor principal é {dor}. Comentário do post: {comentario_teste}"
            
            resposta = processar_ia(contexto_full)
            
            st.chat_message("assistant").write(resposta)
            st.balloons()
    else:
        st.warning("Por favor, insira um comentário para simular o atendimento.")
```python
st.markdown("---")
st.subheader("📊 Painel de Leads (Seu CRM)")
if st.checkbox("Mostrar Histórico de Atendimentos"):
    leads = buscar_leads()
    for l in leads:
        with st.expander(f"Lead #{l[0]} - {l[1]}"):
            st.write(f"**Nicho:** {l[2]} | **Dor:** {l[3]}")
            st.write(f"**Insight:** {l[5]}")