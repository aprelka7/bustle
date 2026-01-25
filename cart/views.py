from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.contrib import messages
from django.db import transaction
from main.models import Dish
from .models import Cart, CartItem
from .forms import AddToCartForm
import json


class CartMixin:
    def get_cart(self, request):
        if hasattr(request, 'cart'):
            return request.cart
        if not request.session.session_key:
            request.session.create()


        cart, created = Cart.objects.get_or_create(
            session_key = request.session_key
        )

        request.session['cart_id'] = cart.id
        request.session.modified = True
        return cart

class CartModalView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'dish',
            ).order_by('-added_at')
        }
        return TemplateResponse(request, 'cart/cart_modal.html', context)

class AddToCartView(CartMixin, View):
    @transaction.atomic
    def post(self, request, slug):
        cart = self.get_cart(request)
        dish = get_object_or_404(Dish, slug=slug)

        form = AddToCartForm(request.POST, dish=dish)

        if not form.is_valid():
            return JsonResponse({
                'error': 'Invalid form data',
                'errors': form.error
            }, status=400)
        
        quantity = form.cleaned_data['quantity']
        existing_item = cart.items.filter(
            dish=dish,
        ).first()

        if existing_item:
            total_quantity = existing_item.quantity + quantity
        
        cart_item = cart.add_dish(dish, quantity)

        request.session['cart_id'] = cart.id
        request.session.modified = True

        if request.headers.get('HX-Request'):
            return redirect('cart:cart_modal')
        else:
            return JsonResponse({
                'success': True,
                'total_items': cart.total_items,
                'message': f"{dish.name} добавлено в корзину",
                'cart_item_id': cart_item.id,
            })
class UpdateCartItemView(CartMixin, View):
    @transaction.atomic
    def post(self, request, item_id):
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        quantity = int(request.POST.get('quantity', 1))

        if quantity < 0:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        
        if quantity == 0:
            cart_item.delete()

        else:
            cart_item.quantity = quantity
            cart_item.save()

        request.session['cart_id'] = cart.id
        request.session.modified = True

        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'dish',
            ).order_by('-added_at')
        }
        return TemplateResponse(request, 'cart/cart_modal.html', context)
    

class RemoveCartItemView(CartMixin, View):
    def post(self, request, item_id):
        cart = self.get_cart(request)

        try:
            cart_item = cart.items.get(id=item_id)
            cart_item.delete()

            request.session['cart_id'] = cart.id
            request.session.modified = True

            context = {
                'cart': cart,
                'cart_items': cart.items.select_related(
                    'dish',
                ).order_by('-added_at')
            }
            return TemplateResponse(request, 'cart/cart_modal.html', context)
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=400)
        
class CartCountView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        return JsonResponse({
            'total_items': cart.total_items,
            'subtotal': float(cart.subtotal),
        })

class ClearCartView(CartMixin, View):
    def post(self, request):
        cart = self.get_cart(request)
        cart.clear()

        request.session['cart_id'] = cart.id
        request.session.modified = True

        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'cart/cart_empty.html', {
                'cart': cart
            })
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
        })
    
class CartSummaryView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'dish',
            ).order_by('-added_at')
        }
        return TemplateResponse(request, 'cart/cart_summary.html', context)