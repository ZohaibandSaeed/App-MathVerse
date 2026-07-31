from fastapi import APIRouter, HTTPException
from app.schemas.models import MathRequest, MathResponse, PlaygroundRequest, PlaygroundResponse
from app.rags.graph import build_graph
from app.utils.code_runner import execute_mathly_code
import uuid
import os

router = APIRouter()
# We compile the graph once when the app starts
graph = build_graph()

@router.post("/solve", response_model=MathResponse)
async def solve_math_problem(request: MathRequest):
    """
    Receives a math problem, runs it through the 4-stage LangGraph RAG,
    executes the resulting Mathly code, and returns the image in base64.
    """
    initial_state = {
        "question": request.problem,
        "solution_text": "",
        "solution_json": "",
        "generated_code": "",
        "final_code": ""
    }
    
    try:
        # Run the Multi-Agent Pipeline
        result = graph.invoke(initial_state)
        final_code = result["final_code"]
        solution_text = result["solution_text"]
        
        # Prepare output path for the image
        image_filename = f"output_{uuid.uuid4().hex}.png"
        output_path = os.path.join(os.path.dirname(__file__), "../../../../", image_filename)
        output_path = os.path.abspath(output_path)
        
        # Execute the python code securely and get base64
        image_base64 = execute_mathly_code(final_code, output_path)
        
        # Optionally, clean up the image file after getting base64
        if os.path.exists(output_path):
            os.remove(output_path)
            
        return MathResponse(image_base64=image_base64, solution_text=solution_text)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-playground", response_model=PlaygroundResponse)
async def run_playground(request: PlaygroundRequest):
    """
    Executes raw Mathly code from the playground and returns the rendered Base64 image.
    """
    try:
        image_filename = f"playground_{uuid.uuid4().hex}.png"
        output_path = os.path.join(os.path.dirname(__file__), "../../../../", image_filename)
        output_path = os.path.abspath(output_path)
        
        # We explicitly replace any instance of 'output.png' or similar with our output_path 
        # so it saves to the right place and we can read it.
        # But `execute_mathly_code` expects `final_code` and `output_path`.
        
        # Execute the python code securely and get base64
        image_base64 = execute_mathly_code(request.code, output_path)
        
        if os.path.exists(output_path):
            os.remove(output_path)
            
        return PlaygroundResponse(image_base64=image_base64)
        
    except Exception as e:
        # We return 400 Bad Request for syntax/runtime errors so the playground can show them nicely.
        raise HTTPException(status_code=400, detail=str(e))
