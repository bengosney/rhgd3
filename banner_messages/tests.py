# Standard Library
import datetime

# Django
from django.apps import apps
from django.urls import reverse

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

# First Party
from modulestatus import ModelStatus
from stef.test_helpers import postgres_text

# Locals
from .apps import BannerMessagesConfig
from .context_processors import messages
from .models import message

today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
yesterday = datetime.date.today() + datetime.timedelta(days=-1)


class BannerMessagesViewTests(TestCase):
    def setUp(self) -> None:
        self.message = message.objects.create(
            title="test", message="test", published_from=yesterday, published_to=tomorrow, status=ModelStatus.LIVE_STATUS
        )

    def test_redirects(self) -> None:
        url = self.message.dismiss_url
        response = self.client.get(url, follow=False)

        self.assertEqual(response.status_code, 302)

    def test_redirect_no_referer(self) -> None:
        url = self.message.dismiss_url
        response = self.client.get(url, follow=False)

        self.assertEqual(response.url, "/")

    def test_redirect_referer(self) -> None:
        url = self.message.dismiss_url
        referer = "/referer"
        response = self.client.get(url, follow=False, HTTP_REFERER=referer)

        self.assertEqual(response.url, referer)


class BannerMessagesTests(TestCase):
    @given(title=postgres_text, body=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_get_message(self, title, body, published_from, published_to) -> None:
        message.objects.create(
            title=title, message=body, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )
        all_messages = message.get_messages({})
        self.assertEqual(len(all_messages), 1)

    @given(title=postgres_text, body=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_dont_get_dismissed(self, title, body, published_from, published_to) -> None:
        m = message.objects.create(
            title=title, message=body, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )
        session = {m.session_key: True}
        all_messages = message.get_messages(session)
        self.assertEqual(len(all_messages), 0)

    @given(title=postgres_text, body=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_title(self, title, body, published_from, published_to) -> None:
        m = message.objects.create(
            title=title, message=body, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )

        self.assertEqual(f"{m}", title)

    @given(title=postgres_text, body=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_dismiss_url(self, title, body, published_from, published_to) -> None:
        m = message.objects.create(
            title=title, message=body, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )

        url = reverse("banner_messages:dismiss", kwargs={"slug": m.slug})
        self.assertEqual(m.dismiss_url, url)

    @given(title=postgres_text, body=postgres_text, published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_context_processor(self, title, body, published_from, published_to) -> None:
        m = message.objects.create(
            title=title, message=body, published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS
        )

        context = messages(None)
        test_context = {"banner_messages": [m]}

        self.assertEqual(context, test_context)

    def test_apps(self):
        self.assertEqual(apps.get_app_config("banner_messages").name, BannerMessagesConfig.name)
