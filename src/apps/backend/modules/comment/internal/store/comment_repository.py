from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from modules.application.repository import ApplicationRepository
from modules.comment.internal.store.comment_model import CommentModel
from modules.logger.logger import Logger

# Standard Practice: Enforce schema at the DB level
COMMENT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["task_id", "account_id", "content", "active"],
        "properties": {
            "task_id": {"bsonType": "string"},
            "account_id": {"bsonType": "string"},
            "content": {"bsonType": "string"},
            "active": {"bsonType": "bool"},
        },
    }
}

class CommentRepository(ApplicationRepository):
    collection_name = CommentModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        # Standard Practice: Always index foreign keys (task_id)
        collection.create_index(
            [("task_id", 1), ("active", 1)], 
            name="task_active_index"
        )
        
        # Apply Validation logic
        try:
            collection.database.command({
                "collMod": cls.collection_name,
                "validator": COMMENT_VALIDATION_SCHEMA,
                "validationLevel": "strict"
            })
        except OperationFailure:
            pass # Collection likely doesn't exist yet, which is fine
        return True