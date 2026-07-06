from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RadarEvent:
    event_type: str
    title: str
    summary: str
    city: str = "Malaysia"
    source: str = ""
    url: str = ""
    priority: int = 1
    company: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None

    def is_critical(self) -> bool:
        return self.priority >= 5

    def is_important(self) -> bool:
        return self.priority >= 4
