from django.core.management import BaseCommand, CommandError
from .scraping.chequing_scrapers import PCChequingScraper

from apps.transactions.models import Transaction


class Command(BaseCommand):
    help = 'scrape data from banking site'

    def handle(self, *args, **kwargs):
        import configparser

        config = configparser.ConfigParser()
        config.read('config.cfg')

        self.scrape_presidents_choice(config)

    def insert(self, transactions):
        for transaction in transactions:
            date, value, description = transaction[0:3]

            created, trans = Transaction.objects.get_or_create(
                date=date,
                value=value,
                description=description
            )

    def scrape_presidents_choice(self, config):
        chequing_scraper = PCChequingScraper(credentials=config['pc-chequing'])
        chequing_scraper.login()
        expenses, income = chequing_scraper.scrape()

        self.insert(expenses)
        self.insert(income)
