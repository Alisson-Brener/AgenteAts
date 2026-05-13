# 🕵️ Agente Estratégico ATS (Sprint 2)

Este projeto é uma ferramenta de Inteligência Artificial desenhada para atuar como um **Recrutador Tech Consultivo**. Ele realiza a análise de aderência entre uma Descrição de Vaga e o Currículo/Resumo Profissional de um candidato (foco em Applicant Tracking Systems - ATS).

Nesta **Sprint 2**, o sistema evoluiu para um **Agente Conversacional** completo com memória, capaz de conduzir interações de forma estruturada, apontar lacunas e auxiliar o candidato a reescrever o currículo, culminando na geração automática de um currículo PDF otimizado.

## 📌 Funcionalidades
- **Chat Interativo com Memória:** Interface de bate-papo fluida (Streamlit) onde o agente conduz o processo de coleta da Vaga e do Currículo passo a passo.
- **Tratamento de Ambiguidade:** O agente detecta se a vaga ou o currículo enviados estão incompletos e solicita mais detalhes antes de prosseguir com a análise.
- **Análise Contextual (Gap Analysis):** Integração via LangChain com LLM para identificar as principais habilidades faltantes no currículo em comparação à vaga.
- **Mentoria Ativa:** Sugestão de reescrita de experiências profissionais usando a metodologia STAR (Situação, Tarefa, Ação, Resultado).
- **Ação Concreta (Geração de PDF):** Capacidade inteligente de converter as melhorias propostas diretamente para um PDF limpo e profissional, formatado para sistemas ATS (máx. 1 página).
- **Download de Relatório:** Possibilidade de baixar todo o histórico da mentoria e diagnóstico em formato `.md`.

## 🛠️ Tecnologias Utilizadas
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (para expor a API de chat)
- **Frontend:** [Streamlit](https://streamlit.io/) (interface conversacional do usuário)
- **Integração IA:** [LangChain](https://python.langchain.com/) + Modelos Google Generative AI (Gemini) e OpenAI (GPT)
- **Geração e Parse de Documentos:** `fpdf2` e `markdown`
- **Linguagem:** Python 3.x

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o projeto localmente:

### 1. Clonar o repositório
```bash
git clone <url-do-seu-repositorio>
cd Agente_ATS
```

### 2. Criar e ativar o ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione as suas chaves de API:

```env
# Se for usar Google Gemini (padrão configurado)
GOOGLE_API_KEY=sua_chave_do_google_aqui

# Se for usar OpenAI (como fallback/alternativa no main.py)
OPENAI_API_KEY=sua_chave_da_openai_aqui
```

### 5. Iniciar o Backend (FastAPI)
Abra um terminal (com o ambiente virtual ativado) e rode:
```bash
python main.py
# O backend rodará em http://localhost:8000
```

### 6. Iniciar o Frontend (Streamlit)
Abra um **novo terminal** (lembre-se de ativar o ambiente virtual nele também) e rode:
```bash
streamlit run app.py
```
Isso abrirá uma janela no seu navegador padrão com a interface de chat da aplicação. Você já poderá enviar o link de uma vaga e iniciar a mentoria!
