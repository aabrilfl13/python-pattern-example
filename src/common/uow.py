from django.db import transaction
from cart.interfaces.repositories import CartRepository


class UnitOfWork:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def __enter__(self):
        self.transaction = transaction.atomic()
        self.transaction.__enter__()
        return self

    def __exit__(self, *args):
        self.transaction.__exit__(*args)
