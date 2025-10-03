from typing import Optional
from pydantic import BaseModel, Field

class DashboardItem(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Заголовок запису")
    value: int = Field(ge=0, le=10_000_000, description="Числове значення")
    note: Optional[str] = Field(default=None, max_length=1000, description="Опціональна примітка")

class DashboardItemOut(DashboardItem):
    id: int