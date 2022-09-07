from flask import Blueprint, render_template, request, url_for, session
from library.search.services import create_search_fields
import library.utilities.utilities as utils
import library.adapters.repository as repo
from .services import search_for_items
from  library.browser.browser_bp import AddBookForm

search_bp = Blueprint('search_bp', __name__)




@search_bp.route('/search', methods=['GET', 'POST'])
def search(page_number=0):
    form = create_search_fields(repo.repo_instance, request.args)
    add_book_form = AddBookForm()
    query = request.args.get('search', '')
    authors = request.args.getlist('author')
    publishers = request.args.getlist('publisher')
    years = request.args.getlist('year')
    ebook = request.args.get('ebook')

    read_list = []
    try:
        user = session['user_name']
        user = utils.get_user(user)
        read_list = user.read_books
    except KeyError:
        pass


    books = search_for_items(repo.repo_instance, query, authors, publishers, years, ebook)

    book_chunks = list(utils.get_chunks(books, 15))

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
    return render_template('search.html',
                           read_list=read_list,
                           add_form=add_book_form,
                           base_url=base_url,
                           url_route="search_bp.search",
                           current_page=page_number,
                           prev_page=previous_page,
                           next_page=next_page,
                           num_pages=len(book_chunks),
                           form=form, book_list=book_chunks[page_number])