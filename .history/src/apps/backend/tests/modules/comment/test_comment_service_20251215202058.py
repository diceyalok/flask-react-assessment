import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Import the service you wrote
from modules.comment.comment_service import CommentService
# Import the error class
from modules.application.errors import AppError

# --- MOCK DATA ---
FAKE_TASK_ID = "693f99e5ca59562f35431332"
FAKE_ACCOUNT_ID = "693f99e5ca59562f35431333"
FAKE_COMMENT_ID = "507f1f77bcf86cd799439011"

@pytest.fixture
def mock_repositories():
    """Mock the Task and Comment Repositories so we don't need a real DB"""
    with patch("modules.comment.comment_service.TaskRepository") as mock_task_repo, \
         patch("modules.comment.comment_service.CommentRepository") as mock_comment_repo:
        yield mock_task_repo, mock_comment_repo

def test_create_comment_success(mock_repositories):
    mock_task_repo, mock_comment_repo = mock_repositories
    
    # 1. Simulate finding a valid task
    mock_task_repo.find_one.return_value = {"_id": FAKE_TASK_ID}
    
    # 2. Simulate creating the comment
    mock_comment_repo.create.return_value = MagicMock(
        _id=FAKE_COMMENT_ID, 
        content="Test Comment", 
        task_id=FAKE_TASK_ID
    )

    # 3. Call the Service
    result = CommentService.create_comment(FAKE_TASK_ID, FAKE_ACCOUNT_ID, "Test Comment")

    # 4. Verify the result
    assert result.content == "Test Comment"
    assert result.task_id == FAKE_TASK_ID
    # Ensure repositories were called correctly
    mock_task_repo.find_one.assert_called_once()
    mock_comment_repo.create.assert_called_once()

def test_create_comment_task_not_found(mock_repositories):
    mock_task_repo, _ = mock_repositories
    
    # 1. Simulate Task NOT found (return None)
    mock_task_repo.find_one.return_value = None

    # 2. Verify that it raises an AppError (404)
    with pytest.raises(AppError) as excinfo:
        CommentService.create_comment(FAKE_TASK_ID, FAKE_ACCOUNT_ID, "Test Comment")
    
    assert excinfo.value.http_code == 404
    assert "Task not found" in excinfo.value.message

def test_get_comments(mock_repositories):
    _, mock_comment_repo = mock_repositories
    
    # 1. Mock DB returning a list of comments
    mock_comment_repo.find.return_value = [
        MagicMock(content="First"), 
        MagicMock(content="Second")
    ]

    # 2. Call Service
    comments = CommentService.get_comments_for_task(FAKE_TASK_ID)

    # 3. Verify
    assert len(comments) == 2
    assert comments[0].content == "First"

def test_delete_comment(mock_repositories):
    _, mock_comment_repo = mock_repositories
    
    # 1. Mock finding the comment
    mock_comment = MagicMock(active=True)
    mock_comment_repo.find_one.return_value = mock_comment

    # 2. Call Delete
    CommentService.delete_comment(FAKE_COMMENT_ID)

    # 3. Verify Soft Delete (active set to False)
    assert mock_comment.active is False
    mock_comment_repo.update.assert_called_once()