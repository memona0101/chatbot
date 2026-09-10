from pydantic import BaseModel, Field


class CreateSessionResponse(BaseModel):
    session_token: str
    lead_state: str


class LeadCaptureRequest(BaseModel):
    session_token: str
    field: str
    value: str = Field(min_length=1)


class LeadCaptureResponse(BaseModel):
    success: bool
    message: str
    lead_state: str

class ChatRequest(BaseModel):
    session_token: str
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_token: str
    message: str
    lead_state: str    