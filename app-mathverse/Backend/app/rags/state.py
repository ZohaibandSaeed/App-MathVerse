from typing import TypedDict

class PipelineState(TypedDict):
    question: str
    solution_text: str
    solution_json: str
    generated_code: str
    final_code: str
