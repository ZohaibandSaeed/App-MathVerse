from langgraph.graph import StateGraph, END
from app.rags.state import PipelineState
from app.rags.rag1_solver import solve_math
from app.rags.rag2_formatter import format_json
from app.rags.rag3_coder import generate_code
from app.rags.rag4_reviewer import review_code

def build_graph():
    # Initialize the graph
    workflow = StateGraph(PipelineState)
    
    # Add nodes
    workflow.add_node("solver", solve_math)
    workflow.add_node("formatter", format_json)
    workflow.add_node("coder", generate_code)
    workflow.add_node("reviewer", review_code)
    
    # Define edges (Sequential Flow)
    workflow.set_entry_point("solver")
    workflow.add_edge("solver", "formatter")
    workflow.add_edge("formatter", "coder")
    workflow.add_edge("coder", "reviewer")
    workflow.add_edge("reviewer", END)
    
    # Compile the graph
    return workflow.compile()
