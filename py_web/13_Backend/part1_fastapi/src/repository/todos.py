import sys
from os.path import abspath, dirname, join

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, abspath(join(dirname(__file__), "..")))

from src.entity.models import Todo
from src.schemas.todo import TodoSchema, TodoUpdate


async def get_todos(limit: int, offset: int, db: AsyncSession):
    stmt = select(Todo).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession):
    stmt = select(Todo).filter_by(id=todo_id)
    todos = await db.execute(stmt)
    return todos.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession):
    todo = Todo(**body.model_dump(exclude_unset=True))
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: TodoUpdate, db: AsyncSession):
    stmt = select(Todo).filter_by(id=todo_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.description = body.description
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def delete_todo(todo_id: int, db: AsyncSession):
    stmt = select(Todo).filter_by(id=todo_id)
    todo = await db.execute(stmt)
    todo = todo.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo
