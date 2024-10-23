# src/cart/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_display", "calories", "expiration_date")
    list_filter = ("expiration_date",)
    search_fields = ("name",)
    ordering = ("name",)

    def price_display(self, obj):
        return f"${obj.price:.2f}"

    price_display.short_description = "Price"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    raw_id_fields = ("product",)
    fields = ("product", "quantity", "get_price", "get_total")
    readonly_fields = ("get_price", "get_total")

    def get_price(self, obj):
        if obj.product:
            return f"${obj.product.price:.2f}"
        return "-"

    get_price.short_description = "Unit Price"

    def get_total(self, obj):
        if obj.product:
            total = obj.product.price * obj.quantity
            return f"${total:.2f}"
        return "-"

    get_total.short_description = "Total"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        # "items_count",
        # "total_amount",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]
    date_hierarchy = "created_at"

    # def items_count(self, obj):
    #     return obj.items.count()

    # items_count.short_description = "Number of Items"

    # def total_amount(self, obj):
    #     total = sum(item.quantity * item.product.price for item in obj.items.all())
    #     return format_html(
    #         '<span style="color: {};">${:.2f}</span>',
    #         "green" if total > 0 else "grey",
    #         total,
    #     )

    # total_amount.short_description = "Total Amount"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items", "items__product")


# Optional: Register CartItem separately if you want to manage them independently
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "item_total")
    list_filter = ("cart__user",)
    search_fields = ("cart__user__username", "product__name")
    raw_id_fields = ("cart", "product")

    def item_total(self, obj):
        total = obj.quantity * obj.product.price
        return f"${total:.2f}"

    item_total.short_description = "Total"
