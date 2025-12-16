import sys
import os
import json
from unittest.mock import patch, MagicMock

# FORCE PYTHON TO FIND THE MODULES
# This adds the current directory to Python's search path
sys.path.append(os.getcwd())

from flask import Flask
from modules.comment.rest_api.comment_rest_api_server import CommentRestApiServer

def create_test_app():
    app = Flask(__name__)
    app.register_blueprint(CommentRestApiServer.create())
    return app.test_client()

@patch("modules.comment.comment_service.TaskRepository")
@patch("modules.comment.comment_service.CommentRepository")
def test_create_and_get_comment(mock_comment_repo, mock_task_repo):
    client = create_test_app()

    # 1. SETUP MOCK DATA
    fake_task_id = "507f1f77bcf86cd799439011"
    fake_account_id = "user123"
    
    mock_task_repo.find_one.return_value = {"_id": fake_task_id, "title": "Test Task"}
    
    mock_comment_model = MagicMock()
    mock_comment_model.to_dict.return_value = {
        "content": "This is a test comment",
        "task_id": fake_task_id,
        "account_id": fake_account_id
    }
    mock_comment_repo.create.return_value = mock_comment_model

    # 2. RUN TEST
    print("\n🚀 Sending POST request...")
    response = client.post(f"/tasks/{fake_task_id}/comments", json={
        "account_id": fake_account_id,
        "content": "This is a test comment"
    })

    # 3. VERIFY
    if response.status_code == 201:
        print("✅ Success! Status Code 201 Created")
    else:
        print(f"❌ Failed. Status Code: {response.status_code}")
        print(response.json)
    
    assert response.status_code == 201
    assert response.json["content"] == "This is a test comment"
    print("✅ Test Passed: Comment Created Successfully!")

if __name__ == "__main__":
    test_create_and_get_comment()