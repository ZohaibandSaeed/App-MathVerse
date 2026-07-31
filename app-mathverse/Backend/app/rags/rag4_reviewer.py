import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.rags.state import PipelineState
from app.rags.prompt_manager import get_system_prompt

def review_code(state: PipelineState) -> dict:
    generated_code = state["generated_code"]
    
    api_key = os.environ.get("rag4_GEMINI_API_KEY", "")
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0, google_api_key=api_key)
    
    cheat_sheet = get_system_prompt()
    sys_msg = SystemMessage(
        content=f"""You are an expert Python and Math Code Reviewer. 
Your job is to review Python code that uses the `mathly` library.
Here is the official documentation for the library:
{cheat_sheet}

CRITICAL INSTRUCTIONS FOR REVIEW:
1. Specifically, look for the `board.add_step(equation, description)` lines. Ensure that the `equation` string uses proper LaTeX symbols for math display (e.g., using `\\times` instead of `*` for multiplication, proper superscripts, etc.).
2. Ensure the code strictly follows the Mathly Cheat Sheet.
3. DO NOT change the executable python logic or expressions inside `plot_function` which must remain standard python math syntax. ONLY fix the display strings in `add_step` and syntax errors related to Mathly rules.
4. Return ONLY the final corrected python code, with no markdown formatting."""
    )
    
    human_msg = HumanMessage(content=f"Review and fix this code:\n{generated_code}")
    
    response = llm.invoke([sys_msg, human_msg])
    
    final_code = response.content.replace("```python", "").replace("```", "").strip()
    return {"final_code": final_code}
