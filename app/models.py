from pydantic import BaseModel

# Define request model
class QuestionRequest(BaseModel):
    question: str

# DEfine the response model
class QuestionResponse(BaseModel):
    question: str
    answer: str