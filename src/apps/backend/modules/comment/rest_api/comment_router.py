from flask import Flask
from modules.comment.rest_api.comment_view import CommentView, SingleCommentView

class CommentRouter:
    @staticmethod
    def register(app: Flask):
        # 1. List/Create Comments for a Task
        # URL: /api/tasks/<task_id>/comments
        comment_view = CommentView.as_view("comment_view")
        app.add_url_rule(
            "/api/tasks/<task_id>/comments",
            view_func=comment_view,
            methods=["GET", "POST"]
        )

        # 2. Edit/Delete Specific Comment
        # URL: /api/comments/<comment_id>
        single_comment_view = SingleCommentView.as_view("single_comment_view")
        app.add_url_rule(
            "/api/comments/<comment_id>",
            view_func=single_comment_view,
            methods=["PATCH", "DELETE"]
        )