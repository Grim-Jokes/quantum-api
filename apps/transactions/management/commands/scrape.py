from django.core.management import BaseCommand
from .scraping.chequing_scrapers import PCChequingScraper


from apps.transactions.models import Transaction, Description


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

            desc, created = Description.objects.get_or_create(name=description)

            trans, created = Transaction.objects.get_or_create(
                date=date,
                value=value,
                name=desc
            )

    def scrape_presidents_choice(self, config):
        try:

            chequing_scraper = PCChequingScraper(
                credentials=config['pc-chequing'])
            chequing_scraper.login()
            expenses, income = chequing_scraper.scrape()

            self.insert(expenses)
            self.insert(income)

        except Exception as e:
            self.stderr.write(str(e))
