import configparser

from django.test import TestCase

from .chequing_scrapers import PCChequingScraper


class ParsingTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        config = configparser.ConfigParser()
        config.read('config.cfg')

        cls.scraper = PCChequingScraper(config['pc-chequing'])

    def test_scrape(self):
        self.scraper.login()
        self.scraper.scrape()
