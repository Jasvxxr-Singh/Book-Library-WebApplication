from abc import ABC
from datetime import date
from typing import List

from sqlalchemy import desc, asc, text
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import *
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()




class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()



    def add_book(self, book: Book):
        with self._session_cm as scm:
            try:
                scm.session.add(book)
            except:
                pass
            scm.commit()

    def add_publisher(self, publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()


    def add_reviews(self, review_text: str, rating: int, book: Book, user_name):
        pass

    def get_books(self) -> list[Book]:
        books = self._session_cm.session.query(Book).all()
        return books

    def get_book_by_id(self, book_id):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            pass
        return book

    def get_available_authors(self):
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_authors(self) -> list[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_users(self) -> list[User]:
        users = self._session_cm.session.query(User).all()
        return users

    def get_available_years(self):
        data = self._session_cm.session.query(Book).all()
        new_list = []
        for items in data:
            if items.release_year != None and items.release_year not in new_list:
                new_list.append(items.release_year)
        return new_list


    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_publishers(self) -> list[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def get_search_results(self) -> list[Book]:
        pass

    def get_user(self, user_name) -> User or None:
        try:
            return self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            return None

    def get_reviews_by_book(self, book: Book):
        current_book_id = book.book_id
        new_list = []
        data = self._session_cm.session.query(Review).all()
        for i in data:
            if i.book.book_id == current_book_id:
                new_list.append(i)
        return new_list

    def get_number_of_books(self) -> int:
        return self._session_cm.session.query(Book).count()

    def has_book(self, author: Author) -> bool:
        pass

    def clear_search_results(self):
        pass

    def set_search_results(self, array):
        pass

    def chunks(self, data_array: [], per_page: int):
        if len(data_array) > per_page:
            for i in range(0, len(data_array), per_page):
                yield data_array[i: i + per_page]
        else:
            yield data_array

    def add_to_readlist(self, user, book):
        current_user_id = user.id
        current_book_id = book.book_id
        sql_statement = text("""INSERT INTO user_reading_lists(user_id, book_id)  VALUES(:user_id, :book_id)""")
        self._session_cm.session.execute(sql_statement, {"user_id": current_user_id, "book_id": current_book_id})
        self._session_cm.session.commit()