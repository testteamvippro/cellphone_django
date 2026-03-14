"""
Admin dashboard views for store management
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from store.models import Product, Order, Cart, Wishlist, NewsArticle
from decimal import Decimal


@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard with statistics and analytics
    """
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Product Statistics
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True).count()
    flash_sale_products = Product.objects.filter(is_flash_sale=True).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__lt=10, stock__gt=0).count()
    
    # Order Statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    
    # Recent orders (last 7 days)
    recent_orders = Order.objects.filter(created_at__gte=week_ago).count()
    
    # Revenue Statistics
    total_revenue = Order.objects.filter(
        status__in=['delivered', 'shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    weekly_revenue = Order.objects.filter(
        created_at__gte=week_ago,
        status__in=['delivered', 'shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    monthly_revenue = Order.objects.filter(
        created_at__gte=month_ago,
        status__in=['delivered', 'shipped']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    # Average order value
    avg_order_value = Order.objects.filter(
        status__in=['delivered', 'shipped']
    ).aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0')
    
    # Cart Statistics
    active_carts = Cart.objects.filter(items__isnull=False).distinct().count()
    abandoned_carts = Cart.objects.filter(
        updated_at__lt=week_ago,
        items__isnull=False
    ).distinct().count()
    
    # Wishlist Statistics
    total_wishlist_items = Wishlist.objects.count()
    
    # Popular Products (by views)
    popular_products = Product.objects.order_by('-views_count')[:5]
    
    # Recent Orders
    latest_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Low Stock Products
    low_stock_products = Product.objects.filter(
        stock__lt=10, 
        is_available=True
    ).order_by('stock')[:10]
    
    # Best Selling Products (by order items)
    from store.models import OrderItem
    best_selling = OrderItem.objects.values(
        'product__id', 'product__name', 'product__image'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    # News Statistics
    total_articles = NewsArticle.objects.count()
    recent_articles = NewsArticle.objects.filter(created_at__gte=week_ago).count()
    
    # Top Categories by Sales
    from store.models import Category
    top_categories = Category.objects.annotate(
        product_count=Count('products'),
        total_sales=Count('products__orderitem')
    ).order_by('-total_sales')[:5]
    
    context = {
        # Products
        'total_products': total_products,
        'available_products': available_products,
        'flash_sale_products': flash_sale_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        
        # Orders
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'recent_orders_count': recent_orders,
        
        # Revenue
        'total_revenue': total_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'avg_order_value': avg_order_value,
        
        # Carts
        'active_carts': active_carts,
        'abandoned_carts': abandoned_carts,
        
        # Wishlist
        'total_wishlist_items': total_wishlist_items,
        
        # Lists
        'popular_products': popular_products,
        'latest_orders': latest_orders,
        'low_stock_products': low_stock_products,
        'best_selling': best_selling,
        
        # News
        'total_articles': total_articles,
        'recent_articles': recent_articles,
        
        # Categories
        'top_categories': top_categories,
    }
    
    return render(request, 'admin/store_dashboard.html', context)
