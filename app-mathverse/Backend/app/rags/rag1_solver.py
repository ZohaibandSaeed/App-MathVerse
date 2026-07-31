from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.rags.state import PipelineState
import os

def solve_math(state: PipelineState) -> dict:
    question = state["question"]
    # User requested Gemini 2.5 Pro. We use gemini-1.5-pro or 2.5-pro based on API availability.
    # We will use "gemini-1.5-pro" as it's the stable pro model, but can be changed.
    api_key = os.environ.get("rag1_GEMINI_API_KEY", "")
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.1, google_api_key=api_key)
    
    sys_msg = SystemMessage(
        content="You are an expert mathematical solver. Solve the user's question step-by-step in pure mathematical language. Do not skip any step. Do NOT write code. Do NOT format as JSON. Just provide the logical mathematical steps."
    )
    human_msg = HumanMessage(content=question)
    
    response = llm.invoke([sys_msg, human_msg])
    return {"solution_text": response.content}
