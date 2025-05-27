from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, auth, schemas

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user

async def create_book(db: AsyncSession, book: schemas.BookCreate, user_id: int):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year,
        user_id=user_id
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10, user_id: int | None = None):
    if user_id is not None:
        result = await db.execute(select(models.Book).where(models.Book.user_id == user_id).offset(skip).limit(limit))
        return result.scalars().all()
    return False

async def update_book(db: AsyncSession, db_book: models.Book, book: schemas.BookUpdate): # out of order
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, db_book: models.Book):
    await db.delete(db_book)
    await db.commit()