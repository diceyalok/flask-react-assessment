from flask import request, jsonify
from flask.views import MethodView
from modules.comment.comment_service import CommentService

class CommentView(MethodView):
    def post(self, task_id):
        data = request.get_json()
        return jsonify(CommentService.create_comment(
            task_id=task_id,
            account_id=data.get('account_id'),
            content=data.get('content')
        ).to_dict()), 201

    def get(self, task_id):
        comments = CommentService.get_comments_for_task(task_id)
        return jsonify([c.to_dict() for c in comments]), 200

    def patch(self, comment_id):
        data = request.get_json()
        comment = CommentService.update_comment(comment_id, data.get('content'))
        return jsonify(comment.to_dict()), 200
        
    def delete(self, comment_id):
        CommentService.delete_comment(comment_id)
        return jsonify({"message": "Deleted"}), 200