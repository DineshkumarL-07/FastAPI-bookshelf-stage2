# from motor.motor_asyncio import AsyncIOMotorDatabase

# class BaseService:
#     def __init__(self, db: AsyncIOMotorDatabase):
#         self.db = db

#     def _replace_id(self, doc):
#         doc['id'] = str(doc.pop('_id', None))
#         return doc

#     def _to_response(self, doc, class_name):
#         doc = self._replace_id(doc)
#         return class_name(**doc)
