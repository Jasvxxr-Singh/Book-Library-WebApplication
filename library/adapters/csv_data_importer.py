from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader
from pathlib import Path

import json
import csv


def read_csv_file(filename: str):
    with open(filename, encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_books_and_authors(data_path: Path, repo: AbstractRepository, database_mode: bool):
    authors = str(data_path / 'book_authors_excerpt.json')
    books = str(data_path / 'comic_books_excerpt.json')
    reader = BooksJSONReader(books, authors)
    reader.read_json_files()
    list_of_authors = []
    list_of_publishers = []
    list_of_books = []
    list_of_reviews = []
    # Create new objects, based on JSON book objects
    for book in reader.dataset_of_books:
        # AUTHORS
        for author in book.authors:
            new_author = Author(
                author.unique_id,
                author.full_name
            )
            if new_author not in list_of_authors:
                list_of_authors.append(new_author)

        # PUBLISHERS
        if book.publisher not in list_of_publishers:
            list_of_publishers.append(book.publisher)

        # BOOKS
        new_book = Book(
            book.book_id,
            book.title
        )
        new_book.ebook = book.ebook
        new_book.num_pages = book.num_pages
        new_book.description = book.description
        if book.release_year is not None:
            new_book.release_year = book.release_year

        # Connect book with newly created Publisher objects
        for publisher in list_of_publishers:
            if book.publisher.name == publisher.name:
                new_book.publisher = publisher

        # Connect book to newly created Authors objects
        for new_author in list_of_authors:
            for author in book.authors:
                if author.unique_id == new_author.unique_id:
                    new_book.add_author(new_author)

        list_of_books.append(new_book)

    # load reviews
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):

        book_id = int(data_row[1])
        book = [book for book in list_of_books if book.book_id == book_id][0]

        user_name = data_row[0]

        user = repo.get_user(user_name)
        review = Review(
            book=book,
            review_text=data_row[2],
            rating=int(data_row[3]),
        )
        review.user = user
        user.add_review(review)
        if review not in list_of_reviews:
            list_of_reviews.append(review)

    # Loading new objects into the repo
    for book in list_of_books:
        repo.add_book(book)

    for author in list_of_authors:
        repo.add_author(author)

    for publisher in list_of_publishers:
        repo.add_publisher(publisher)

    for review in list_of_reviews:
        try:
            repo.add_review(review)
        except:
            pass


def load_books(data_path: Path, repo: AbstractRepository):
    authors = str(data_path / "book_authors_excerpt.json")
    comic_books = str(data_path / "comic_books_excerpt.json")
    reader_instance = BooksJSONReader(comic_books, authors)
    reader_instance.read_json_files()
    for book in reader_instance.dataset_of_books:
        repo.add_publisher(book.publisher)
        repo.add_book(book)



def load_authors(data_path: Path, repo: AbstractRepository):
    authors_file = str(data_path / "book_authors_excerpt.json")
    file = open(authors_file)
    authors_file_content = file.readlines()
    for authors in authors_file_content:
        temp_dict = json.loads(authors)
        new_author = Author(int(temp_dict["author_id"]), temp_dict["name"])
        repo.add_author(new_author)


def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(user_name=data_row[1], password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users