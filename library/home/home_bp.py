from flask import Blueprint, render_template
import library.utilities.utilities as utils
from library.search.search import request
from library.search.services import create_search_fields
import library.adapters.repository as repo


home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route('/home', methods=['GET'])
def home():

    form = create_search_fields(repo.repo_instance, request.args)
    book_list = utils.get_list_of_books()
    return render_template('home.html',
                           form=form)
