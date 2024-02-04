import sys
from os.path import abspath, dirname, join

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, abspath(join(dirname(__file__), "..")))

from src.database.connect import get_db
from src.entity.models import User
from src.repository import todos as repositories_todos
from src.schemas.todo import TodoResponse, TodoSchema, TodoUpdate
from src.services.auth import auth_service

router_todo = APIRouter(prefix="/todos", tags=["todos"])


@router_todo.get("/", response_model=list[TodoResponse])
async def get_todos(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    todos = await repositories_todos.get_todos(limit, offset, db)
    return todos


@router_todo.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    todo = await repositories_todos.get_todo(todo_id, db)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return todo


@router_todo.post(
    "/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_201_CREATED
)
async def create_todo(
    body: TodoSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    todo = await repositories_todos.create_todo(body, db)
    return todo


@router_todo.put("/{todo_id}")
async def update_todo(
    body: TodoUpdate,
    todo_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    todo = await repositories_todos.update_todo(todo_id, body, db)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return todo


@router_todo.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    todo = await repositories_todos.delete_todo(todo_id, db)
    return todo
