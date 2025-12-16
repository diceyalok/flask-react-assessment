import json
from unittest.mock import patch, MagicMock
from flask import Flask
from modules.comment.rest_api.comment_rest_api_server import CommentRestApiServer

# 1. Setup a Test Client
def create_test_app():
    app = Flask(__name__)
    # Register our new blueprint
    app.register_blueprint(CommentRestApiServer.create())
    return app.test_client()

# 2. The Test Case
@patch("modules.comment.comment_service.TaskRepository") # Mock the Task check
@patch("modules.comment.comment_service.CommentRepository") # Mock the Comment save
def test_create_and_get_comment(mock_comment_repo, mock_task_repo):
    client = create_test_app()

    # A. Setup Mock Data
    fake_task_id = "507f1f77bcf86cd799439011"
    fake_account_id = "user123"
    
    # When the service checks if task exists, say "Yes"
    mock_task_repo.find_one.return_value = {"_id": fake_task_id, "title": "Test Task"}
    
    # When the service saves a comment, return a fake saved object
    mock_comment_model = MagicMock()
    mock_comment_model.to_dict.return_value = {
        "content": "This is a test comment",
        "task_id": fake_task_id,
        "account_id": fake_account_id
    }
    mock_comment_repo.create.return_value = mock_comment_model

    # B. TEST: Create Comment (POST)
    response = client.post(f"/tasks/{fake_task_id}/comments", json={
        "account_id": fake_account_id,
        "content": "This is a test comment"
    })

    # C. Verify Results
    assert response.status_code == 201
    assert response.json["content"] == "This is a test comment"
    print("\n✅ Test Passed: Comment Created Successfully!")

if __name__ == "__main__":
    # Run the test manually
    test_create_and_get_comment()