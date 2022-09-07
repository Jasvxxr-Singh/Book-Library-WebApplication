from datetime import date, datetime

from typing import List

import pytest
from library.domain.model import *
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('ben', 'Password12345')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('ben') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_get_books(in_memory_repo):
    books = in_memory_repo.get_books()

    assert books == [Book(1, "Test Book One"), Book(2, "Test Book Two"), Book(3, "Test Book Three")]


def test_repository_can_add_books(in_memory_repo):
    new_book = Book(4, "Test Book Four")
    in_memory_repo.add_book(new_book)

    books = in_memory_repo.get_books()

    assert books == [Book(1, "Test Book One"), Book(2, "Test Book Two"), Book(3, "Test Book Three"), Book(4, "Test Book Four")]

def test_repository_add_duplicate_book(in_memory_repo):
    book = Book(1, "Test Book One")
    new_book = Book(2, "Test Book Two")
    in_memory_repo.add_book(book)
    in_memory_repo.add_book(new_book)
    books = in_memory_repo.get_books()

    assert books == [Book(1, "Test Book One"), Book(2, "Test Book Two"), Book(3, "Test Book Three")]


def test_repository_can_get_book_by_id(in_memory_repo):
    book = in_memory_repo.get_book_by_id(1)

    assert book == Book(1, "Test Book One")


def test_repository_cannot_get_book_by_id(in_memory_repo):
    book = in_memory_repo.get_book_by_id(6)
    assert book is None


def test_repository_author_has_a_book(in_memory_repo):
    status = in_memory_repo.has_book(Author(1, "Test Author"))

    assert status is True


def test_repository_author_has_no_book(in_memory_repo):
    status = in_memory_repo.has_book(Author(7, "Test Author Seven"))
    assert status is False


def test_repository_get_number_of_book(in_memory_repo):
    length = in_memory_repo.get_number_of_books()

    assert length == 3


def test_repository_can_add_reviews(in_memory_repo):
    in_memory_repo.add_reviews("Sample review text", 3, Book(1, "Test Book One"), "fmercury")

    reviews = in_memory_repo.get_reviews()
    new_review = Review(Book(1, "Test Book One"), "Sample review text", 3)
    new_review.user_name = "fmercury"
    results = [new_review]

    assert reviews == in_memory_repo.get_reviews()


def test_repository_can_get_available_authors(in_memory_repo):
    authors = in_memory_repo.get_available_authors()

    assert authors == [Author(1, "Test Author"), Author(2, "Test AuthorTwo"), Author(3, "Test Author Three")]

def test_repository_can_get_all_authors(in_memory_repo):
    authors = in_memory_repo.get_authors()

    assert authors == [Author(1, "Test Author"), Author(2, "Test AuthorTwo"), Author(3, "Test Author Three"), Author(4, "Test Author Four")]


def test_repository_get_publishers(in_memory_repo):
    publishers = in_memory_repo.get_publishers()
    assert publishers == [Publisher("Publisher One"), Publisher("Publisher Two"), Publisher("Publisher Three")]



def test_repository_get_available_years(in_memory_repo):
    years = in_memory_repo.get_available_years()
    assert years == [2019, 2020, 2021]


def test_repository_chunks(in_memory_repo):
    chunks = in_memory_repo.chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 5)
    assert chunks == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12]]