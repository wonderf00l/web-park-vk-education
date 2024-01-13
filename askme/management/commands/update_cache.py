from django.core.cache import cache
from django.core.management import BaseCommand

from askme.models import Tag, Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        top_tags = Tag.objects.top_tags(quantity=10)
        cache.set('top_tags', top_tags, 180)

        top_users = Profile.objects.top_users(quantity=10)
        cache.set('top_users', top_users, 180)
