from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECCT_NAME.value]
    
    @classmethod
    async def creat_instance(cls, db_client: object):
        instance = cls(db_client) # call __init__
        await instance.init_collection()

        return instance



    async def init_collection(self): # create the indexing
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECCT_NAME.value not in all_collections:
                    self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECCT_NAME.value]
                    indexes = Project.get_indexes()
                    for index in indexes:
                        await self.collection.create_index(
                            index["key"],
                            name = index["name"],
                            unique = index["unique"]
                        )


    async def create_project(self, project : Project):

        result = await self.collection.insert_one(project.dict(by_alias = True, exclude_unset=True ))# from motor need dict
        project._id = result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one( #from motor need dict
            {
                "project_id": project_id
            }
        ) # type = dict

        if record is None:
            # create one
            project = Project(project_id=project_id)
            project = await self.create_project(project = project)

            return project # type = project
        
        return Project(**record) # type = project

    async def get_all_projects(self, page: int=1, page_size: int=10):
        # if we have so many project --> alot of peoblem 
        # So we use pagination --> make the result on pages

        # count total number of documents
        total_documents = await self.collection.count_documents({})

        total_pages = (total_pages + page_size -1) // page_size

        # colecte data skip for pages 1, 2,....
        cursor = self.collection.find().skip( (page - 1)*page_size  ).limit(page_size)

        projects = []
        # use async with motor
        async for document in cursor:
            projects.append(
                project(**document)
            )

        return projects, total_pages



            

