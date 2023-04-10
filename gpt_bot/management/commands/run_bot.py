from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from gpt_bot.bot import main
