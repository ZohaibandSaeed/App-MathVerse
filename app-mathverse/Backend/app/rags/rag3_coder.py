from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.rags.state import PipelineState
from app.rags.prompt_manager import get_system_prompt
import os

def generate_code(state: PipelineState) -> dict:
    solution_json = state["solution_json"]
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    cheat_sheet = get_system_prompt()
    sys_msg = SystemMessage(content=cheat_sheet)
    human_msg = HumanMessage(content=f"Here is the JSON solution. Convert this to Mathly Python Code, Code should be step by step and without any error.\n{solution_json}")
    
    response = llm.invoke([sys_msg, human_msg])
    
    # Clean up potential markdown formatting
    code_str = response.content.replace("```python", "").replace("```", "").strip()
    return {"generated_code": code_str}
