from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.csv_data_importer import load_users, load_books_and_authors

def populate(data_path: Path, repo: AbstractRepository, database_mode):
    load_users(data_path, repo)
    if database_mode:
        load_books_and_authors(data_path, repo, database_mode)
    else:
        load_authors(data_path, repo)
        load_books(data_path, repo)
