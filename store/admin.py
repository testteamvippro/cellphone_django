from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Category, Brand, Product, ProductColor, ProductSpec,
    Cart, CartItem, Wishlist, Order, OrderItem, NewsArticle, VideoReview
)


# Customize Admin Site Header
admin.site.site_header = "🍓 Dâu Store Admin"
admin.site.site_title = "Dâu Store Admin Portal"
admin.site.index_title = "Welcome to Dâu Store Management"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'product_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    def product_count(self, obj):
        count = obj.products.count()
        url = reverse('admin:store_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} products</a>', url, count)
    product_count.short_description = 'Products'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'logo_preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def product_count(self, obj):
        count = obj.products.count()
        return f'{count} products'
    product_count.short_description = 'Total Products'
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'brand', 'formatted_price', 
                   'stock_status', 'rating', 'is_flash_sale', 'is_available', 'views_count')
    list_filter = ('category', 'brand', 'is_flash_sale', 'is_available', 'created_at')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductColorInline, ProductSpecInline]
    list_editable = ('is_flash_sale', 'is_available')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'discount_percentage', 'image_preview_large')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'brand', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_percentage')
        }),
        ('Specifications', {
            'fields': ('storage', 'ram', 'screen_size', 'processor', 'camera', 'battery')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3', 'image_preview_large')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_available')
        }),
        ('Marketing', {
            'fields': ('is_flash_sale', 'promotion_text', 'installment_offer')
        }),
        ('Ratings & Analytics', {
            'fields': ('rating', 'reviews_count', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_flash_sale', 'remove_flash_sale', 'mark_available', 'mark_unavailable', 'reset_views']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="border-radius: 10px;" />', obj.image.url)
        return 'No image'
    image_preview_large.short_description = 'Preview'
    
    def formatted_price(self, obj):
        return format_html('<strong>₫{:,}</strong>', int(obj.price))
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'
    
    def stock_status(self, obj):
        if obj.stock == 0:
            color = 'red'
            status = 'Out of Stock'
        elif obj.stock < 10:
            color = 'orange'
            status = f'Low Stock ({obj.stock})'
        else:
            color = 'green'
            status = f'In Stock ({obj.stock})'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status.short_description = 'Stock Status'
    stock_status.admin_order_field = 'stock'
    
    def mark_as_flash_sale(self, request, queryset):
        updated = queryset.update(is_flash_sale=True)
        self.message_user(request, f'{updated} products marked as flash sale.')
    mark_as_flash_sale.short_description = '⚡ Mark as Flash Sale'
    
    def remove_flash_sale(self, request, queryset):
        updated = queryset.update(is_flash_sale=False)
        self.message_user(request, f'{updated} products removed from flash sale.')
    remove_flash_sale.short_description = '❌ Remove Flash Sale'
    
    def mark_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} products marked as available.')
    mark_available.short_description = '✅ Mark as Available'
    
    def mark_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} products marked as unavailable.')
    mark_unavailable.short_description = '🚫 Mark as Unavailable'
    
    def reset_views(self, request, queryset):
        updated = queryset.update(views_count=0)
        self.message_user(request, f'Views reset for {updated} products.')
    reset_views.short_description = '🔄 Reset View Count'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user_info', 'item_count', 'total_value', 'last_updated', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'total_price')
    
    actions = ['clean_empty_carts', 'clean_old_carts']
    
    def cart_id(self, obj):
        return f'Cart #{obj.id}'
    cart_id.short_description = 'Cart ID'
    
    def user_info(self, obj):
        if obj.user:
            return format_html('<strong>{}</strong> ({})', obj.user.username, obj.user.email)
        return f'Guest: {obj.session_key[:10]}...'
    user_info.short_description = 'User'
    
    def item_count(self, obj):
        count = obj.items.count()
        if count == 0:
            return format_html('<span style="color: gray;">Empty</span>')
        return format_html('<strong>{}</strong> items', count)
    item_count.short_description = 'Items'
    
    def total_value(self, obj):
        total = obj.total_price
        return format_html('<strong>₫{:,}</strong>', int(total))
    total_value.short_description = 'Total'
    total_value.admin_order_field = 'total_price'
    
    def last_updated(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')
    last_updated.short_description = 'Last Updated'
    last_updated.admin_order_field = 'updated_at'
    
    def clean_empty_carts(self, request, queryset):
        # Delete carts with no items
        empty_carts = queryset.filter(items__isnull=True)
        count = empty_carts.count()
        empty_carts.delete()
        self.message_user(request, f'{count} empty carts deleted.')
    clean_empty_carts.short_description = '🗑️ Delete Empty Carts'
    
    def clean_old_carts(self, request, queryset):
        # Delete carts older than 30 days
        cutoff = timezone.now() - timedelta(days=30)
        old_carts = queryset.filter(updated_at__lt=cutoff)
        count = old_carts.count()
        old_carts.delete()
        self.message_user(request, f'{count} old carts deleted.')
    clean_old_carts.short_description = '🧹 Clean Old Carts (30+ days)'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'product_info', 'product_price', 'added_date')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name', 'session_key')
    readonly_fields = ('added_at',)
    
    def user_info(self, obj):
        if obj.user:
            return obj.user.username
        return f'Guest: {obj.session_key[:10]}...'
    user_info.short_description = 'User'
    
    def product_info(self, obj):
        url = reverse('admin:store_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_info.short_description = 'Product'
    
    def product_price(self, obj):
        return format_html('₫{:,}', int(obj.product.price))
    product_price.short_description = 'Price'
    
    def added_date(self, obj):
        return obj.added_at.strftime('%Y-%m-%d')
    added_date.short_description = 'Added On'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_info', 'status_badge',
                   'total_amount_formatted', 'item_count', 'order_date')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'full_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'postal_code')
        }),
        ('Order Summary', {
            'fields': ('total_amount',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'export_orders']
    
    def user_info(self, obj):
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_info.short_description = 'User'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#1E90FF',
            'shipped': '#9370DB',
            'delivered': '#32CD32',
            'cancelled': '#DC143C'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def total_amount_formatted(self, obj):
        return format_html('<strong>₫{:,}</strong>', int(obj.total_amount))
    total_amount_formatted.short_description = 'Total'
    total_amount_formatted.admin_order_field = 'total_amount'
    
    def item_count(self, obj):
        count = obj.items.count()
        return f'{count} items'
    item_count.short_description = 'Items'
    
    def order_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    order_date.short_description = 'Order Date'
    order_date.admin_order_field = 'created_at'
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = '🔄 Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = '📦 Mark as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = '✅ Mark as Delivered'
    
    def export_orders(self, request, queryset):
        # This is a placeholder - you can implement CSV export
        self.message_user(request, f'Export feature coming soon! Selected {queryset.count()} orders.')
    export_orders.short_description = '📊 Export to CSV'


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category_badge', 'view_count', 'publish_date')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at', 'image_preview')
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'image', 'image_preview')
        }),
        ('Analytics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['reset_views']
    
    def author_name(self, obj):
        if obj.author:
            return obj.author.username
        return '-'
    author_name.short_description = 'Author'
    
    def category_badge(self, obj):
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            obj.category
        )
    category_badge.short_description = 'Category'
    
    def view_count(self, obj):
        return format_html('<strong>{:,}</strong> views', obj.views)
    view_count.short_description = 'Views'
    view_count.admin_order_field = 'views'
    
    def publish_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    publish_date.short_description = 'Published'
    publish_date.admin_order_field = 'created_at'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'
    
    def reset_views(self, request, queryset):
        updated = queryset.update(views=0)
        self.message_user(request, f'Views reset for {updated} articles.')
    reset_views.short_description = '🔄 Reset View Count'


@admin.register(VideoReview)
class VideoReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_link', 'view_count', 'thumbnail_preview', 'created_date')
    list_filter = ('created_at',)
    search_fields = ('title', 'product__name')
    readonly_fields = ('views', 'created_at', 'thumbnail_preview_large')
    
    def product_link(self, obj):
        url = reverse('admin:store_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Product'
    
    def view_count(self, obj):
        return f'{obj.views:,} views'
    view_count.short_description = 'Views'
    view_count.admin_order_field = 'views'
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="80" height="60" style="border-radius: 5px;" />', obj.thumbnail.url)
        return '-'
    thumbnail_preview.short_description = 'Thumbnail'
    
    def thumbnail_preview_large(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="400" style="border-radius: 10px;" />', obj.thumbnail.url)
        return 'No thumbnail'
    thumbnail_preview_large.short_description = 'Preview'
    
    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    created_date.short_description = 'Created'
    created_date.admin_order_field = 'created_at'

