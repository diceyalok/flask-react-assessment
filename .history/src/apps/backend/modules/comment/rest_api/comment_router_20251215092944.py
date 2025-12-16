from flask import Blueprint
from modules.comment.rest_api.comment_view import CommentView

class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        # URL for Task-Specific actions (Create, List)
        blueprint.add_url_rule(
            "/tasks/<task_id>/comments",
            view_func=CommentView.as_view("comment_create_list"),
            methods=["POST", "GET"]
        )
        # URL for Comment-Specific actions (Edit, Delete)
        blueprint.add_url_rule(
            "/comments/<comment_id>",
            view_func=CommentView.as_view("comment_edit_delete"),
            methods=["PATCH", "DELETE"]
        )
        return blueprint