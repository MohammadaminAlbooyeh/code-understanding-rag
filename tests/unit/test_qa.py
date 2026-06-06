import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_db_session():
    """Mock the database session to avoid needing a real database."""
    with patch("backend.services.qa_service.SessionLocal") as mock_session:
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        yield mock_session_instance


def test_qa_service_ask_no_code(mock_db_session):
    from backend.services.qa_service import QAService
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    qa = QAService()
    with pytest.raises(Exception):
        qa.ask("nonexistent-id", "What does this code do?")


def test_qa_service_ask_with_code(mock_db_session):
    from backend.services.qa_service import QAService

    mock_code = MagicMock()
    mock_code.id = "code-123"
    mock_code.content = "def hello():\n    return 'Hello'"
    mock_code.filename = "hello.py"
    mock_code.language = "python"
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_code

    qa = QAService()
    with patch.object(qa, "_get_rag_chain", return_value=None):
        result = qa.ask("code-123", "What does this function do?")
    assert result["question"] == "What does this function do?"
    assert result["code_id"] == "code-123"
    assert "hello.py" in result["answer"]


def test_qa_service_get_history_empty(mock_db_session):
    from backend.services.qa_service import QAService
    mock_db_session.query.return_value.order_by.return_value.all.return_value = []

    qa = QAService()
    history = qa.get_history()
    assert history == []


def test_qa_service_clear_history(mock_db_session):
    from backend.services.qa_service import QAService

    qa = QAService()
    qa.clear_history()
    mock_db_session.query.return_value.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_qa_service_batch_ask(mock_db_session):
    from backend.services.qa_service import QAService

    mock_code = MagicMock()
    mock_code.id = "code-123"
    mock_code.content = "x = 1"
    mock_code.filename = "test.py"
    mock_code.language = "python"
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_code

    qa = QAService()
    with patch.object(qa, "_get_rag_chain", return_value=None):
        results = qa.batch_ask([
            {"code_id": "code-123", "question": "Q1"},
            {"code_id": "code-123", "question": "Q2"},
        ])
    assert len(results) == 2
    assert results[0]["question"] == "Q1"
    assert results[1]["question"] == "Q2"
