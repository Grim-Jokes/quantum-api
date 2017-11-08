from ..serializers import ChequingSerializer
from ._base import Action
from ..errors import NoRowsException

import logging

logger = logging.getLogger()


class ShowLoginModal(Action):
    def execute(self):
        button_css = 'button.dropdown-button.open-solid-red'
        button = self.session.at_css(button_css)
        button.click()


class LoginAction(Action):
    def execute(self):
        button_css = "button[type='submit']"
        button = self.session.at_css(button_css)
        button.click()


class WaitAction(Action):
    def __init__(self, session, selector='div.ui-indicator'):
        self.selector = selector
        super().__init__(session)

    def __wait_for_loading(self):
        """If the indicator is gone, it means the data should be loaded"""
        loading = self.session.at_css(self.selector)

        return loading is None

    def execute(self):
        logger.info("Waiting")
        self.session.wait_for(self.__wait_for_loading, timeout=20)


class ClickDetailAction(Action):

    def execute(self):
        logger.info("Clicking detail link")
        link = self.session.at_css("tbody tr:nth-child(2) div.type a", 5)
        link.click()


class SelectMonthButtonAction(Action):

    def execute(self):
        logger.info('Selecting radio button')
        button_class = (
            '.month ui-radiobutton.ember-view.ui-radiobutton'
            '.ui-display-default'
        )
        button = self.session.at_css(button_class)
        button.click()


class SelectMonthAction(Action):

    def __init__(self, session, month):
        self.month = month
        super().__init__(session)

    def execute(self):
        logger.info(f'Selecting month {self.month}')
        dropdown_select = '.month select.ember-view.ember-select'
        dropdown = self.session.css(dropdown_select)[0]
        dropdown.set(self.month)
        dropdown.select_option()


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
