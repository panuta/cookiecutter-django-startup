from django.core import mail
from django.contrib.auth.models import AnonymousUser
from django.test.client import Client, RequestFactory
from django.urls import reverse, resolve, Resolver404

from test_plus.test import TestCase

from app.accounts.utils import findall_urls, strip_url_to_path


class TestEmailUser(TestCase):

    def setUp(self):
        pass

    def test_new_user_signup(self):
        user_email = 'johnsnow@got.com'
        request = RequestFactory().post(
            reverse('account_signup'),
            {
                'display_name': 'John Snow',
                'email': user_email,
                'password1': 'winteriscoming'
            }
        )

        from django.contrib.sessions.middleware import SessionMiddleware
        SessionMiddleware().process_request(request)
        request.user = AnonymousUser()

        # Sign user up
        from allauth.account.views import signup
        response = signup(request)

        assert response.status_code == 302
        assert len(mail.outbox) == 1

        # Get confirm url from email body
        confirm_url = None
        for url in findall_urls(mail.outbox[0].body):
            striped_url = strip_url_to_path(url)
            try:
                match = resolve(striped_url)
            except Resolver404:
                pass
            else:
                if match.url_name == 'confirm_email':
                    confirm_url = striped_url
                    break

        # Simulate click on confirm url
        client = Client()
        response = client.get(confirm_url)

        assert response.status_code == 302

        from django.contrib import auth
        user = auth.get_user(client)
        assert user.is_authenticated

    def test_duplicated_user_signup(self):
        pass

    def test_confirm_on_authenticated_session(self):
        pass

    def test_invalid_confirm_url(self):
        pass

    def test_already_confirmed_confirm_url(self):
        pass

    def test_user_login(self):
        pass

    def test_recover_user_password(self):
        pass
