from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, OrderItem,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ProductForm
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# from .helpers import Helpers

# Create your views here.

# def index(request):
# 	preview_products = Product.objects.all().order_by('-id')[:12]
	
# 	return render(request, Helpers.get_url('index.html'), {'products': preview_products, 'currency': EcommerceConfig.currency})

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})

def product_list(request, category_id=None):
    categories = Category.objects.filter(parent__isnull=True)  # Top-level categories
    products = Product.objects.all()

    selected_category = None

    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        if selected_category.subcategories.exists():
            subcats = selected_category.subcategories.all()
            products = products.filter(category__in=subcats)
        else:
            products = products.filter(category=selected_category)

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

class MyLoginView(LoginView):
    authentication_form = CustomLoginForm

# def add_to_cart(request, product_id):
#     # Simple cart logic using session or models
#     # Placeholder logic
#     return redirect('cart')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# def cart_view(request):
#     cart_items = []  # Replace with actual cart logic
#     cart_total = sum(item.total for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
# -----------------------


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.total for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })

@login_required
def update_cart_item(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity < 1:
                item.delete()
                return redirect('cart')
        item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    if request.method == 'POST':
        CartItem.objects.filter(user=request.user).delete()
    return redirect('cart')

# @login_required
# def cart_view(request):
#     cart_items = CartItem.objects.filter(user=request.user)
    
#     # original_total = cart_total
#     # # original_total = sum(item.product.original_price * item.quantity for item in cart_items)
#     # cart_total = sum(item.product.price * item.quantity for item in cart_items)
#     # total_discount = original_total - cart_total
#     # cart_count = sum(item.quantity for item in cart_items)
#     # savings = original_total - cart_total

#     cart_total = sum(item.product.price * item.quantity for item in cart_items)
#     original_total = cart_total
#     total_discount = 0
#     savings = 0
#     cart_count = sum(item.quantity for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'original_total': original_total,
#         'cart_total': cart_total,
#         'total_discount': total_discount,
#         'cart_count': cart_count,
#         'savings': savings,
#     }
#     return render(request, 'cart.html', context)

# @login_required
# def update_quantity(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id, user=request.user)
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         if action == 'increase':
#             item.quantity += 1
#         elif action == 'decrease' and item.quantity > 1:
#             item.quantity -= 1
#         item.save()
#     return redirect('cart')

# @login_required
# def remove_from_cart(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id, user=request.user)
#     item.delete()
#     return redirect('cart')

# @login_required
# def clear_cart(request):
#     if request.method == 'POST':
#         CartItem.objects.filter(user=request.user).delete()
#     return redirect('cart')

# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         # Save order logic here
#         return redirect('order_confirmation')
#     return render(request, 'checkout.html')

# def order_confirmation(request):
#     return render(request, 'order_confirmation.html')

@login_required
def order_confirmation(request):
    latest_order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'order_confirmation.html', {'order': latest_order})

@login_required
def order_history(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': user_orders})

# def user_register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('product_list')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        payment_method = request.POST['payment_method']

        # Create Order
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            payment_method=payment_method
        )

        # Move cart items to order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Clear cart
        cart_items.delete()

        return redirect('order_confirmation')

    return render(request, 'checkout.html', {'cart_items': cart_items})

from django import template

register = template.Library()

@register.filter
def order_total(order):
    return sum(item.total for item in order.items.all())

@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect('product_list')  # or show an error message

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # go to login page
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})
