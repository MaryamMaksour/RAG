  project
  
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


data_chunk
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


    projectModel

      async def init_collection(self): # create the indexing
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
                    self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECCT_NAME.value]
                    indexes = Project.get_indexes()
                    for index in indexes:
                        await self.collection.create_index(
                            index["key"],
                            name = index["name"],
                            unique = index["unique"]
                        )
