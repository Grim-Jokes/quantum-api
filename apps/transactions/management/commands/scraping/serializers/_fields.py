from datetime import datetime
from decimal import Decimal, InvalidOperation

import logging

logger = logging.getLogger()


class SerializationError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def fail(self, message):
        logger.error(message)
        raise SerializationError(message)


class DateField(Field):

    def __init__(self, value):
        super().__init__(value)

        self.date = datetime.strptime(self.value, "%b %d, %Y")

    def to_value(self):
        return self.date.strftime("%m/%d/%Y")


class DecimalField(Field):

    def to_value(self):
        try:
            value = Decimal(self.value.replace(',', ''))
            return value
        except InvalidOperation:
            self.fail("Unable to parse value " + self.value)


class CharField(Field):

    def to_value(self):
        return self.value
