'''
 FOR FILES
 
''' 

from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime


class Asset(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId 
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1) # file_id
    asset_size : int = Field (ge=0, default=None)
    asset_config: dict = Field (default=None)
    asste_pushed_at: datetime = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True # Do not know what is objectid is So ignore 
    
    
    @classmethod
    def get_indexes(cls): # we put cls insted self because it is static method
        return [
            {
                "key":[ #    1 for Ascending order, 
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False 

            },
            {
                "key":[ 
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True 

            }
        ]
