import library.adapters.repository as repo
import library.utilities.services as services
from library.domain.model import Book


def get_list_of_books():
    books = services.get_books(repo.repo_instance)
    return books

def get_number_of_books():
    number_of_books = services.get_number_of_books(repo.repo_instance)
    return number_of_books

def get_authors():
    authors = services.get_authors_list(repo.repo_instance)
    return authors

def set_search_results(array):
    services.set_search_results(repo.repo_instance, array)

def get_search_results():
    return services.get_search_results(repo.repo_instance)

def clear_search_results():
    services.clear_search_results(repo.repo_instance)

def get_publishers():
    return services.get_publishers(repo.repo_instance)

def get_book_by_id(book_id):
    return services.get_book_by_id(repo.repo_instance, book_id)

def get_available_authors():
    return services.get_available_authors(repo.repo_instance)

def get_review_by_book(book:Book):
    return services.get_review_by_book(repo.repo_instance, book)

def get_chunks(data_array, per_page):
    return services.get_chunks(repo.repo_instance, data_array, per_page)

def get_user(user_name):
    return services.get_user(repo.repo_instance, user_name)


def get_available_years():
    return services.get_available_years(repo.repo_instance)