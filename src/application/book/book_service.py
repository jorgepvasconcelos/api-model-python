from typing import Union

from src.application.book.book_error import BookError
from src.domain.book import Book
from src.infrastructure.repository.books_repository import BooksRepository
from src.infrastructure.errors.sql_error import SQLError
from src.presentation.schemas.book_schema import POSTBookInput


class BookService:
    @staticmethod
    def find_book_by_id(book_id: int) -> Book:
        return BooksRepository.find_book_by_id(book_id=book_id)

    @staticmethod
    def insert_book(data: POSTBookInput) -> tuple[Union[Book, None], Union[BookError, None]]:
        new_book = Book(**data.dict())

        result, error = BooksRepository.insert_book(book=new_book)
        if error:
            if error == SQLError.duplicate_entry:
                return None, BookError.duplicate_entry

        return Book(**result), None
