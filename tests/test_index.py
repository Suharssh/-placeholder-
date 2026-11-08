import pytest

from linernotes.catalog import JsonCatalog
from linernotes.search import SearchIndex


@pytest.fixture
def catalog(catalog_path):
    return JsonCatalog(catalog_path)


@pytest.fixture
def artist_index(catalog):
    idx = SearchIndex(lambda a: (a.name, *a.aliases))
    idx.extend(catalog.artists())
    return idx


def top(index, q):
    results = index.search(q)
    assert results, f"no results for {q!r}"
    return results[0].item


def test_len_counts_items_not_keys(artist_index):
    assert len(artist_index) == 3


@pytest.mark.parametrize("q", ["kendrick", "Kend", "kendrik", "k.dot", "kdot", "lamar"])
def test_finds_kendrick(artist_index, q):
    assert top(artist_index, q).id == "kendrick-lamar"


def test_accent_insensitive(artist_index):
    assert top(artist_index, "beyonce").id == "beyonce"


def test_typo(artist_index):
    assert top(artist_index, "beyonse").id == "beyonce"


def test_as_you_type(artist_index):
    assert top(artist_index, "j").id == "j-cole"
    assert top(artist_index, "be").id == "beyonce"


def test_empty_query(artist_index):
    assert artist_index.search("") == []
    assert artist_index.search("   ") == []


def test_no_duplicate_items(artist_index):
    # Kendrick has 3 keys ("Kendrick Lamar", "K.Dot", "K Dot"); he must appear once.
    ids = [m.item.id for m in artist_index.search("k", min_score=0.0)]
    assert len(ids) == len(set(ids))


def test_limit(artist_index):
    assert len(artist_index.search("e", limit=1, min_score=0.0)) <= 1


def test_sorted_best_first(artist_index):
    scores = [m.score for m in artist_index.search("j", min_score=0.0)]
    assert scores == sorted(scores, reverse=True)
