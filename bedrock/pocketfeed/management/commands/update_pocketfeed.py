from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from bedrock.pocketfeed.models import PocketArticle


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        error = None
        updated, deleted = PocketArticle.objects.refresh(count=4)

        if updated is None:
            error = 'There was a problem updating the Pocket feed'
            raise CommandError(error)

        if not options['quiet']:
            if updated:
                print('Refreshed %s articles from Pocket' % updated)

                if deleted:
                    print('Deleted %s old articles' % deleted)
            else:
                print('Pocket feed is already up to date')
