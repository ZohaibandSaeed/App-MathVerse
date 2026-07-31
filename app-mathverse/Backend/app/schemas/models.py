from pydantic import BaseModel

class MathRequest(BaseModel):
    problem: str
    
class MathResponse(BaseModel):
    image_base64: str
    solution_text: str

class PlaygroundRequest(BaseModel):
    code: str

class PlaygroundResponse(BaseModel):
    image_base64: str
