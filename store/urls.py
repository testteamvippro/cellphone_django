from django.urls import path
from . import views
from . import admin_views

app_name = 'store'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Admin Dashboard (must be before other paths to avoid conflicts)
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<str:order_number>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    
    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
]
