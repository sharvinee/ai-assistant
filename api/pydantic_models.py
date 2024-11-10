from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# define enumeration for model names
class ModelName(str, Enum):
    GPT4_O = "gpt-4o"
    GPT4_O_MINI = "gpt-4o-mini"

# defines data model for handling input queries
class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_O_MINI)


# defines data model for structuring API responses
class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

# defines data model for storing information about uploaded documents
class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

# defines data model for handling requests to delete a document
class DeleteFileRequest(BaseModel):
    file_id: int