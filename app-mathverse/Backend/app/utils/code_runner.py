import base64
import traceback
import re
import os

def execute_mathly_code(python_code: str, output_filepath: str) -> str:
    """
    Executes the generated Python code and returns the base64 string of the generated image.
    """
    # Replace board.render(...) calls with our own output_filepath
    python_code = re.sub(r'board\.render\(.*?\)', f'board.render(r"{output_filepath}")', python_code)
    
    # We must ensure mathly is available in the environment.
    # Since we installed it via pip, it will be globally available to exec.
    local_env = {}
    try:
        exec(python_code, {}, local_env)
    except Exception as e:
        error_msg = f"Error executing code:\n{traceback.format_exc()}"
        print(error_msg)
        raise ValueError("Failed to execute generated Mathly code. There might be a syntax error.")
        
    # Read the generated image and convert to base64
    try:
        with open(output_filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        raise ValueError("The AI code executed, but no image was generated.")
