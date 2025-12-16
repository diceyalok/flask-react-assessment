from dataclasses import asdict
from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.comment_service import CommentService
from modules.application.errors import AppError

class CommentView(MethodView):
    @access_auth_middleware
    def post(self, task_id: str) -> ResponseReturnValue:
        # Get Current User ID from the middleware
        account_id = getattr(request, "account_id")
        data = request.get_json()

        if not data or not data.get("content"):
            return jsonify({"error": "Content is required"}), 400

        try:
            comment = CommentService.create_comment(
                task_id=task_id,
                account_id=account_id,
                content=data["content"]
            )
            return jsonify(asdict(comment)), 201
        except AppError as e:
            return jsonify({"error": e.message}), e.http_code

    @access_auth_middleware
    def get(self, task_id: str) -> ResponseReturnValue:
        comments = CommentService.get_comments_for_task(task_id)
        return jsonify([asdict(c) for c in comments]), 200


class SingleCommentView(MethodView):
    @access_auth_middleware
    def patch(self, comment_id: str) -> ResponseReturnValue:
        data = request.get_json()
        if not data or not data.get("content"):
             return jsonify({"error": "Content is required"}), 400
             
        try:
            comment = CommentService.update_comment(comment_id, data["content"])
            return jsonify(asdict(comment)), 200
        except AppError as e:
            return jsonify({"error": e.message}), e.http_code

    @access_auth_middleware
    def delete(self, comment_id: str) -> ResponseReturnValue:
        CommentService.delete_comment(comment_id)
        return "", 204