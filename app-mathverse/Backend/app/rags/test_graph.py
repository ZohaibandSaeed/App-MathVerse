import os
from app.rags.graph import build_graph
from dotenv import load_dotenv

# Load environment variables (Make sure to set GOOGLE_API_KEY and GROQ_API_KEY in .env)
load_dotenv()

def run_test():
    graph = build_graph()
    
    initial_state = {
        "question": "Solve the inequality 2x - 4 > 0 and graph it on a number line.",
        "solution_text": "",
        "solution_json": "",
        "generated_code": "",
        "final_code": ""
    }
    
    print("Starting Multi-Agent RAG Pipeline...")
    # Invoke the graph
    result = graph.invoke(initial_state)
    
    print("\\n=== 1. MATH SOLVER OUTPUT ===")
    print(result["solution_text"])
    
    print("\\n=== 2. JSON FORMATTER OUTPUT ===")
    print(result["solution_json"])
    
    print("\\n=== 3. CODER OUTPUT ===")
    print(result["generated_code"])
    
    print("\\n=== 4. REVIEWER OUTPUT ===")
    print(result["final_code"])

if __name__ == "__main__":
    # Ensure this runs correctly from the backend root
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    run_test()
