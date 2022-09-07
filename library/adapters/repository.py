import abc
from typing import List
from datetime import date

from library.domain.model import *

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_books(self) -> list[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> list[Author]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User or None:
        raise NotImplementedError

    @abc.abstractmethod
    def has_book(self, author: Author) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_search_results(self) -> list[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def set_search_results(self, array):
        raise NotImplementedError

    @abc.abstractmethod
    def clear_search_results(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> list[Publisher]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_available_authors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, book_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_by_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def add_reviews(self, review_text: str, rating: int, book: Book, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def chunks(self, data_array: [], per_page: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_available_years(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError


    @abc.abstractmethod
    def add_to_readlist(self, user, book):
        raise NotImplementedError
