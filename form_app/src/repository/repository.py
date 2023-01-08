from typing import Union, List

from pymongo.collection import Collection


def insert_documents(documents: Union[dict, List[dict]], collection: Collection):
    if isinstance(documents, dict):
        collection.insert_one(documents)
    elif isinstance(documents, list):
        collection.insert_many(documents)
