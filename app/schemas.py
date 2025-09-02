from pydantic import BaseModel, Field

class VacancyRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)

    model_config = { 
        "json_schema_extra": {
            "example": {
                "title": "Some Position",
                "description": "Description of the new position",
                "completed": False
            }
        }
    }

