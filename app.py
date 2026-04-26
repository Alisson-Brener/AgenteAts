import streamlit as st
import requests

# Configuração básica da página do Streamlit
st.set_page_config(
    page_title="Agente ATS - Recrutador Consultivo",
    page_icon="🕵️",
    layout="centered"
)

st.title("🕵️ Agente Estratégico ATS")
st.markdown("### 🎯 Sprint 1: Adequação Semântica Básica")
st.markdown("""
Bem-vindo! Esta é uma ferramenta que cruza uma descrição de vaga com um resumo profissional. 
O agente vai identificar até 3 palavras-chave faltantes e dar um feedback com tom consultivo de um Tech Recruiter.
""")

# Formulário para entrada de dados
with st.form("ats_form"):
    st.subheader("📝 Dados para Análise")
    
    job_description = st.text_area(
        "📄 Descrição da Vaga", 
        height=200, 
        placeholder="Cole a descrição completa da vaga de tecnologia aqui..."
    )
    
    resume = st.text_area(
        "🧑‍💻 Seu Currículo (Resumo Profissional)", 
        height=200, 
        placeholder="Cole o seu resumo profissional, experiências e competências aqui..."
    )
    
    submit_button = st.form_submit_button(label="🔍 Analisar Aderência")

# Tratamento do evento de clique no botão
if submit_button:
    if not job_description.strip() or not resume.strip():
        st.warning("⚠️ Por favor, preencha tanto a descrição da vaga quanto o currículo para continuarmos.")
    else:
        with st.spinner("O Agente (Recrutador Tech Consultivo) está analisando o seu perfil..."):
            try:
                # Realiza a requisição POST para a API FastAPI
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={
                        "job_description": job_description,
                        "resume": resume
                    }
                )
                
                # Se a requisição for bem sucedida
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("analysis_result", "")
                    
                    st.success("✅ Análise concluída com sucesso!")
                    
                    st.markdown("---")
                    st.markdown("### 💡 Feedback Consultivo:")
                    st.write(result) # Utiliza write para renderizar markdown adequadamente
                    st.markdown("---")
                else:
                    st.error(f"❌ Erro na API (Status Code: {response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Erro de conexão. Verifique se o servidor FastAPI (Backend) está rodando na porta 8000. (python main.py)")
            except Exception as e:
                st.error(f"⚠️ Ocorreu um erro inesperado: {e}")
