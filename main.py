import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Carrega as variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="Agente Estratégico ATS - Sprint 2",
    description="Backend conversacional para adequação de currículos usando LLM.",
    version="2.0.0"
)

# Modelos Pydantic para a nova estrutura conversacional
class MessageData(BaseModel):
    role: str = Field(..., description="'user' ou 'assistant'")
    content: str = Field(..., description="Conteúdo da mensagem")

class ChatRequest(BaseModel):
    messages: List[MessageData]

class ChatResponse(BaseModel):
    reply: str

# Sistema base do Agente (Persona e Instruções de Fluxo da Sprint 2)
SYSTEM_PROMPT = """Você atua como um Recrutador Tech Consultivo e Especialista em ATS (Applicant Tracking System).
Seu objetivo é guiar o candidato em um processo interativo e passo a passo para otimizar seu currículo para uma vaga específica.

ETAPAS OBRIGATÓRIAS DO FLUXO:
1. Coleta da Vaga: A conversa inicia pedindo a Vaga. Se o usuário enviar apenas um "título" de vaga ou for muito vago, VOCÊ DEVE OBRIGATORIAMENTE pedir a "descrição completa da vaga" ou o "link da vaga". Nunca prossiga sem a descrição detalhada da vaga.
2. Coleta do Currículo: Assim que receber a descrição detalhada da vaga, agradeça e PEÇA o Currículo ou Resumo Profissional. Não faça a análise ainda.
3. Diagnóstico e Mentoria: ATENÇÃO! Quando você já tiver a DESCRIÇÃO DA VAGA e o CURRÍCULO em mãos, você DEVE IMEDIATAMENTE apresentar a Análise de Aderência (Diagnóstico) nessa mesma resposta. Não diga "vou analisar e volto", faça a análise agora mesmo! Liste de 1 a 3 lacunas principais. Em seguida, na mesma resposta, pergunte se o candidato deseja ajuda para reescrever um tópico do currículo usando o método STAR (Situação, Tarefa, Ação, Resultado).
4. Geração do Currículo Final: Ao final, após as correções e quando o candidato aprovar as mudanças, você DEVE gerar a versão completa do novo currículo otimizado e colocá-la EXCLUSIVAMENTE dentro das tags <CURRICULO_FINAL> e </CURRICULO_FINAL>. Importante: Mantenha o currículo extremamente conciso, profissional e estruturado para caber em 1 página (foco em ATS). Use Markdown puro (# para Nome, ## para seções, e bullet points). Exemplo: <CURRICULO_FINAL> # Nome ... </CURRICULO_FINAL>.

REGRAS GERAIS E TRATAMENTO DE AMBIGUIDADE:
- Se a vaga for só um título (ex: "Desenvolvedor Java"), peça os requisitos da vaga antes de continuar.
- Se o currículo for curtíssimo, peça mais detalhes.
- Tom de voz: empático, direto, construtivo e focado no crescimento.
- Leia e lembre-se do histórico da conversa. Nunca repita perguntas se o usuário já forneceu a informação.
- NUNCA adie uma ação. Se você tem os dados para a análise, entregue o resultado imediatamente na mesma mensagem.
"""

@app.post("/chat", response_model=ChatResponse)
async def chat_agent(request: ChatRequest):
    try:
        # Instancia o LLM
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        # Converter formato de lista de dicionários para o formato de mensagens do LangChain
        langchain_messages = [SystemMessage(content=SYSTEM_PROMPT)]
        
        for msg in request.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
                
        # Invocação do modelo com o histórico conversacional
        response = llm.invoke(langchain_messages)
        
        return ChatResponse(reply=response.content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor ao processar o LLM: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Executa o servidor
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
