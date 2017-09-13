from ..serializers import ChequingSerializer
from ._base import Action
from ..errors import NoRowsException

import logging

logger = logging.getLogger()


class LoginAction(Action):
    def execute(self):
        button_css = "ui-button.ember-view.primary.ui-size-medium.ui-display-default.ui-button.ui-trailing-icon"
        button = self.session.at_css(button_css)
        button.click()


class WaitAction(Action):
    def __wait_for_loading(self):
        """If the indicator is gone, it means the data should be loaded"""
        loading = self.session.at_css("div.ui-indicator")

        return loading is None

    def execute(self):
        logger.info("Waiting")
        self.session.wait_for(self.__wait_for_loading, timeout=20)


class DetailAction(Action):

    def execute(self):
        logger.info("Clicking detail link")
        link = self.session.css("div.type a")[1]
        link.click()
        


class SelectMonthAction(Action):

    def execute(self):
        logger.info('Selecting radio button')
        buttons = self.session.css("ui-radiobutton")
        if not buttons:
            logger.error('.ui-radiobutton element not found')
            self.session.render('error.png')
        buttons[1].click()


class SubmitAction(Action):

    def __init__(self, session, selector):
        super().__init__(session)

        self.selector = selector

    def execute(self):
        logger.info('Hitting submit button')
        submit_button = self.session.at_css(self.selector)
        submit_button.click()


class ParseAction(Action):

    def execute(self):
        logger.info("Parsing results")

        results = self.session.at_css(
            'section.ember-view.transaction-list.row'
        )

        expenses, income = [], []
        if results.is_visible():
            cells = self.session.css("td")

            counts = int(len(cells) / 5)

            for index in range(1, counts + 1):
                offset = index * 5

                row = ChequingSerializer(cells[offset - 5:offset]).to_value()
                value = row[1]
                if value > 0:
                    income.append(row)
                else:
                    expenses.append(row)

            return expenses, income
        else:
            raise NoRowsException('No rows found')
