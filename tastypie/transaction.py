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

    def __init__(self, using=None, *args, **kwargs):
        super(DjangoTransaction, self).__init__(*args, **kwargs)

        self.using = using

    def start(self):
        transaction.enter_transaction_management(using=self.using)
        transaction.managed(True, using=self.using)

    def commit(self):
        try:
            if transaction.is_dirty(using=self.using):
                try:
                    transaction.commit(using=self.using)
                except:
                    transaction.rollback(using=self.using)
                    raise
        finally:
            transaction.leave_transaction_management(using=self.using)

    def rollback(self):
        try:
            if transaction.is_dirty(using=self.using):
                transaction.rollback(using=self.using)
        finally:
            transaction.leave_transaction_management(using=self.using)
