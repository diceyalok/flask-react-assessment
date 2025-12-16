import pytest
from unittest.mock import MagicMock, patch
from modules.comment.comment_service import CommentService
from modules.application.errors import AppError

# --- MOCK DATA ---
FAKE_TASK_ID = "693f99e5ca59562f35431332"
FAKE_ACCOUNT_ID = "user123"

@pytest.fixture
def mock_repo():
    """Mock the Repositories so we don't need a real DB"""
    with patch("modules.comment.comment_service.CommentRepository") as mock:
        yield mock

@pytest.fixture
def mock_task_repo():
    with patch("modules.comment.comment_service.TaskRepository") as mock:
        yield mock

def test_create_comment(mock_repo, mock_task_repo):
    # 1. Simulate Task Exists
    mock_task_repo.find_one.return_value = {"_id": FAKE_TASK_ID}
    # 2. Simulate Create
    mock_repo.create.return_value = MagicMock(content="Nice work!")
    
    # 3. Call Service
    result = CommentService.create_comment(FAKE_TASK_ID, FAKE_ACCOUNT_ID, "Nice work!")
    
    assert result.content == "Nice work!"

def test_create_comment_no_task(mock_repo, mock_task_repo):
    # 1. Simulate Task Does NOT Exist
    mock_task_repo.find_one.return_value = None
    
    # 2. Expect Error 404
    with pytest.raises(AppError) as e:
        CommentService.create_comment(FAKE_TASK_ID, FAKE_ACCOUNT_ID, "Fail")
    
    assert e.value.http_code == 404