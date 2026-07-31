import os

def get_system_prompt() -> str:
    """
    Reads the MATHLY_PROMPT.md cheat sheet to inject into Gemini.
    """
    # Assuming MATHLY_PROMPT.md is in the project root
    prompt_path = os.path.join(os.path.dirname(__file__), "MATHLY_PROMPT.md")
    try:
        with open(prompt_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are an expert Mathly AI Code Generator. Your task is to write code that saves an image to output_path using board.save(output_path)."
