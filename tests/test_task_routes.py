from datetime import datetime, UTC
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.services.task_service import TaskService


client = TestClient(app)


def fake_task():
    now = datetime.now(UTC)

    return {
        "id": str(uuid4()),
        "title": "Estudar FastAPI",
        "description": "Criar testes automatizados",
        "status": "Pendente",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "deleted_at": None,
    }


def test_create_task(monkeypatch):
    def mock_create(self, payload):
        task = fake_task()
        task["title"] = payload.title
        task["description"] = payload.description
        return task

    monkeypatch.setattr(TaskService, "create", mock_create)

    response = client.post(
        "/tasks",
        json={
            "title": "Estudar FastAPI",
            "description": "Criar testes"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Estudar FastAPI"
    assert response.json()["status"] == "Pendente"


def test_list_tasks(monkeypatch):
    def mock_list_all(self, title=None, status_filter=None):
        return [fake_task()]

    monkeypatch.setattr(TaskService, "list_all", mock_list_all)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task_by_id(monkeypatch):
    task_id = uuid4()

    def mock_get_by_id(self, task_id):
        task = fake_task()
        task["id"] = str(task_id)
        return task

    monkeypatch.setattr(TaskService, "get_by_id", mock_get_by_id)

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(task_id)


def test_update_task(monkeypatch):
    task_id = uuid4()

    def mock_update(self, task_id, payload):
        task = fake_task()
        task["id"] = str(task_id)
        task["title"] = payload.title
        task["status"] = payload.status
        return task

    monkeypatch.setattr(TaskService, "update", mock_update)

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Tarefa atualizada",
            "status": "Concluída"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa atualizada"
    assert response.json()["status"] == "Concluída"


def test_delete_task(monkeypatch):
    task_id = uuid4()

    def mock_soft_delete(self, task_id):
        return None

    monkeypatch.setattr(TaskService, "soft_delete", mock_soft_delete)

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204