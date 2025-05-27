from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas, crud, auth, database

router = APIRouter()

@router.post('/books', response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return await crud.create_book(db, book, user_id=current_user.id)

@router.get('/books', response_model=list[schemas.Book])
async def get_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    books = await crud.get_books(db, skip=skip, limit=limit, user_id=current_user.id)
    if not books:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")
    return books

@router.put('/books/{book_id}', response_model=schemas.Book)
async def update_book(book: schemas.BookUpdate, book_id: int, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_book = await db.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this book")
    updated_book = await crud.update_book(db, db_book=db_book, book=book)
    return updated_book

@router.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_book = await db.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this book")
    await crud.delete_book(db, db_book=db_book)
    return None