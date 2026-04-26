import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Carrega as variáveis de ambiente (ex: OPENAI_API_KEY ou GOOGLE_API_KEY)
load_dotenv()

app = FastAPI(
    title="Agente Estratégico ATS - Sprint 1",
    description="Backend para adequação de currículos a sistemas ATS usando LLM.",
    version="1.0.0"
)

# Modelos Pydantic para validação e estrutura de dados (Input/Output)
class AnalysisRequest(BaseModel):
    job_description: str = Field(..., description="Descrição completa da vaga alvo")
    resume: str = Field(..., description="Resumo profissional ou currículo do candidato")

class AnalysisResponse(BaseModel):
    analysis_result: str = Field(..., description="Feedback consultivo gerado pelo LLM")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest):
    try:
        # Configuração do LLM via LangChain.
        # Por padrão estou usando OpenAI, mas você pode mudar facilmente para Google Generative AI se preferir.
        # Certifique-se de que a chave OPENAI_API_KEY esteja definida no seu .env
        # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        # Template de Prompt: Define a persona e a regra de restrição da Sprint 1
        prompt_template = """
        Você atua como um Recrutador Tech Consultivo e Especialista em ATS (Applicant Tracking System).
        Sua tarefa é analisar o currículo de um candidato em relação a uma vaga específica de tecnologia.
        
        REGRAS DE ANÁLISE:
        1. Compare a "Descrição da Vaga" com o "Currículo".
        2. Identifique e liste até 3 (três) palavras-chave, habilidades técnicas ou competências essenciais que são exigidas pela vaga, mas que ESTÃO FALTANDO claramente no currículo.
        3. Forneça sugestões práticas de como o candidato pode incluir essas competências no currículo (caso ele já as possua) ou como pode desenvolvê-las.
        4. O seu tom de voz DEVE ser de um "Recrutador Tech Consultivo": empático, encorajador, direto, construtivo e focado no crescimento da carreira do candidato.
        5. NÃO invente informações que não constam nos textos fornecidos.
        
        Descrição da Vaga:
        {job_description}

        Currículo / Resumo Profissional:
        {resume}
        
        Apresente o seu feedback de forma estruturada, com marcadores e bem formatada.
        """
        
        # Estruturando o prompt via LangChain
        prompt = PromptTemplate(
            input_variables=["job_description", "resume"],
            template=prompt_template
        )
        
        # Orquestração simples: Prompt -> LLM -> Parser de String
        chain = prompt | llm | StrOutputParser()
        
        # Invocação do modelo com os dados de entrada
        result = chain.invoke({
            "job_description": request.job_description,
            "resume": request.resume
        })
        
        return AnalysisResponse(analysis_result=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor ao processar o LLM: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Executa o servidor na porta 8000 com reload automático ativado
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
