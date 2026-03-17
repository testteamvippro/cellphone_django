from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product, ProductColor, ProductSpec
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample product data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Điện thoại', 'slug': 'phones', 'icon': '📱'},
            {'name': 'Laptop', 'slug': 'laptops', 'icon': '💻'},
            {'name': 'Âm thanh', 'slug': 'audio', 'icon': '🎧'},
            {'name': 'TV', 'slug': 'tv', 'icon': '📺'},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(**cat_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories_data)} categories'))
        
        # Create brands
        self.stdout.write('Creating brands...')
        brands_data = ['Apple', 'Samsung', 'Xiaomi', 'OPPO', 'TECNO', 'HONOR', 
                      'Google', 'OnePlus', 'Motorola', 'ASUS', 'Lenovo', 'MSI',
                      'Acer', 'HP', 'Dell', 'LG', 'Sony', 'JBL', 'Huawei', 'Garmin']
        
        for brand_name in brands_data:
            Brand.objects.get_or_create(name=brand_name, slug=brand_name.lower())
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(brands_data)} brands'))
        
        # Create sample products
        self.stdout.write('Creating products...')
        
        phone_category = Category.objects.get(slug='phones')
        laptop_category = Category.objects.get(slug='laptops')
        watch_category = Category.objects.get(slug='watches')
        audio_category = Category.objects.get(slug='audio')
        tv_category = Category.objects.get(slug='tv')
        
        samsung = Brand.objects.get(slug='samsung')
        apple = Brand.objects.get(slug='apple')
        xiaomi = Brand.objects.get(slug='xiaomi')
        google = Brand.objects.get(slug='google')
        asus = Brand.objects.get(slug='asus')
        huawei = Brand.objects.get(slug='huawei')
        jbl = Brand.objects.get(slug='jbl')
        lg = Brand.objects.get(slug='lg')
        
        products_data = [
            # Phones
            {
                'name': 'Samsung Galaxy S24 Ultra 12GB 256GB',
                'slug': 'samsung-galaxy-s24-ultra-12gb-256gb',
                'category': phone_category,
                'brand': samsung,
                'description': 'Flagship Samsung với camera 200MP, chip Snapdragon 8 Gen 3',
                'price': Decimal('32990000'),
                'original_price': Decimal('36990000'),
                'storage': '256GB',
                'color': 'Titanium Gray',
                'ram': '12GB',
                'screen_size': '6.8 inch',
                'rating': Decimal('4.8'),
                'reviews_count': 245,
                'stock': 50,
                'is_flash_sale': True,
                'promotion_text': 'Giảm thêm 2 triệu khi trả góp 0%',
                'installment_offer': 'Trả góp 0% qua thẻ tín dụng',
            },
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'slug': 'iphone-15-pro-max-256gb',
                'category': phone_category,
                'brand': apple,
                'description': 'iPhone 15 Pro Max với chip A17 Pro, camera 48MP',
                'price': Decimal('34990000'),
                'original_price': Decimal('38990000'),
                'storage': '256GB',
                'color': 'Natural Titanium',
                'ram': '8GB',
                'screen_size': '6.7 inch',
                'rating': Decimal('4.9'),
                'reviews_count': 512,
                'stock': 30,
                'is_flash_sale': True,
                'promotion_text': 'Thu cũ đổi mới lên đến 5 triệu',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'Google Pixel 8 Pro 128GB',
                'slug': 'google-pixel-8-pro-128gb',
                'category': phone_category,
                'brand': google,
                'description': 'Google Pixel 8 Pro với chip Tensor G3, camera AI',
                'price': Decimal('24990000'),
                'original_price': Decimal('27990000'),
                'storage': '128GB',
                'color': 'Obsidian',
                'ram': '12GB',
                'screen_size': '6.7 inch',
                'rating': Decimal('4.7'),
                'reviews_count': 189,
                'stock': 40,
                'is_flash_sale': True,
                'promotion_text': 'Tặng ốp lưng Google chính hãng',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'Xiaomi 14 Ultra 16GB 512GB',
                'slug': 'xiaomi-14-ultra-16gb-512gb',
                'category': phone_category,
                'brand': xiaomi,
                'description': 'Xiaomi 14 Ultra với Leica camera, Snapdragon 8 Gen 3',
                'price': Decimal('28990000'),
                'original_price': Decimal('31990000'),
                'storage': '512GB',
                'color': 'Black',
                'ram': '16GB',
                'screen_size': '6.73 inch',
                'rating': Decimal('4.6'),
                'reviews_count': 156,
                'stock': 25,
                'is_flash_sale': True,
                'promotion_text': 'Giảm 3 triệu + Quà 2 triệu',
                'installment_offer': 'Trả góp 0% qua Home PayLater',
            },
            # Laptops
            {
                'name': 'MacBook Air M3 15 inch 2026 (8-core CPU | 16GB | 512GB)',
                'slug': 'macbook-air-m3-15-2026',
                'category': laptop_category,
                'brand': apple,
                'description': 'MacBook Air M3 mỏng nhẹ, pin 18 giờ',
                'price': Decimal('29990000'),
                'original_price': Decimal('34990000'),
                'storage': '512GB',
                'color': 'Space Gray',
                'ram': '16GB',
                'screen_size': '15 inch',
                'rating': Decimal('5.0'),
                'reviews_count': 89,
                'stock': 20,
                'promotion_text': 'Giảm 5 triệu cho sinh viên',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'ASUS ROG Strix G16 (2026) i9-14900HX RTX 4070',
                'slug': 'asus-rog-strix-g16-2026',
                'category': laptop_category,
                'brand': asus,
                'description': 'Laptop gaming cao cấp, màn hình 240Hz',
                'price': Decimal('45990000'),
                'original_price': Decimal('52990000'),
                'storage': '1TB SSD',
                'color': 'Eclipse Gray',
                'ram': '32GB',
                'screen_size': '16 inch',
                'rating': Decimal('4.8'),
                'reviews_count': 67,
                'stock': 15,
                'promotion_text': 'Tặng chuột gaming + balo',
                'installment_offer': 'Trả góp 0%',
            },
            # Watches
            {
                'name': 'Apple Watch Series 9 GPS 45mm',
                'slug': 'apple-watch-series-9-gps-45mm',
                'category': watch_category,
                'brand': apple,
                'description': 'Apple Watch với S9 chip, Always-On display',
                'price': Decimal('8590000'),
                'original_price': Decimal('9990000'),
                'storage': '',
                'color': 'Midnight',
                'rating': Decimal('4.8'),
                'reviews_count': 234,
                'stock': 50,
                'promotion_text': 'Giảm 1.4 triệu',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'Huawei Watch GT 4 46mm',
                'slug': 'huawei-watch-gt-4-46mm',
                'category': watch_category,
                'brand': huawei,
                'description': 'Đồng hồ thông minh pin 14 ngày',
                'price': Decimal('5340000'),
                'original_price': Decimal('6990000'),
                'color': 'Black',
                'rating': Decimal('4.7'),
                'reviews_count': 156,
                'stock': 40,
                'promotion_text': 'Giảm 1.65 triệu',
                'installment_offer': 'Trả góp 0%',
            },
            # Audio
            {
                'name': 'AirPods Pro 2 USB-C',
                'slug': 'airpods-pro-2-usb-c',
                'category': audio_category,
                'brand': apple,
                'description': 'Tai nghe chống ồn chủ động, chip H2',
                'price': Decimal('5490000'),
                'original_price': Decimal('6490000'),
                'rating': Decimal('4.9'),
                'reviews_count': 456,
                'stock': 100,
                'promotion_text': 'Giảm 1 triệu',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'JBL Flip 6',
                'slug': 'jbl-flip-6',
                'category': audio_category,
                'brand': jbl,
                'description': 'Loa Bluetooth chống nước IP67',
                'price': Decimal('2990000'),
                'original_price': Decimal('3490000'),
                'rating': Decimal('4.7'),
                'reviews_count': 189,
                'stock': 60,
                'promotion_text': 'Giảm 500K',
            },
            # TVs
            {
                'name': 'Samsung Crystal UHD 4K 50 inch UA50DU7000',
                'slug': 'samsung-crystal-uhd-50-inch',
                'category': tv_category,
                'brand': samsung,
                'description': 'Smart TV 4K, Crystal Processor',
                'price': Decimal('8490000'),
                'original_price': Decimal('10990000'),
                'screen_size': '50 inch',
                'rating': Decimal('4.6'),
                'reviews_count': 234,
                'stock': 20,
                'promotion_text': 'Giảm 2.5 triệu',
                'installment_offer': 'Trả góp 0%',
            },
            {
                'name': 'LG Smart TV 4K 55 inch 55UR8050PSB',
                'slug': 'lg-smart-tv-55-inch',
                'category': tv_category,
                'brand': lg,
                'description': 'Smart TV 4K với webOS, ThinQ AI',
                'price': Decimal('10990000'),
                'original_price': Decimal('13990000'),
                'screen_size': '55 inch',
                'rating': Decimal('4.7'),
                'reviews_count': 178,
                'stock': 15,
                'promotion_text': 'Giảm 3 triệu',
                'installment_offer': 'Trả góp 0%',
            },
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
        
        # Generate 100 phone products for display
        self.stdout.write('Generating 100 phone products...')
        phone_brands = [samsung, apple, xiaomi, google]
        phone_models = {
            'samsung': ['Galaxy S24', 'Galaxy S24+', 'Galaxy S24 Ultra', 'Galaxy A55', 'Galaxy A35', 'Galaxy Z Fold', 'Galaxy Z Flip'],
            'apple': ['iPhone 15', 'iPhone 15 Plus', 'iPhone 15 Pro', 'iPhone 15 Pro Max'],
            'xiaomi': ['14', '14 Ultra', '14 Civi', '13', '13 Ultra', 'Redmi Note 14', 'Redmi 14'],
            'google': ['Pixel 8', 'Pixel 8 Pro', 'Pixel 8a', 'Pixel Fold'],
        }
        storages = ['128GB', '256GB', '512GB', '1TB']
        colors = ['Black', 'White', 'Silver', 'Gold', 'Blue', 'Red', 'Green', 'Purple', 'Pink']
        rams = ['8GB', '12GB', '16GB', '24GB']
        screens = ['6.1 inch', '6.3 inch', '6.5 inch', '6.7 inch', '6.8 inch', '7.0 inch']
        
        phone_count = 0
        for i in range(100):
            brand = phone_brands[i % len(phone_brands)]
            brand_slug = brand.slug.lower()
            model = phone_models.get(brand_slug, ['Phone'])[i % len(phone_models.get(brand_slug, ['Phone']))]
            storage = storages[i % len(storages)]
            color = colors[i % len(colors)]
            ram = rams[i % len(rams)]
            screen = screens[i % len(screens)]
            
            # Calculate prices
            base_price = Decimal('12990000') + (i % 30) * Decimal('1000000')
            original_price = base_price + Decimal('3000000')
            
            slug = f'{brand_slug}-{model.lower().replace(" ", "-")}-{storage.lower()}-{i}'.replace('+', 'plus')
            product_name = f'{brand.name} {model} {storage} {ram}'
            
            is_flash_sale = (i % 3) == 0
            
            product_data = {
                'name': product_name,
                'slug': slug,
                'category': phone_category,
                'brand': brand,
                'description': f'{brand.name} {model} với camera 48MP, pin 5000mAh, chip flagship mạnh mẽ',
                'price': base_price,
                'original_price': original_price,
                'storage': storage,
                'color': color,
                'ram': ram,
                'screen_size': screen,
                'rating': Decimal('4') + Decimal(str(i % 10)) / Decimal('10'),
                'reviews_count': 50 + (i % 500),
                'stock': 10 + (i % 90),
                'is_flash_sale': is_flash_sale,
                'promotion_text': 'Trả góp 0% qua thẻ' if i % 2 == 0 else 'Thu cũ đổi mới',
                'installment_offer': 'Trả góp 0% lên đến 12 tháng',
            }
            
            Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            
            # Get the product
            product = Product.objects.get(slug=product_data['slug'])
            
            # Add colors to the product
            color_options = ['Black', 'Silver', 'Gold', 'Blue', 'Red', 'Green', 'Purple']
            color_hex_map = {
                'Black': '#000000', 'Silver': '#C0C0C0', 'Gold': '#FFD700',
                'Blue': '#0000FF', 'Red': '#FF0000', 'Green': '#00AA00', 'Purple': '#9932CC'
            }
            for color_opt in color_options[:3]:  # Add 3 colors per product
                ProductColor.objects.get_or_create(
                    product=product,
                    color_name=color_opt,
                    defaults={'color_hex': color_hex_map.get(color_opt, '#000000')}
                )
            
            # Add specs to the product
            specs_data = [
                ('Bộ nhớ', storage, 1),
                ('RAM', ram, 2),
                ('Màn hình', screen, 3),
                ('Dung lượng pin', '5000mAh', 4),
                ('Camera sau', '48MP f/1.8', 5),
                ('Camera trước', '20MP f/2.2', 6),
                ('Kết nối', '5G, WiFi 6, Bluetooth 5.3', 7),
                ('Hệ điều hành', 'Android 14', 8),
            ]
            for spec_name, spec_value, order in specs_data:
                ProductSpec.objects.get_or_create(
                    product=product,
                    spec_name=spec_name,
                    defaults={'spec_value': spec_value, 'order': order}
                )
            
            phone_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(products_data)} initial products'))
        self.stdout.write(self.style.SUCCESS(f'Generated {phone_count} phone products'))
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
