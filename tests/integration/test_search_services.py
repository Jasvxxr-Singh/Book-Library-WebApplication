import pytest
import warnings
from library.search import services as services
from library.authentication.services import NameNotUniqueException, AuthenticationException
from library.adapters.memory_repository import MemoryRepository

def test_search_with_empty_string(in_memory_repo):
    query = ""
    authors = []
    publishers = []
    years = []
    ebook = None
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 3

def test_search_with_specific_authors(in_memory_repo):
    query = ""
    authors = ["Test Author"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 1


def test_search_with_non_existent_authors(in_memory_repo):
    query = ""
    authors = ["False Author"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 0

def test_search_with_multiple_authors(in_memory_repo):
    query = ""
    authors = ["Test Author", "Test AuthorTwo"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 2

def test_search_with_publishers(in_memory_repo):
    query = ""
    authors = []
    years = []
    ebook = None
    publishers = ["Publisher One", "Publisher Two"]
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 2


def test_search_with_non_existent_publishers(in_memory_repo):
    query = ""
    authors = []
    years = []
    ebook = None
    publishers = ["Publisher Fiv"]
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 0


def test_search_with_years(in_memory_repo):
    query = ""
    authors = []
    years = [2019, 2020]
    ebook = None
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 2


def test_search_for_query(in_memory_repo):
    query = "Two"
    authors = []
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 1


def test_search_for_query_and_search_params(in_memory_repo):
    query = "Two"
    authors = ["Test AuthorTwo"]
    years = [2021]
    ebook = None
    publishers = ["Publisher Two"]
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 1

def test_search_for_ebook_false(in_memory_repo):
    query = ""
    authors = []
    years = []
    ebook = "False"
    publishers = []
    results = services.search_for_items(in_memory_repo, query, authors, publishers, years, ebook)
    assert len(results) == 1
