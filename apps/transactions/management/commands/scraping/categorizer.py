from apps.transactions.models import Category, Transaction
from fuzzywuzzy import fuzz


class Categorizer:

    def __init__(self):
        self.categories = Category.objects.all()

        self.transactions = Transaction.objects.all()

    def find_matches(self, transaction):
        matches = [
            (x, fuzz.token_sort_ratio(x.description, transaction.description))
            for x in self.transactions
            if fuzz.token_sort_ratio(
                x.description,
                transaction.description
            ) >= 90
            and x.category
        ]

        return matches

    def process_patches(self, transaction, matches):

        if len(matches) == 1:
            trans, score = matches[0]

            if score >= 95:
                transaction.category = trans.category
                transaction.save()
                return trans.category

    def categorize(self, transaction):
        matches = self.find_matches(transaction)

        return self.process_patches(transaction, matches)
