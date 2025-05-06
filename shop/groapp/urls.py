from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from groapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home Page
    path('', views.home, name='home'),
    
    # Product Pages
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # User Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Cart and Checkout
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Order Confirmation
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Product List (Home)
    path('products/', views.product_list, name='product_list'),  # Changed name to avoid conflict with home
    
]
