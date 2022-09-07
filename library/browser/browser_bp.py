from better_profanity import profanity
from flask import Blueprint, render_template, request, url_for, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import SelectField, TextAreaField, SubmitField, IntegerField, HiddenField, StringField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length
from wtforms.widgets import HiddenInput

import library.utilities.utilities as utils
import library.adapters.repository as repo
from library.authentication.authentication import login_required
from library.browser import services
from library.domain.model import Review

browser_bp = Blueprint("browser_bp", __name__, url_prefix="/browsing")

INVALID_CHOICE_MESSAGE = "Invalid Choice: not an Int"

INVALID_REVIEW_TEXT_MESSAGE = "Invalid review text."
RATING_REQUIRED_MESSAGE = "Ratings must be an integer between 1 and 10."
INVALID_RATING_RANGE_MESSAGE = "Ratings must be an integer between 1 and 10."

REVIEW_TEXT_REQUIRED_MESSAGE = "Reviews must be at least one character long."
INVALID_REVIEW_TEXT_LENGTH_MESSAGE = "Reviews must be at least one character long."
REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE = "No profanity"


@browser_bp.route("/books", methods=["GET", "POST"])
def browse_books(page_number=0):
    books = utils.get_list_of_books()
    total_num_of_books = len(books)
    book_chunks = utils.get_chunks(books, 10)
    form = AddBookForm()

    read_list = []
    try:
        user = session['user_name']
        user = utils.get_user(user)
        read_list = user.read_books
    except KeyError:
        pass

    page_number = request.args.get("page_number")
    if page_number is None:
        page_number = 0

    page_number = int(page_number)
    if page_number == 0:
        previous_page = 0
    else:
        previous_page = page_number - 1

    if page_number == len(book_chunks) - 1:
        next_page = len(book_chunks) - 1
    else:
        next_page = page_number + 1

    base_url = url_for("browser_bp.browse_books")


    return render_template(
        "books/books.html",
        read_list=read_list,
        base_url=base_url,
        form=form,
        url_route="browser_bp.browse_books",
        total_books=total_num_of_books,
        current_page=page_number,
        book_list=book_chunks[page_number],
        num_pages=len(book_chunks),
        prev_page=previous_page,
        next_page=next_page,

    )


@browser_bp.route("/authors", methods=["GET"])
def browse_authors(page_number=0):
    authors = utils.get_authors()
    total_num_of_authors = len(authors)
    author_chunks = utils.get_chunks(authors, 15)
    page_number = request.args.get("page_number")
    available_authors = utils.get_available_authors()
    showing_available_authors = False
    if page_number is None:
        page_number = 0

    page_number = int(page_number)
    if page_number == 0:
        previous_page = 0
    else:
        previous_page = page_number - 1

    if page_number == len(author_chunks) - 1:
        next_page = len(author_chunks) - 1
    else:
        next_page = page_number + 1

    return render_template(
        "authors/authors.html",
        showing_available_authors=showing_available_authors,
        available_authors=available_authors,
        total_authors=total_num_of_authors,
        current_page=page_number,
        url_route="browser_bp.browse_authors",
        author_list=author_chunks[page_number],
        num_pages=len(author_chunks),
        prev_page=previous_page,
        next_page=next_page,
    )


@browser_bp.route("/publishers", methods=["GET"])
def browse_publishers():
    publishers = utils.get_publishers()
    total_num_of_publishers = len(publishers)
    publisher_chunks = utils.get_chunks(publishers, 5)
    page_number = request.args.get("page_number")
    if page_number is None:
        page_number = 0
    page_number = int(page_number)

    if page_number == 0:
        previous_page = 0
    else:
        previous_page = page_number - 1

    if page_number == len(publisher_chunks) - 1:
        next_page = len(publisher_chunks) - 1
    else:
        next_page = page_number + 1

    return render_template(
        "publishers.html",
        total_publishers=total_num_of_publishers,
        current_page=page_number,
        url_route="browser_bp.browse_publishers",
        publisher_list=publisher_chunks[page_number],
        num_pages=len(publisher_chunks),
        prev_page=previous_page,
        next_page=next_page,
    )


@browser_bp.route("/books/<book_id>", methods=["GET", "POST"])
def book_extend(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template("books/book_extend.html", book=book)


@browser_bp.route("/books/<book_id>/reviews", methods=["GET", "POST"])
@login_required
def reviews(book_id):
    form = ReviewForm()

    book = repo.repo_instance.get_book_by_id(book_id)

    try:
        user_name = session["user_name"]
    except KeyError:
        user_name = "Anonymous"

    if form.validate_on_submit():
        services.add_review(
            repo.repo_instance, form.review.data, form.rating.data, book, user_name
        )
        review = Review(book, form.review.data, form.rating.data)

        user = repo.repo_instance.get_user(user_name)
        user.add_review(review)
        review.user = user

        repo.repo_instance.add_review(review)
        return redirect(url_for("browser_bp.reviews", book_id=book_id))
    list_of_reviews = utils.get_review_by_book(book)

    return render_template(
        "review.html",
        form=form,
        book=book,
        reviews=list_of_reviews,
        user_name=user_name,
    )


@browser_bp.route("/add_readlist", methods=["GET", "POST"])
@login_required
def add_readlist():
    if request.method == "POST":
        book_id = int(request.form["book_id"])
        base_url = request.form["base_url"]
        book = repo.repo_instance.get_book_by_id(book_id)

        user_name = session["user_name"]
        user = repo.repo_instance.get_user(user_name)
        repo.repo_instance.add_to_readlist(user, book)
        user.read_a_book(book)
        return redirect(base_url)

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = INVALID_REVIEW_TEXT_MESSAGE
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    rating = SelectField(
        "Rating: ",
        [
            DataRequired(message=RATING_REQUIRED_MESSAGE),
            NumberRange(min=1, max=5, message=INVALID_RATING_RANGE_MESSAGE),
        ],
        choices=range(1, 6),
        coerce=int,
        default=6,
    )
    review = TextAreaField(
        "Review: ",
        [
            DataRequired(message=REVIEW_TEXT_REQUIRED_MESSAGE),
            Length(min=1, message=INVALID_REVIEW_TEXT_LENGTH_MESSAGE),
            ProfanityFree(message=REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE),
        ],
    )
    submit = SubmitField("Submit")


class AddBookForm(FlaskForm):
    add_book = SubmitField("Add Book")
    book_id = IntegerField(widget=HiddenInput())
    base_url = StringField(widget=HiddenInput())
