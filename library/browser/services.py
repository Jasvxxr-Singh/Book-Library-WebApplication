
import library.utilities.utilities as utils
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review


def get_search_results():
    return utils.get_search_results()

def sort_by_date(array):
    results = get_search_results()
    results.sort(key=lambda x:x.release_year)
    return results


def add_review(repo: AbstractRepository, review_string, rating, book, user_name):
    repo.add_reviews(review_string, rating, book, user_name)


