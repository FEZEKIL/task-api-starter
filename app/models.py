from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Task:
    id: Optional[int]
    title: str
    done: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            done=bool(data.get("done", False))
        )
