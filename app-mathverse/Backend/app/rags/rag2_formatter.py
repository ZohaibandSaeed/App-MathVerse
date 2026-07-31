from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.rags.state import PipelineState
import os

def format_json(state: PipelineState) -> dict:
    question = state["question"]
    solution_text = state["solution_text"]
    
    # We use llama3-70b-8192 as the standard fast Groq model.
    llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0)
    
    sys_msg = SystemMessage(
        content="""You are an expert Data Formatter. Your job is to take a math solution and convert it into a strict JSON format.
Output ONLY raw JSON. Do not use markdown blocks.
Format:
{
  "title": "Short title of problem",
  "steps": [
    {"equation": "step 1 eq", "reason": "reason 1"},
    {"equation": "step 2 eq", "reason": "reason 2"}
  ],
  "graph": {
    "type": "calculus",
    "expression": "x**2"
  }
}"""
    )
    
    human_msg = HumanMessage(content=f"Question: {question}\\n\\nSolution:\\n{solution_text}")
    
    response = llm.invoke([sys_msg, human_msg])
    
    # Clean up potential markdown formatting
    json_str = response.content.replace("```json", "").replace("```", "").strip()
    return {"solution_json": json_str}
