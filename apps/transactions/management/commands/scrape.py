from django.core.management import BaseCommand, CommandError
from .scraping.chequing_scrapers import PCChequingScraper


class Command(BaseCommand):
    help = 'scrape data from banking site'

    def handle(self, *args, **kwargs):
        import configparser

        config = configparser.ConfigParser()
        config.read('config.cfg')

        self.scrape_presidents_choice(config)

    def scrape_presidents_choice(self, config):
        chequing_scraper = PCChequingScraper(credentials=config['pc-chequing'])
        chequing_scraper.login()
        expense, income = chequing_scraper.scrape()
