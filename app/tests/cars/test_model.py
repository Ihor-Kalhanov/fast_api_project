import datetime


class TestCarModel:

    def test_book_fields(self, car):
        assert car.name == 'test car name'
        assert car.description == 'test car description'
        assert isinstance(car.created_at, datetime.datetime)
        assert isinstance(car.updated_at, datetime.datetime)

