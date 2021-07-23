# Standard Library
import datetime
import string
from typing import Any

# Django
from django.contrib.admin.sites import AdminSite
from django.test import Client

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text

# Locals
from .admin import ContactAdmin
from .models import ContactSubmission, Empty, HomePageHeader, Page


def sane_text():
    # Third Party
    from hypothesis.strategies import text

    return text(min_size=1, max_size=255, alphabet=f"{string.ascii_letters}{string.digits}")


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def get_page(self, title, body, home=False):
        return Page(title=title, body=body, is_home_page=home)

    def test_only_one_homepage(self):
        page_1 = self.get_page("page1", "page1", True)
        page_1.save()
        page_2 = self.get_page("page2", "page2", True)
        page_2.save()

        pages = Page.objects.filter(is_home_page=True)

        self.assertEqual(len(pages), 1)


class PageMethodTests(TestCase):
    @given(sane_text())
    def test_nav_title_title(self, expected):
        """Page nav title should return title."""

        page = Page(title=expected)

        self.assertEqual(page.nav_title_actual, expected)

    @given(text(min_size=5), text(min_size=5))
    def test_nav_title_nav(self, expected, title):
        """Page nav title should return nav_title."""

        page = Page(title=title, nav_title=expected)

        self.assertEqual(page.nav_title_actual, expected)
        if expected != title:
            self.assertNotEqual(page.nav_title_actual, title)

    def test_url(self):
        """Page url."""

        expected = "page title"

        page = Page(title=expected)
        page.save()

        self.assertEqual(page.url, "/%s/" % page.slug)

    @given(sane_text())
    def test_str(self, expected):
        """_unicode_"""

        page = Page(title=expected)

        self.assertEqual(str(page), expected)


class EmptyNodeMethodTests(TestCase):
    def test_url(self):
        """Test the #URL."""

        expected = "empty node"

        empty = Empty(title=expected)
        empty.save()

        self.assertEqual(empty.url, "#%s" % empty.slug)


class ContactSubmissionMethodTest(TestCase):
    @given(sane_text())
    def test_str(self, expected):
        """_unicode_"""

        name = ContactSubmission(name=expected)

        self.assertEqual(str(name), expected)


class ContactAdmminMethodTest(TestCase):
    site: Any

    def setUp(self):
        self.site = AdminSite

    def test_permissions(self):
        """make sure permissions are correct."""

        admin = ContactAdmin(ContactSubmission, self.site)

        self.assertFalse(admin.has_add_permission(None, None))
        self.assertFalse(admin.has_delete_permission(None, None))


today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
yesterday = datetime.date.today() + datetime.timedelta(days=-1)

today_last_year = today.replace(year=today.year - 1)
tomorrow_last_year = tomorrow.replace(year=tomorrow.year - 1)
yesterday_last_year = yesterday.replace(year=yesterday.year - 1)


class HomePageHeaderTest(TestCase):
    def test_no_homepageheader_returns_none(self):
        """Not having a homepageheader should return none."""
        self.assertIsNone(HomePageHeader.getCurrentImage())

    def test_not_in_date(self):
        """Not having a homepageheader in date should return first header."""

        HomePageHeader(strapline="test_no_date")
        HomePageHeader(strapline="test_not_in_date", start=tomorrow, end=tomorrow).save()
        self.assertEqual(HomePageHeader.getCurrentImage().strapline, "test_no_date")

    def test_single_day_homepageheader(self):
        """HomePageHeader with the same start and end should return an svg."""

        homepageheaderStrapline = "test_single_day_homepageheader"
        HomePageHeader(strapline=homepageheaderStrapline, start=today, end=today).save()
        homepageheader = HomePageHeader.getCurrentImage()

        self.assertIsNotNone(homepageheader)
        self.assertEqual(homepageheader.strapline, homepageheaderStrapline)

    def test_range_homepageheader(self):
        """HomePageHeader with a range should return an svg."""

        homepageheaderStrapline = "test_range_homepageheader"
        HomePageHeader(strapline=homepageheaderStrapline, start=yesterday, end=tomorrow).save()
        homepageheader = HomePageHeader.getCurrentImage()

        self.assertIsNotNone(homepageheader)
        self.assertEqual(homepageheader.strapline, homepageheaderStrapline)

    def test_single_day_homepageheader_last_year(self):
        """HomePageHeader with the same start and end should return an svg."""

        homepageheaderStrapline = "test_single_day_homepageheader_last_year"
        HomePageHeader(strapline=homepageheaderStrapline, start=today_last_year, end=today_last_year).save()
        homepageheader = HomePageHeader.getCurrentImage()

        self.assertIsNotNone(homepageheader)
        self.assertEqual(homepageheader.strapline, homepageheaderStrapline)

    def test_range_homepageheader_last_year(self):
        homepageheaderStrapline = "test_range_homepageheader_last_year"
        HomePageHeader(strapline=homepageheaderStrapline, start=yesterday_last_year, end=tomorrow_last_year).save()
        homepageheader = HomePageHeader.getCurrentImage()

        self.assertIsNotNone(homepageheader)
        self.assertEqual(homepageheader.strapline, homepageheaderStrapline)
