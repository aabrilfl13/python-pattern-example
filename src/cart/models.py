from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField(
        validators=[MinValueValidator(0)], help_text="Number of calories per serving"
    )
    expiration_date = models.DateTimeField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (${self.price})"

    @property
    def is_expired(self):
        from django.utils import timezone

        return self.expiration_date <= timezone.now()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        unique_together = ["cart", "product"]

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart {self.cart.id}"

    @property
    def total(self):
        return self.quantity * self.product.price
