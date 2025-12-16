from datetime import datetime
from typing import List
from bson import ObjectId

from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.task.internal.store.task_repository import TaskRepository 
from modules.application.errors import AppError

class CommentService:
    @classmethod
    def create_comment(cls, task_id: str, account_id: str, content: str) -> CommentModel:
        # Check: Does Task exist? (Data Integrity)
        task = TaskRepository.find_one({"_id": ObjectId(task_id)})
        if not task:
            # --- FIX: Changed 'http_code' to 'http_status_code' ---
            raise AppError(message="Task not found", code="TASK_NOT_FOUND", http_status_code=404)

        comment = CommentModel(
            task_id=task_id,
            account_id=account_id,
            content=content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return CommentRepository.create(comment)

    @classmethod
    def get_comments_for_task(cls, task_id: str) -> List[CommentModel]:
        return CommentRepository.find({"task_id": task_id, "active": True})

    @classmethod
    def update_comment(cls, comment_id: str, content: str) -> CommentModel:
        comment = CommentRepository.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            # --- FIX: Changed 'http_code' to 'http_status_code' ---
            raise AppError(message="Comment not found", code="COMMENT_NOT_FOUND", http_status_code=404)
        
        comment.content = content
        comment.updated_at = datetime.utcnow()
        return CommentRepository.update(comment)

    @classmethod
    def delete_comment(cls, comment_id: str):
        # Standard Practice: Soft Delete. Never lose user data.
        comment = CommentRepository.find_one({"_id": ObjectId(comment_id)})
        if comment:
            comment.active = False
            comment.updated_at = datetime.utcnow()
            CommentRepository.update(comment)