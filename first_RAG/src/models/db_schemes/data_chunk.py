from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    
    chunk_txt: str = Field(..., min_length=1)
    chunk_metadata: dict
    
    chunk_order: int = Field(..., gt=0)# gt=0 mean chunk_order > 0 

    chunk_project_id: ObjectId

    chunk_asset_id: ObjectId

 
    class Config:
        arbitrary_types_allowed = True # Do not know what is objectid is SO ignore 
    
    @classmethod
    def get_indexes(cls): # we put cls insted self because it is static method
        return [
            {
                "key":[ #    1 for Ascending order, 
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "unique": False  

            }
        ]