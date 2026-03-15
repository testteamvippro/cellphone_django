from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Import Services (Business Logic Layer)
from store.services.cart import CartService
from store.services.product import ProductService
from store.services.order import OrderService
from store.services.wishlist import WishlistService
from store.services.news import NewsService

# Import Utilities
from store.utils.helpers import SessionHelper, ValidationHelper

# Import Exceptions
from store.exceptions import (
    CartException, InvalidQuantityException, 
    InsufficientStockException, EmptyCartException, OrderException
)

# Import Models (kept for template context)
from .models import Category, Brand, VideoReview

# Initialize Services
cart_service = CartService()
product_service = ProductService()
order_service = OrderService()
wishlist_service = WishlistService()
news_service = NewsService()



def home(request):
    """
    Homepage with all product categories.
    Uses ProductService for data retrieval.
    Uses CartService for cart management.
    Uses NewsService for news articles.
    """
    # Get user/session identifier
    user, session_key = SessionHelper.get_user_identifier(request)
    
    # Get or create cart
    cart = cart_service.get_or_create_cart(user, session_key)
    
    # Get products using service
    homepage_products = product_service.get_homepage_products()
    
    # Get categories and brands
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Get products by category
    products_by_category = {}
    for category in categories:
        products = product_service.repo.get_by_category(category.slug, limit=4)
        if products:
            products_by_category[category] = products
    
    # Get news and videos
    news_articles = news_service.get_homepage_news(limit=3)
    video_reviews = VideoReview.objects.all()[:3]
    
    context = {
        'flash_sale_products': homepage_products['flash_sale'],
        'new_products': homepage_products['new'],
        'products_by_category': products_by_category,
        'categories': categories,
        'brands': brands,
        'news_articles': news_articles,
        'video_reviews': video_reviews,
        'cart': cart,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    """
    Product listing page with filtering and search.
    Uses ProductService for queries and filtering.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    # Get filters from request
    brand_slug = request.GET.get('brand')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')
    page = request.GET.get('page', 1)
    
    # Get products using service
    products, category = product_service.get_products_by_category(
        category_slug=category_slug or '',
        brand_slug=brand_slug,
        search_query=search_query,
        sort_by=sort_by
    )
    
    # Paginate products
    paginator = Paginator(products, 15)  # 15 items per page
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    # Get filter options
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Price options for sidebar
    price_options = [
        {'value': '', 'label': 'Tất cả'},
        {'value': '0-5', 'label': 'Dưới 5 triệu'},
        {'value': '5-10', 'label': '5-10 triệu'},
        {'value': '10-20', 'label': '10-20 triệu'},
        {'value': '20+', 'label': 'Trên 20 triệu'},
    ]
    
    context = {
        'products': products_page,
        'category': category,
        'categories': categories,
        'brands': brands,
        'cart': cart,
        'search_query': search_query or '',
        'price_options': price_options,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    Product detail page.
    Uses ProductService to get product with all related information.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    # Get product with all details using service
    product_details = product_service.get_product_with_details(slug)
    
    if not product_details:
        return redirect('store:product_list')
    
    # Check if in wishlist
    in_wishlist = wishlist_service.is_in_wishlist(
        product_details['product'], 
        user=user if request.user.is_authenticated else None,
        session_key=session_key
    )
    
    context = {
        'product': product_details['product'],
        'related_products': product_details['related_products'],
        'colors': product_details['colors'],
        'specs': product_details['specs'],
        'cart': cart,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """
    Add product to cart.
    Uses CartService with validation and error handling.
    """
    try:
        product = product_service.get_available_product(product_id)
        if not product:
            return JsonResponse({'success': False, 'error': 'Product not found or not available'}, status=404)
        
        user, session_key = SessionHelper.get_user_identifier(request)
        cart = cart_service.get_or_create_cart(user, session_key)
        
        quantity = int(request.POST.get('quantity', 1))
        cart_item = cart_service.add_to_cart(cart, product, quantity)
        
        cart_totals = cart_service.get_cart_totals(cart)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart_totals['total_items'],
                'message': 'Added to cart successfully'
            })
        
        return redirect('store:cart_view')
    
    except InvalidQuantityException as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except InsufficientStockException as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except CartException as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)


def cart_view(request):
    """
    Shopping cart page.
    Uses CartService to get cart items and totals.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    cart_totals = cart_service.get_cart_totals(cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_totals['items'],
        'total_items': cart_totals['total_items'],
        'total_price': cart_totals['total_price'],
    }
    return render(request, 'store/cart.html', context)


@require_POST
def update_cart(request, item_id):
    """
    Update cart item quantity.
    Uses CartService with validation.
    """
    try:
        user, session_key = SessionHelper.get_user_identifier(request)
        cart = cart_service.get_or_create_cart(user, session_key)
        
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')
        
        if action == 'increase':
            cart_item = cart_service.increase_quantity(cart, item_id)
        elif action == 'decrease':
            cart_item = cart_service.decrease_quantity(cart, item_id)
        else:
            quantity = int(quantity) if quantity else 1
            cart_item = cart_service.update_cart_item(cart, item_id, quantity)
        
        cart_totals = cart_service.get_cart_totals(cart)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart_totals['total_items'],
                'item_subtotal': cart_item.subtotal if cart_item else 0,
                'cart_total_price': cart_totals['total_price']
            })
        
        return redirect('store:cart_view')
    
    except InsufficientStockException as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def remove_from_cart(request, item_id):
    """
    Remove item from cart.
    Uses CartService.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    success = cart_service.remove_from_cart(cart, item_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_totals = cart_service.get_cart_totals(cart)
        return JsonResponse({
            'success': success,
            'cart_total': cart_totals['total_items'],
            'cart_total_price': cart_totals['total_price']
        })
    
    return redirect('store:cart_view')


@require_POST
def toggle_wishlist(request, product_id):
    """
    Add/remove product from wishlist.
    Uses WishlistService with support for both authenticated and anonymous users.
    """
    try:
        product = product_service.get_available_product(product_id)
        if not product:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        
        user, session_key = SessionHelper.get_user_identifier(request)
        
        result = wishlist_service.toggle_wishlist(
            product,
            user=user if request.user.is_authenticated else None,
            session_key=session_key
        )
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def wishlist_view(request):
    """
    Wishlist page.
    Uses WishlistService to get wishlist items.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    wishlist_items = wishlist_service.get_wishlist_products(
        user=user if request.user.is_authenticated else None,
        session_key=session_key
    )
    
    context = {
        'wishlist_items': wishlist_items,
        'cart': cart,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def checkout(request):
    """
    Checkout page with order creation.
    Uses OrderService for order creation and CartService for validation.
    """
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    # Validate cart
    is_valid, message = cart_service.validate_cart_for_checkout(cart)
    if not is_valid:
        messages.error(request, message)
        return redirect('store:cart_view')
    
    if request.method == 'POST':
        try:
            # Validate order data
            order_data = {
                'full_name': request.POST.get('full_name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
                'postal_code': request.POST.get('postal_code'),
            }
            
            is_valid, errors = ValidationHelper.validate_order_data(order_data)
            if not is_valid:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'store/checkout.html', {
                    'cart': cart,
                    'cart_items': cart_service.get_cart_items(cart),
                })
            
            # Create order using service
            order = order_service.create_order(request.user, cart, order_data)
            
            # Clear cart
            cart_service.clear_cart(cart)
            
            messages.success(request, 'Order created successfully!')
            return redirect('store:order_success', order_number=order.order_number)
        
        except EmptyCartException as e:
            messages.error(request, str(e))
            return redirect('store:cart_view')
        except OrderException as e:
            messages.error(request, str(e))
            return redirect('store:cart_view')
        except Exception as e:
            messages.error(request, f"Error creating order: {str(e)}")
            return redirect('store:cart_view')
    
    cart_items = cart_service.get_cart_items(cart)
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_number):
    """
    Order success page.
    Uses OrderService to get order details.
    """
    order = order_service.get_order_by_number(order_number, request.user)
    
    if not order:
        messages.error(request, 'Order not found')
        return redirect('store:home')
    
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    context = {
        'order': order,
        'order_items': order_service.get_order_items(order),
        'cart': cart,
    }
    return render(request, 'store/order_success.html', context)


@login_required
def order_list(request):
    """
    User's order history.
    Uses OrderService to get user orders.
    """
    orders = order_service.get_user_orders(request.user)
    
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    context = {
        'orders': orders,
        'cart': cart,
    }
    return render(request, 'store/order_list.html', context)


def news_list(request):
    """
    News articles listing.
    Uses NewsService to get all articles.
    """
    articles = news_service.get_all_articles()
    
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    context = {
        'articles': articles,
        'cart': cart,
    }
    return render(request, 'store/news_list.html', context)


def news_detail(request, slug):
    """
    News article detail.
    Uses NewsService to get article with related articles.
    """
    article = news_service.get_article(slug)
    
    if not article:
        messages.error(request, 'Article not found')
        return redirect('store:news_list')
    
    related_articles = news_service.get_related_articles(article)
    
    user, session_key = SessionHelper.get_user_identifier(request)
    cart = cart_service.get_or_create_cart(user, session_key)
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'cart': cart,
    }
    return render(request, 'store/news_detail.html', context)

