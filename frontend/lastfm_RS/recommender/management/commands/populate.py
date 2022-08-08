from recommender.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """populate database"""

    def handle(self, *args, **kwargs):
        # c = client(1001, 'Frodo Bolsón', 33)
        # c.save()
        pass