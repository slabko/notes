import datetime
from datetime import datetime as real_datetime


def pytest_configure(config):

    class fake_datetime(datetime.__class__):

        def now():
            return real_datetime.now()

        def utcfromtimestamp(timestamp):
            return real_datetime.utcfromtimestamp(timestamp)

    datetime.datetime = fake_datetime
