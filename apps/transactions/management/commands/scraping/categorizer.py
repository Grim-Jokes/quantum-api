from apps.transactions.models import Category, Transaction
from fuzzywuzzy import fuzz


class Categorizer:

    def __init__(self):
        self.categories = Category.objects.all()

        self.transactions = Transaction.objects.all()

    def get_root_categories(self):
        return self.categories.filter(
            parent_category=None
        )

    def get(self, pk):
        return self.categories.get(pk=pk)

    def get_child_categories(self, parent_category):
        return self.categories.filter(parent_category_id=parent_category)

    def find_matches(self, transaction):
        matches = [
            (x, fuzz.token_sort_ratio(x.description, transaction.description))
            for x in self.transactions
            if fuzz.token_sort_ratio(x.description, transaction.description) >= 90
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

            raise NotImplementedError()
        elif len(matches) > 1:
            categories = list(set([x.category for (x, s) in matches]))

            if len(categories) == 1:
                transaction.category = categories[0]
                transaction.save()
                return categories[0]

    def categorize(self, transaction):
        matches = self.find_matches(transaction)

        return self.process_patches(transaction, matches)
