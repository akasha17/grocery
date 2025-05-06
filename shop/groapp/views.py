from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

from django.shortcuts import render, get_object_or_404
from .models import Product

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to homepage or dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

from .forms import SimpleRegisterForm

def register(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SimpleRegisterForm()
    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import CartItem, Order, OrderItem

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect('cart')

    # Calculate total as Decimal
    total = sum(Decimal(item.subtotal()) for item in items)

    if request.method == 'POST':
        full_name   = request.POST['full_name']
        address     = request.POST['address']
        phone       = request.POST['phone_number']

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone_number=phone,
            total_price=total
        )

        # Create OrderItems — **call** discounted_price()
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=Decimal(item.product.discounted_price())  # ← note the ()
            )

        # Clear cart
        items.delete()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })
from django.shortcuts import render, get_object_or_404
from .models import Order

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'order_confirmation.html', {
        'order': order
    })


from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return render(request, 'login.html')  # Redirect to home or any other page


from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
