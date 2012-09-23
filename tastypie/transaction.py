from django.db import transaction


class Transaction(object):
    """
    Transaction is a simple context manager that just calls entering and exiting
    upon entering/exiting a transaction block.
    """

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def start(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError


class DummyTransaction(Transaction):
    """
    A Dummy Transaction class that does no transaction management.
    """

    def start(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class DjangoTransaction(Transaction):
    """
    A Django ORM specific transaction management class that utilizes Django's
    database transaction system.
    """

    def start(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

    def commit(self):
        try:
            if transaction.is_dirty():
                try:
                    transaction.commit()
                except:
                    transaction.rollback()
                    raise
        finally:
            transaction.leave_transaction_management()

    def rollback(self):
        try:
            if transaction.is_dirty():
                transaction.rollback()
        finally:
            transaction.leave_transaction_management()
