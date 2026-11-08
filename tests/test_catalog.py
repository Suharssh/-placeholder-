import json

import pytest

from linernotes.catalog import CatalogError, JsonCatalog


def write(tmp_path, data):
    p = tmp_path / "catalog.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_loads_sample(catalog_path):
    cat = JsonCatalog(catalog_path)
    assert cat.artist("kendrick-lamar").name == "Kendrick Lamar"
    assert len(cat.artists()) == 3


def test_aliases_are_tuples(catalog_path):
    assert isinstance(JsonCatalog(catalog_path).artist("kendrick-lamar").aliases, tuple)


def test_unknown_artist(catalog_path):
    with pytest.raises(CatalogError):
        JsonCatalog(catalog_path).artist("nobody")


def test_duplicate_ids_rejected(tmp_path):
    p = write(tmp_path, {"artists": [{"id": "x", "name": "X"}, {"id": "x", "name": "X2"}]})
    with pytest.raises(CatalogError):
        JsonCatalog(p).artists()  # eager or lazy loading: either way it must fail


def test_missing_name_rejected(tmp_path):
    p = write(tmp_path, {"artists": [{"id": "x"}]})
    with pytest.raises(CatalogError):
        JsonCatalog(p).artists()
