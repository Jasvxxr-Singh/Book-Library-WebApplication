from library.adapters.memory_repository import AbstractRepository


def get_books(repo: AbstractRepository):
    return repo.get_books()

def get_number_of_books(repo: AbstractRepository):
    return repo.get_number_of_books()


def get_authors_list(repo: AbstractRepository):
    return repo.get_authors()


def set_search_results(repo: AbstractRepository, search_results: []):
    repo.set_search_results(search_results)


def get_search_results(repo: AbstractRepository):
    return repo.get_search_results()


def clear_search_results(repo: AbstractRepository):
    repo.clear_search_results()


def get_publishers(repo: AbstractRepository):
    return repo.get_publishers()


def get_available_authors(repo: AbstractRepository):
    return repo.get_available_authors()


def get_book_by_id(repo: AbstractRepository, book_id):
    return repo.get_book_by_id(book_id)


def get_review_by_book(repo: AbstractRepository, book):
    return repo.get_reviews_by_book(book)


def get_chunks(repo: AbstractRepository, data_array: [], per_page: int):
    return list(repo.chunks(data_array, per_page))

def get_user(repo: AbstractRepository, user_name):
    return repo.get_user(user_name)

def get_available_years(repo: AbstractRepository):
    return repo.get_available_years()