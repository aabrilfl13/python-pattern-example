from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CartSerializer
from cart.services.cart_service import CartService
from cart.repositories import cart_repository


class CartViewSet(viewsets.ViewSet):
    # permission to everyone
    permission_classes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_service = CartService(
            cart_repository.DjangoCartRepository(),
            cart_repository.DjangoProductRepository(),
        )

    def retrieve(self, request, pk=None):
        cart = self.cart_service.cart_repository.get(pk)
        if not cart:
            return Response(status=404)
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        self.cart_service.add_to_cart(pk, product_id, quantity)
        cart = self.cart_service.cart_repository.get(pk)
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=["post"])
    def update_quantity(self, request, pk=None):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        self.cart_service.update_quantity(pk, product_id, quantity)
        cart = self.cart_service.cart_repository.get(pk)
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=["post"])
    def remove_item(self, request, pk=None):
        product_id = request.data.get("product_id")

        self.cart_service.remove_from_cart(pk, product_id)
        cart = self.cart_service.cart_repository.get(pk)
        return Response(CartSerializer(cart).data)
