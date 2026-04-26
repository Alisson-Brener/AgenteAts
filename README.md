# 🕵️ Agente Estratégico ATS

Este projeto é uma ferramenta de Inteligência Artificial desenhada para atuar como um **Recrutador Tech Consultivo**. Ele realiza a análise de aderência entre uma Descrição de Vaga e o Currículo/Resumo Profissional de um candidato (foco em Applicant Tracking Systems - ATS).

O sistema identifica lacunas (skills faltando) e fornece um feedback empático e construtivo.

## 🛠️ Tecnologias Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (para expor a API de análise)
- **Frontend:** [Streamlit](https://streamlit.io/) (para a interface do usuário)
- **Integração IA:** [LangChain](https://python.langchain.com/) + Modelos Google Generative AI (Gemini) ou OpenAI
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
# Se for usar Google Gemini (padrão atual do main.py)
GOOGLE_API_KEY=sua_chave_do_google_aqui

# Se for usar OpenAI (caso altere o código no main.py)
OPENAI_API_KEY=sua_chave_da_openai_aqui
```

### 5. Iniciar o Backend (FastAPI)
Abra um terminal e rode:
```bash
python main.py
# O backend rodará em http://localhost:8000
```

### 6. Iniciar o Frontend (Streamlit)
Abra um **novo terminal** (lembre-se de ativar o ambiente virtual nele também) e rode:
```bash
streamlit run app.py
```
Isso abrirá uma janela no seu navegador padrão com a interface de uso da aplicação.

## 📌 Funcionalidades (Sprint 1)
- Entrada da Descrição da Vaga e Resumo do Candidato.
- Integração via LangChain com LLM para análise contextual.
- Extração de até 3 palavras-chave/habilidades que faltam no currículo do candidato com sugestões de desenvolvimento.
