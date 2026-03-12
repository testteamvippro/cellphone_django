from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import (
    Product, Category, Brand, Cart, CartItem, 
    Wishlist, Order, OrderItem, NewsArticle, VideoReview
)
import uuid


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def home(request):
    """Homepage with all product categories"""
    # Flash sale products
    flash_sale_products = Product.objects.filter(is_flash_sale=True, is_available=True)[:8]
    
    # New products
    new_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    # Products by category
    categories = Category.objects.all()
    products_by_category = {}
    for category in categories:
        products = Product.objects.filter(category=category, is_available=True)[:4]
        if products:
            products_by_category[category] = products
    
    # Brands
    brands = Brand.objects.all()
    
    # News articles
    news_articles = NewsArticle.objects.all().order_by('-published_date')[:3]
    
    # Video reviews
    video_reviews = VideoReview.objects.all()[:3]
    
    # Cart info
    cart = get_or_create_cart(request)
    
    context = {
        'flash_sale_products': flash_sale_products,
        'new_products': new_products,
        'products_by_category': products_by_category,
        'categories': categories,
        'brands': brands,
        'news_articles': news_articles,
        'video_reviews': video_reviews,
        'cart': cart,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    """Product listing page"""
    products = Product.objects.filter(is_available=True)
    category = None
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Filter by brand
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    cart = get_or_create_cart(request)
    
    context = {
        'products': products,
        'category': category,
        'categories': categories,
        'brands': brands,
        'cart': cart,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug)
    product.views_count += 1
    product.save()
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    # Get colors and specs
    colors = product.colors.all()
    specs = product.specs.all()
    
    cart = get_or_create_cart(request)
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'colors': colors,
        'specs': specs,
        'cart': cart,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'message': 'Đã thêm vào giỏ hàng'
        })
    
    return redirect('store:cart_view')


def cart_view(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    action = request.POST.get('action')
    quantity = int(request.POST.get('quantity', cart_item.quantity))
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            return redirect('store:cart_view')
    elif quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
        return redirect('store:cart_view')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'item_subtotal': cart_item.subtotal if hasattr(cart_item, 'id') else 0,
            'cart_total_price': cart.total_price
        })
    
    return redirect('store:cart_view')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'cart_total_price': cart.total_price
        })
    
    return redirect('store:cart_view')


@require_POST
def toggle_wishlist(request, product_id):
    """Add/remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            wishlist_item.delete()
            added = False
        else:
            added = True
    else:
        # For non-authenticated users, use session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            session_key=session_key,
            product=product
        )
        
        if not created:
            wishlist_item.delete()
            added = False
        else:
            added = True
    
    return JsonResponse({
        'success': True,
        'in_wishlist': added,
        'added': added,
        'message': 'Đã thêm vào yêu thích' if added else 'Đã xóa khỏi yêu thích'
    })


def wishlist_view(request):
    """Wishlist page"""
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        if request.session.session_key:
            wishlist_items = Wishlist.objects.filter(session_key=request.session.session_key)
        else:
            wishlist_items = []
    
    cart = get_or_create_cart(request)
    
    context = {
        'wishlist_items': wishlist_items,
        'cart': cart,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        return redirect('store:cart_view')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            total_amount=cart.total_price,
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('store:order_success', order_number=order.order_number)
    
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_number):
    """Order success page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    cart = get_or_create_cart(request)
    
    context = {
        'order': order,
        'cart': cart,
    }
    return render(request, 'store/order_success.html', context)


@login_required
def order_list(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user)
    cart = get_or_create_cart(request)
    
    context = {
        'orders': orders,
        'cart': cart,
    }
    return render(request, 'store/order_list.html', context)


def news_list(request):
    """News articles listing"""
    articles = NewsArticle.objects.all()
    cart = get_or_create_cart(request)
    
    context = {
        'articles': articles,
        'cart': cart,
    }
    return render(request, 'store/news_list.html', context)


def news_detail(request, slug):
    """News article detail"""
    article = get_object_or_404(NewsArticle, slug=slug)
    article.views += 1
    article.save()
    
    # Related articles
    related_articles = NewsArticle.objects.exclude(id=article.id)[:3]
    
    cart = get_or_create_cart(request)
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'cart': cart,
    }
    return render(request, 'store/news_detail.html', context)

