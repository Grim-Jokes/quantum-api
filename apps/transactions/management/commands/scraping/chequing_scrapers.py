import logging
from datetime import datetime

from .scrapers import PcScraper
from .errors import NoRowsException

from .actions import (
    DetailAction,
    LoginAction,
    ParseAction,
    SelectMonthAction,
    SubmitAction,
    WaitAction
)

from decimal import Decimal, InvalidOperation

logger = logging.getLogger()



class PCChequingScraper(PcScraper):
    def __init__(self, credentials):
        logging.info("Parsing chequing")
        url = "https://www.txn.banking.pcfinancial.ca/ebm-resources/public/client/web/index.html"
        super(PCChequingScraper, self).__init__(url, credentials)
        self.username_field_selector = "input[type='text'].ember-view"
        self.password_field_selector = "input[type='password'].ember-view"

    def login(self):
        super(PCChequingScraper, self).login()

        LoginAction(self.session).execute()

        WaitAction(self.session).execute()

    def scrape(self):
        DetailAction(self.session).execute()

        WaitAction(self.session).execute()

        SelectMonthAction(self.session).execute()

        SubmitAction(self.session, "ui-button.custom-search-button")

        WaitAction(self.session).execute()

        expenses, income = ParseAction(self.session).execute()

        return expenses, income
