from django.test import TestCase, Client
from django.urls import reverse
from recommender.views import *
from recommender.management.commands.populate import Command

from .models import *
from lastfm_RS.settings import BASE_DIR
pathToProject = BASE_DIR


class Tests(TestCase):
    """ Test template
    """

    def setUp(self):
        self.populate = Command()
        self.clear_db()
        self.create_objects()
        self.client = Client()

    @classmethod
    def decode(cls, txt):
        return txt.decode("utf-8")

    def create_objects(self):
        """ create objects for the test
        """
        pass

    def test01(self):
        """ Test rentals for client 1001
        """

        # Also works, but without URL
        # response = self.client.get(
        #     reverse(show, kwargs={'id':1001}), follow=True)

        # response = self.client.get(
        #     '/exam/client/1001', follow=True)

        # response_txt = self.decode(response.content)

        # Check that response contents correspond to expected contents
        # using self.assertIn(str, str)

    def clear_db(self):
        # model.objects.all().delete()
        pass