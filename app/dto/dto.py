from pydantic import BaseModel

class add_task(BaseModel):
    title: str
    description: str
    status: str
    priority: str