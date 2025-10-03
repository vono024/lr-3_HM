from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from .config import DASHBOARD_TITLE, MAX_ITEMS
from .models import DashboardItem, DashboardItemOut
from .utils import normalize_title, slugify

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_items: list[DashboardItemOut] = []
_next_id: int = 1

def _gen_id() -> int:
    global _next_id
    i = _next_id
    _next_id += 1
    return i

@router.get("/", summary="Статус модуля dashboard")
def dashboard_index():
    return {"dashboard": DASHBOARD_TITLE, "count": len(_items), "limit": MAX_ITEMS}

@router.get("/items", response_model=List[DashboardItemOut], summary="Отримати список елементів")
def list_items(
    q: Optional[str] = Query(default=None, description="Пошук по title/note"),
    limit: int = Query(default=50, ge=1, le=200, description="Ліміт"),
    offset: int = Query(default=0, ge=0, description="Зсув"),
):
    data = _items
    if q:
        ql = q.lower()
        data = [it for it in data if ql in it.title.lower() or (it.note and ql in it.note.lower())]
    return data[offset : offset + limit]

@router.get("/items/{item_id}", response_model=DashboardItemOut, summary="Отримати елемент за id")
def get_item(item_id: int):
    for it in _items:
        if it.id == item_id:
            return it
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=DashboardItemOut, summary="Створити елемент")
def create_item(payload: DashboardItem):
    if len(_items) >= MAX_ITEMS:
        raise HTTPException(status_code=409, detail="Storage limit reached")
    normalized = payload.model_copy()
    normalized.title = normalize_title(normalized.title)
    new = DashboardItemOut(
        id=_gen_id(),
        title=normalized.title,
        value=normalized.value,
        note=normalized.note,
    )
    _items.append(new)
    return new

@router.put("/items/{item_id}", response_model=DashboardItemOut, summary="Оновити елемент")
def update_item(item_id: int, payload: DashboardItem):
    for idx, it in enumerate(_items):
        if it.id == item_id:
            updated = DashboardItemOut(
                id=it.id,
                title=normalize_title(payload.title),
                value=payload.value,
                note=payload.note,
            )
            _items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}", status_code=204, summary="Видалити елемент")
def delete_item(item_id: int):
    global _items
    before = len(_items)
    _items = [it for it in _items if it.id != item_id]
    if len(_items) == before:
        raise HTTPException(status_code=404, detail="Item not found")
    return None

@router.get("/items/{item_id}/slug", summary="Отримати slug для title")
def item_slug(item_id: int):
    for it in _items:
        if it.id == item_id:
            return {"id": it.id, "slug": slugify(it.title)}
    raise HTTPException(status_code=404, detail="Item not found")
