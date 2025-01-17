from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('cart', views.cart, name='cart'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('premium/', views.premium, name='premium'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_from_order/<int:product_id>/', views.remove_from_order, name='remove_from_order'),
    path('place_order/', views.place_order, name='place_order'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('search/', views.search_results, name='search_results'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('privacy/', views.privacy, name='privacy'),
    path('shipping/', views.shipping, name='shipping'),
    path('return_policy/', views.return_policy, name='return_policy'),
    path('payments/', views.payments, name='payments'),
]
