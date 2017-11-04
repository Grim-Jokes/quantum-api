import logging

from .scrapers import PcScraper

from .actions import (
    DetailAction,
    LoginAction,
    ParseAction,
    SelectMonthAction,
    ShowLoginModal,
    SubmitAction,
    WaitAction
)

logger = logging.getLogger()


class PCChequingScraper(PcScraper):
    def __init__(self, credentials):
        logging.info("Parsing chequing")
        url = "https://www.simplii.com/en/home.html"
        super(PCChequingScraper, self).__init__(url, credentials)
        self.username_field_selector = "input#card-number-"
        self.password_field_selector = "input[type='password']"

    def login(self):

        ShowLoginModal(self.session).execute()

        super(PCChequingScraper, self).login()

        LoginAction(self.session).execute()

        WaitAction(self.session).execute()

    def scrape(self):
        try:
            WaitAction(self.session).execute()
            
            DetailAction(self.session).execute()

            WaitAction(self.session).execute()

            SelectMonthAction(self.session).execute()

            SubmitAction(self.session, "ui-button.primary")

            WaitAction(self.session).execute()

            expenses, income = ParseAction(self.session).execute()

            return expenses, income
        except Exception as e:
            self.session.render('error.png')
            raise e
