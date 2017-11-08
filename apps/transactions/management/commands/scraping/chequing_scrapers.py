import logging

from datetime import datetime

from .scrapers import PcScraper

from .actions import (
    ClickDetailAction,
    LoginAction,
    ParseAction,
    SelectMonthAction,
    SelectMonthButtonAction,
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

    def get_current_month(self):
        return datetime.today().month

    def go_to_detail_page(self):

        WaitAction(self.session).execute()

        ClickDetailAction(self.session).execute()

        WaitAction(self.session).execute()

    def get_all_transactions(self, all_expenses, all_income):

        current_month = self.get_current_month()

        for month in range(1, current_month + 1):

            SelectMonthAction(self.session, month).execute()

            SubmitAction(self.session, "ui-button.primary").execute()

            WaitAction(self.session).execute()

            expenses, income = ParseAction(self.session).execute()

            all_expenses.extend(expenses)
            all_income.extend(all_income)

    def scrape(self):
        try:
            self.go_to_detail_page()

            all_expenses = []
            all_income = []

            SelectMonthButtonAction(self.session).execute()

            self.get_all_transactions(all_expenses, all_income)

            return all_expenses, all_income
        except Exception as e:
            self.session.render('error.png')
            raise e
