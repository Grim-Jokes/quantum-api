from ._fields import DateField, DecimalField, CharField


class ChequingSerializer:
    def __init__(self, cells):
        self.date = DateField(cells[0].text())

        value = '-' + \
            cells[2].text().strip('$') if cells[2].text(
            ) else cells[3].text().strip('$')
        self.value = DecimalField(value)

        self.description = CharField(cells[1].text())

        self.fields = [
            self.date,
            self.value,
            self.description
        ]

    def to_value(self):
        return [x.to_value() for x in self.fields]
