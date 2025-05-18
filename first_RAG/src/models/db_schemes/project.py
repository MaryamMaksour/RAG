from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):# we put cls insted self because it is static method
        if not value.isalnum():
            raise ValueError('Project_id must be alphanumaric')

        return value 

    class Config:
        arbitrary_types_allowed = True # Do not know what is objectid is So ignore 
    
    
    @classmethod
    def get_indexes(cls): # we put cls insted self because it is static method
        return [
            {
                "key":[ #    1 for Ascending order, 
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True 

            }
        ]