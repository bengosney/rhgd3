# Standard Library
import datetime

# Django
from django.db import connection

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

# First Party
from modulestatus import ModelStatus
from rhgdesign.test_helpers import postgres_text

# Locals
from .models import statusDateRangeTest, statusDateTest, statusTest

today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
yesterday = datetime.date.today() + datetime.timedelta(days=-1)


class StatusTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(statusTest)

    @given(title=postgres_text)
    def test_live(self, title):
        statusTest.objects.create(title=title, status=ModelStatus.LIVE_STATUS)
        all_items = statusTest.objects.all()
        self.assertEqual(len(all_items), 1)

    @given(title=postgres_text)
    def test_draft(self, title):
        statusTest.objects.create(title=title, status=ModelStatus.DRAFT_STATUS)
        all_items = statusTest.objects.all()
        self.assertEqual(len(all_items), 0)

    @given(title=postgres_text)
    def test_hidden(self, title):
        statusTest.objects.create(title=title, status=ModelStatus.HIDDEN_STATUS)
        all_items = statusTest.objects.all()
        self.assertEqual(len(all_items), 0)


class DateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(statusDateTest)

    @given(title=postgres_text, published=dates(max_value=yesterday))
    def test_get(self, title, published):
        statusDateTest.objects.create(title=title, published=published, status=ModelStatus.LIVE_STATUS)
        all_items = statusDateTest.objects.all()
        self.assertEqual(len(all_items), 1)

    @given(title=postgres_text, published=dates(min_value=tomorrow))
    def test_not_yet(self, title, published):
        statusDateTest.objects.create(title=title, published=published, status=ModelStatus.LIVE_STATUS)
        all_items = statusDateTest.objects.all()
        self.assertEqual(len(all_items), 0)


class DateRangeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(statusDateRangeTest)

    @given(title=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_get(self, title, published_from, published_to) -> None:
        statusDateRangeTest.objects.create(
            title=title, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )
        all_items = statusDateRangeTest.objects.all()
        self.assertEqual(len(all_items), 1)

    @given(title=postgres_text, published_from=dates(max_value=yesterday), published_to=dates(max_value=yesterday))
    def test_date_in_past(self, title, published_from, published_to) -> None:
        statusDateRangeTest.objects.create(
            title=title, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )
        all_items = statusDateRangeTest.objects.all()
        self.assertEqual(len(all_items), 0)

    @given(title=postgres_text, published_from=dates(min_value=tomorrow), published_to=dates(min_value=tomorrow))
    def test_date_in_future(self, title, published_from, published_to) -> None:
        statusDateRangeTest.objects.create(
            title=title, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )
        all_items = statusDateRangeTest.objects.all()
        self.assertEqual(len(all_items), 0)
