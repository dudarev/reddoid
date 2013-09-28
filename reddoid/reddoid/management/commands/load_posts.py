from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import utc

from entities.models import Link, LinkPost

from sources.models import Source, Post
from sources.backends import GooglePlusSource, TwitterSource


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Load posts from sources'

    def handle(self, *args, **options):
        for s in Source.objects.all():
            if 'twitter' in s.url:
                screen_name = s.url.split('/')[-1]
                print screen_name
                source = TwitterSource(screen_name=screen_name)
                for tweet in source.fetch():
                    print tweet['content']
                    entities = tweet['entities']
                    urls = entities.get('urls', None)
                    post, is_created = Post.objects.get_or_create(
                        pid=tweet['id'], content=tweet['content'], source_id=s.id)
                    if urls:
                        for url in urls:
                            expanded_url = url.get('expanded_url', None)
                            if expanded_url:
                                print expanded_url
                                link, is_created = Link.objects.get_or_create(
                                        url=expanded_url)
                                LinkPost.objects.get_or_create(
                                        link=link, post=post)
