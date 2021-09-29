import datetime


class TestCatalogModel:

    def test_book_fields(self, catalog):
        assert catalog.title == 'test catalog title'
        assert isinstance(catalog.id, int)
        assert isinstance(catalog.created_at, datetime.datetime)
        assert isinstance(catalog.updated_at, datetime.datetime)

