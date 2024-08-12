from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Product
from decimal import Decimal


password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'
password_validator = RegexValidator(
    regex=password_regex,
    message = 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one number',
)

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')    
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        try:
            password_validator(password)
        except ValidationError as e:
            error = "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one number"
            return render(request, 'register.html', {'error': error})
        
        if CustomUser.objects.filter(email=email).exists():
            error = "Email already exists"
            return render(request, 'register.html', {'error': error})

        user = CustomUser.objects.create_user(username=username, name=name, email=email, mobile=mobile, password=password, profile_image=profile_image)
        user.save()
        return redirect('login')

    else:
        return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            error = "User not registered. Please sign up first."
            return render(request, 'login.html', {'error': error})

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Invalid email or password"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

@login_required
def orders(request):
    return render(request, 'orders.html')

@login_required
def premium(request):
    return render(request, 'premium.html')

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        profile_image = request.FILES.get('profile_image')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        user = request.user

        user.name = name
        user.mobile = mobile
        user.profile_image = profile_image
        user.address = address
        user.city = city
        user.state = state
        user.save()
        return redirect('user_profile')
    return render(request, 'edit_profile.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.cart.add(product)
    return redirect('cart')

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.cart.add(product)
    return redirect('place_order')

@login_required
@never_cache
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.cart.remove(product)
    return redirect('cart')

@login_required
@never_cache
def remove_from_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.cart.remove(product)
    return redirect('place_order')

@login_required
@never_cache
def cart(request):
    cart_items = request.user.cart.all()
    total_price = sum([item.price for item in cart_items])
    
    discount = Decimal(0)
    if total_price >= Decimal('1000.00'):
        discount = total_price * Decimal('0.20')
    
    discount = round(discount, 2)
    final_price = round(total_price - discount, 2)

    delivery_charge = Decimal('50.00')
    if total_price >= Decimal('1000.00'):
        delivery_charge = Decimal('0.00')

    final_price += delivery_charge
    final_price = round(final_price, 2)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount': discount,
        'delivery_charge': delivery_charge,
        'final_price': final_price
    }
    return render(request, 'cart.html', context)

@login_required
@never_cache
def place_order(request):
    user = request.user
    cart_items = user.cart.all()
    total_price = sum([item.price for item in cart_items])

    discount = Decimal(0)
    if total_price >= Decimal('1000.00'):
        discount = total_price * Decimal('0.20')
    
    discount = round(discount, 2)
    final_price = round(total_price - discount, 2)

    delivery_charge = Decimal('50.00')
    if total_price >= Decimal('1000.00'):
        delivery_charge = Decimal('0.00')

    final_price += delivery_charge
    final_price = round(final_price, 2)

    context = {
        'user' : user,
        'cart_items': cart_items,
        'total_price': total_price,
        'final_price': final_price,
        'discount' : discount,
        'delivery_charge': delivery_charge,
    }
    return render(request, 'place_order.html', context)

def search_results(request):
    query = request.GET.get('query', '')
    if query:
        results = Product.objects.filter(name__icontains=query)  # Adjust this filter based on your needs
    else:
        results = Product.objects.all()
    return render(request, 'search_results.html', {'results': results, 'query': query})

def aboutus(request):
    return render(request, 'aboutus.html')

def privacy(request):
    return render(request, 'privacy.html')

def shipping(request):
    return render(request, 'shipping.html')

def return_policy(request):
    return render(request, 'return.html')

def payments(request):
    return render(request, 'payments.html')