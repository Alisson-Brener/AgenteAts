import streamlit as st
import requests
import re
import markdown
from fpdf import FPDF

# Configuração da página
st.set_page_config(
    page_title="Agente ATS - Recrutador Consultivo (Sprint 2)",
    page_icon="🕵️",
    layout="centered"
)

st.title("Agente Estratégico ATS")
st.markdown("### Mentoria Interativa e Contínua")

# Inicializa o histórico de mensagens no estado da sessão (Memória e Contexto)
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Mensagem de boas-vindas inicial (mock) para instigar o fluxo da Etapa 1
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Olá! Sou o seu Recrutador Tech Consultivo. Vamos otimizar o seu currículo juntos! Para começarmos, por favor, cole aqui a **Descrição da Vaga** (ou o link) da oportunidade que você deseja se candidatar."
    })

# Renderiza histórico de mensagens na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Captura nova entrada do usuário
if prompt := st.chat_input("Digite sua mensagem, vaga ou currículo aqui..."):
    # Adiciona a mensagem do usuário no state e renderiza
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Spinner de carregamento para a resposta do agente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Pensando...")
        
        try:
            # Envia o histórico completo para a nova API de Chat do backend
            response = requests.post(
                "http://localhost:8000/chat",
                json={"messages": st.session_state.messages}
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_reply = data.get("reply", "")
                
                # Renderiza a resposta final
                message_placeholder.markdown(assistant_reply)
                
                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            else:
                message_placeholder.error(f"Erro na API (Status Code: {response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            message_placeholder.error("🔌 Erro de conexão. Verifique se o backend está rodando em http://localhost:8000.")
        except Exception as e:
            message_placeholder.error(f"⚠️ Ocorreu um erro inesperado: {e}")

# Sidebar para o Recurso Adicional (Alternativa A: Geração de Relatório / Ação Concreta)
st.sidebar.title("📥 Ações Extras")
st.sidebar.markdown("Use esta opção para baixar o histórico e as sugestões da nossa mentoria.")

if st.session_state.messages:
    # 1. Busca por um Currículo Final gerado
    curriculo_final_text = None
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            match = re.search(r"<CURRICULO_FINAL>(.*?)</CURRICULO_FINAL>", msg["content"], re.DOTALL)
            if match:
                curriculo_final_text = match.group(1).strip()
                break
                
    if curriculo_final_text:
        st.sidebar.success("🎉 Seu Currículo Finalizado está pronto!")
        
        # Geração do PDF em memória usando renderização HTML do fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Converte o Markdown do LLM para HTML
        html_content = markdown.markdown(curriculo_final_text)
        
        # Envolve com estilo básico para o fpdf2 renderizar melhor
        html_styled = f"""
        <font face="helvetica" size="10">
        <h1 align="center">Currículo Otimizado</h1>
        {html_content}
        </font>
        """
        
        try:
            pdf.write_html(html_styled)
        except Exception as e:
            # Fallback caso a renderização HTML falhe por tags não suportadas
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", size=10)
            texto_limpo = curriculo_final_text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, text="Aviso: A formatação premium falhou. Exibindo versão texto bruto:\n\n" + texto_limpo)
        
        pdf_bytes = bytes(pdf.output())
        
        st.sidebar.download_button(
            label="📄 Baixar Currículo em PDF",
            data=pdf_bytes,
            file_name="Curriculo_Otimizado_ATS.pdf",
            mime="application/pdf",
            type="primary" # Destaca o botão
        )
        st.sidebar.markdown("---")

    # 2. Monta o conteúdo do arquivo Markdown com base no contexto atual
    relatorio_content = "# Relatório de Mentoria ATS\n\n"
    for msg in st.session_state.messages:
        role_pt = "👤 Candidato" if msg["role"] == "user" else "🕵️ Recrutador"
        relatorio_content += f"### {role_pt}\n{msg['content']}\n\n---\n\n"
        
    st.sidebar.download_button(
        label="📄 Baixar Relatório da Mentoria (.md)",
        data=relatorio_content,
        file_name="relatorio_ats_mentoria.md",
        mime="text/markdown",
        help="Baixe o histórico completo da nossa conversa com as dicas e currículo atualizado."
    )
    
    # Botão para limpar o contexto
    if st.sidebar.button("🧹 Limpar Conversa (Recomeçar)"):
        st.session_state.messages = []
        st.rerun()
