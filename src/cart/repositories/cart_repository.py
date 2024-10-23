from django.db import transaction
from cart.interfaces.repositories import CartRepository, ProductRepository
from cart.domain.aggregates import Cart
from cart.adapters.orm import CartModel, CartItemModel, ProductModel
from typing import Optional, List
from cart.domain.entities import Product


from django.utils import timezone


class DjangoCartRepository(CartRepository):
    def get(self, cart_id: int) -> Optional[Cart]:
        try:
            cart_model = CartModel.objects.get(id=cart_id)
            cart = Cart(cart_model.id, cart_model.user_id)

            for item_model in cart_model.items.all():
                product = item_model.product
                cart.add_item(
                    Product(
                        id=product.id,
                        name=product.name,
                        calories=product.calories,
                        expiration_date=product.expiration_date,
                        price=product.price,
                    ),
                    item_model.quantity,
                )
            return cart
        except CartModel.DoesNotExist:
            return None

    def save(self, cart: Cart) -> None:
        with transaction.atomic():
            cart_model = CartModel.objects.get(id=cart.id)
            cart_model.items.all().delete()

            for item in cart.items.values():
                CartItemModel.objects.create(
                    cart=cart_model, product_id=item.product.id, quantity=item.quantity
                )


class DjangoProductRepository(ProductRepository):
    def _to_domain(self, model: ProductModel) -> Product:
        """Convert Django model to domain entity"""
        return Product(
            id=model.id,
            name=model.name,
            calories=model.calories,
            expiration_date=model.expiration_date,
            price=float(model.price),  # Convert Decimal to float for domain entity
        )

    def get(self, product_id: int) -> Optional[Product]:
        try:
            product = ProductModel.objects.get(id=product_id)
            return self._to_domain(product)
        except ProductModel.DoesNotExist:
            return None

    def list(self) -> List[Product]:
        products = ProductModel.objects.all().order_by("name")
        return [self._to_domain(p) for p in products]

    def list_available(self) -> List[Product]:
        now = timezone.now()
        products = ProductModel.objects.filter(expiration_date__gt=now).order_by("name")
        return [self._to_domain(p) for p in products]

    def list_by_ids(self, product_ids: List[int]) -> List[Product]:
        products = ProductModel.objects.filter(id__in=product_ids).order_by("name")
        return [self._to_domain(p) for p in products]

    def search(self, query: str) -> List[Product]:
        products = ProductModel.objects.filter(Q(name__icontains=query)).order_by(
            "name"
        )
        return [self._to_domain(p) for p in products]

    def get_expired_products(self) -> List[Product]:
        now = timezone.now()
        products = ProductModel.objects.filter(expiration_date__lte=now).order_by(
            "expiration_date"
        )
        return [self._to_domain(p) for p in products]
