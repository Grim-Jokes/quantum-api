from ..categorizer import Categorizer


class Input:

    def __init__(self, transactions, categorizer: Categorizer):
        self.transactions = transactions

        self.categorizer = categorizer

    def set_category(self, transaction, categories):

        if not categories:
            return

        options = '\n'.join(
            [
                str(x) for x in categories
            ]
        )

        parent_category_id = int(input(
            f'Select a category for {transaction}:\n{options}\n'
        ))

        detail_cats = self.categorizer.get_child_categories(parent_category_id)

        if not detail_cats:
            transaction.category = self.categorizer.get(parent_category_id)
            transaction.save()
        else:
            self.set_category(transaction, detail_cats)

    def categorize(self):

        for transaction in self.transactions:
            result = self.categorizer.categorize(transaction)

            if not result:
                self.set_category(
                    transaction,
                    self.categorizer.get_root_categories()
                )
