from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, SelectField

import library.utilities.utilities as utils
from library.adapters.repository import AbstractRepository
from library.utilities.services import (
    get_available_authors,
    get_publishers,
    get_available_years,
)


def search_for_items(repo: AbstractRepository, user_input: str, authors, publishers, years, ebook):
    book_results = []
    user_input = user_input.lower()
    books = repo.get_books()


    for book in books:
        print(book.book_id)
        if (
                user_input in str(book.book_id)
                or user_input in book.title.lower()
                or user_input in book.publisher.name.lower()
        ):
            book_results.append(book)

    if publishers:
        book_results = filter(
            lambda x: any(publisher == x.publisher.name for publisher in publishers),
            book_results,
        )

    if years:
        book_results = filter(
            lambda x: any(int(year) == x.release_year for year in years), book_results
        )

    if ebook == "True":
        new_results = []
        for i in book_results:
            if i.ebook:
                new_results.append(i)
        book_results = new_results

    if ebook == "False":
        new_results = []
        for i in book_results:
            if not i.ebook:
                new_results.append(i)

        book_results = new_results

    user_results = []
    if authors:
        for book in book_results:
            new_list = [auth.full_name for auth in book.authors]
            if any(item in new_list for item in authors):
                user_results.append(book)
    else:
        user_results = book_results

    return list(user_results)


def create_search_fields(repo: AbstractRepository, request_args):
    publishers = get_publishers(repo)
    authors = get_available_authors(repo)
    years = get_available_years(repo)
    print(years)
    form = SearchForm(request_args)
    form.publisher.choices = [
                                 (publisher.name, publisher.name) for publisher in publishers
                             ] + [("", "Publishers")]
    form.author.choices = [
                              (author.full_name, author.full_name) for author in authors
                          ] + [("", "Authors")]
    form.year.choices = [(year, year) for year in years] + [("", "Release Year")]
    return form


class SearchForm(FlaskForm):
    search = StringField("search")
    publisher = SelectMultipleField("Publishers")
    author = SelectMultipleField("Authors")
    year = SelectMultipleField("Years")
    ebook = SelectField(
        "Ebook",
        choices=[("", "Ebook"), (True, "True"), (False, "False"), ("both", "Both")],
    )
    submit = SubmitField("Find")