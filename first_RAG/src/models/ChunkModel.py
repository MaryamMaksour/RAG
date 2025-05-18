from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne # insert data py batch
from .db_schemes.data_chunk import DataChunk


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def creat_instance(cls, db_client: object):
        instance = cls(db_client) # call __init__
        await instance.init_collection()

        return instance
        
    async def init_collection(self): # create the indexing
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
                    self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
                    indexes = DataChunk.get_indexes()
                    for index in indexes:
                        await self.collection.create_index(
                            index["key"],
                            name = index["name"],
                            unique = index["unique"]
                        )

    # insert chunk
    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_onr(chunk.dict(by_alias = True, exclude_unset=True ))
        chunk._id = result.inserted_id
        return chunk

    
    # get chunk from id
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one(
            {
                "_id": ObjectId(chunk_id)
            }
        )

        if result is None:
            return  None
        
        return DataChunk(**result) # result is dict **result convert dict to parameters


    async def insert_many_chunk(self, chunk: list, batch_size: int = 100):

        for i in range(0, len(chunk), batch_size):
            batch = chunk[i:i+batch_size]

            operations=[
                InsertOne(chunk.dict(by_alias = True, exclude_unset=True ))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunk)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):

        result = await self.collection.delete_many(
            {
                "chunk_project_id": project_id
            }
        )

        return result.deleted_count