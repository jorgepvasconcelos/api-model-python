from src.data.db_orm.query_obj import delete_obj, insert_obj, select_first_obj, update_obj
from src.data.db_orm.tables.tbl_books import TblBooks
from src.data.dtos.books_dto import BookDTO
from src.data.errors.repository_error import RepositoryError
from src.data.errors.sql_error import SQLError
from src.data.redis.cache_expiration import CacheExpiration
from src.data.redis.decorators import delete_cached_value, get_cached_value_2_returns
from src.domain.book import BookDomain


class BooksRepository:
    @staticmethod
    @get_cached_value_2_returns(key="book-id-{book_id}", expiration=CacheExpiration.ONE_HOUR)
    def find_book_by_id(book_id: int) -> tuple[BookDTO | None, SQLError | None]:
        query_result = select_first_obj(obj_table=TblBooks, where_clauses=[TblBooks.id == book_id])
        if query_result:
            return BookDTO.model_validate(query_result), None
        else:
            return None, None

    @staticmethod
    def find_book_by_name(name: int) -> tuple[BookDTO | None, RepositoryError | None]:
        query_result = select_first_obj(obj_table=TblBooks, where_clauses=[TblBooks.name == name])
        if query_result:
            return BookDTO.model_validate(query_result), None
        else:
            return None, None

    @staticmethod
    def insert_book(book: BookDomain) -> tuple[BookDTO | None, RepositoryError | None]:
        new_book = TblBooks()
        new_book.isbn = book.isbn
        new_book.name = book.name
        new_book.author = book.author
        new_book.publisher = book.publisher
        new_book.release_date = book.release_date
        new_book.pages = book.pages
        new_book.description = book.description

        query_result, error = insert_obj(obj=new_book)
        if error:
            if error == SQLError.duplicate_entry:
                return None, RepositoryError.duplicate_entry

        if query_result:
            return BookDTO.model_validate(query_result), None
        else:
            return None, None

    @staticmethod
    @delete_cached_value(key="book-id-{book.id}")
    def update_book(book: BookDomain) -> tuple[BookDTO | None, RepositoryError | None]:
        obj_update = book.model_dump()
        query_result, error = update_obj(TblBooks, where_clauses=[TblBooks.id == book.id], update_values=obj_update)
        if error:
            if error == SQLError.not_found:
                return None, RepositoryError.not_found

        if query_result:
            return BookDTO(**book.model_dump()), None
        else:
            return None, None

    @staticmethod
    @delete_cached_value(key="book-id-{book_id}")
    def delete_book(book_id: int) -> SQLError | None:
        error = delete_obj(obj_table=TblBooks, where_clauses=[TblBooks.id == book_id])
        return error if error else None
