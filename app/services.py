from typing import Optional, List, Dict, Any
from app.models import Task
from app.repository import TaskRepository, get_repository

class TaskService:
    def __init__(self, repository: Optional[TaskRepository] = None):
        self._repository = repository

    @property
    def repository(self) -> TaskRepository:
        if self._repository is None:
            self._repository = get_repository()
        return self._repository

    def init_db(self) -> None:
        self.repository.init_db()

    def list_tasks(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        tasks = self.repository.get_all(done=done, search=search)
        return [task.to_dict() for task in tasks]

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        task = self.repository.get_by_id(task_id)
        return task.to_dict() if task else None

    def create_task(self, title: str) -> Dict[str, Any]:
        task = self.repository.create(title)
        return task.to_dict()

    def update_task(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        task = self.repository.update(task_id, title=title, done=done)
        return task.to_dict() if task else None

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)

    def get_stats(self) -> Dict[str, int]:
        return self.repository.get_stats()

    def reset_tasks(self) -> None:
        self.repository.reset()
