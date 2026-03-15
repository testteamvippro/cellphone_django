"""
Management command to add modern news articles about tech products
"""
from django.core.management.base import BaseCommand
from store.models import NewsArticle

class Command(BaseCommand):
    help = 'Add comprehensive tech news articles'

    def handle(self, *args, **options):
        self.stdout.write('Adding tech news articles...\n')
        
        news_data = [
            {
                'title': 'iPhone 15 Pro Max Review: Is It Worth The Upgrade?',
                'slug': 'iphone-15-pro-max-review',
                'description': 'Apple\'s latest flagship brings significant improvements. We dive deep into the features, performance, and camera quality that make the iPhone 15 Pro Max a top choice for power users.',
                'content': '''# iPhone 15 Pro Max In-Depth Review

The iPhone 15 Pro Max represents Apple's finest engineering to date. With its advanced titanium design, enhanced A17 Pro chip, and revolutionary camera system, this device sets new standards in the smartphone industry.

## Key Features:
- **Display**: 6.7-inch Super Retina XDR with 120Hz refresh rate
- **Camera**: Triple camera system with advanced computational photography
- **Performance**: A17 Pro chip with 8-core CPU
- **Battery**: Extended battery life up to 30+ hours
- **Design**: Premium titanium construction

## Performance:
The A17 Pro chip delivers exceptional performance for gaming, video editing, and professional applications. Multitasking is seamless even with demanding apps.

## Camera Quality:
The camera system excels in all lighting conditions. Night mode produces stunning results, and the new zoom capabilities rival professional cameras.

## Verdict:
If you want Apple's absolute best, the iPhone 15 Pro Max is worth every penny. The upgrades are meaningful and the device justifies its premium price tag.

**Rating: 9.5/10**'''
            },
            {
                'title': 'Best Gaming Phones 2026: Top Picks For Mobile Gamers',
                'slug': 'best-gaming-phones-2026',
                'description': 'Looking for the ultimate gaming phone? We\'ve tested the fastest phones with the best cooling systems, highest refresh rates, and most powerful processors.',
                'content': '''# Best Gaming Phones of 2026

Mobile gaming has reached new heights. Here are the phones that deliver the best gaming experience.

## Top Gaming Phones:

### 1. iPhone 15 Pro Max
- 120Hz display
- A17 Pro chip with GPU
- Advanced cooling system
- Score: 850,000+ on AnTuTu

### 2. Samsung Galaxy S24 Ultra
- 120Hz AMOLED display
- Snapdragon 8 Gen 3 Leading Version
- Vapor chamber cooling
- Score: 840,000+ on AnTuTu

### 3. OnePlus 12S
- 144Hz display
- Latest Snapdragon processor
- SuperVOOC charging
- Excellent thermal management

### 4. ROG Phone 8
- Gaming-focused design
- High refresh rate display
- Powerful cooling system
- Customizable RGB lighting

## Features You Need:
- **High Refresh Rate**: Minimum 120Hz, 144Hz preferred
- **Processing Power**: Latest flagship processor
- **Cooling System**: Vapor chamber or liquid cooling
- **Display**: AMOLED with good color accuracy
- **Battery**: 5000mAh+ with fast charging

## Conclusion:
All these phones deliver excellent gaming performance. Choose based on your OS preference (iOS vs Android) and budget.'''
            },
            {
                'title': 'Smartwatch Comparison 2026: Apple Watch vs Samsung Galaxy Watch',
                'slug': 'smartwatch-comparison-2026',
                'description': 'Confused between Apple Watch Ultra and Samsung Galaxy Watch 6 Classic? Our detailed comparison covers features, battery life, and ecosystem compatibility.',
                'content': '''# Smartwatch Battle: Apple Watch Ultra vs Samsung Galaxy Watch 6 Classic

Two smartwatch titans go head to head in our comprehensive comparison.

## Design & Build
- **Apple Watch Ultra**: Titanium case, rugged design, 49mm
- **Samsung Galaxy Watch 6 Classic**: Premium stainless steel, rotating bezel, 43mm/47mm options

## Display
- **Apple Watch Ultra**: 1.92-inch Retina display, always-on
- **Samsung Galaxy Watch 6 Classic**: 1.3-inch AMOLED, always-on, rotating bezel

## Features
- **Apple Watch Ultra**: Fitness tracking, ECG, blood oxygen, emergency SOS, diving features
- **Samsung Galaxy Watch 6 Classic**: Fitness tracking, ECG, SpO2, blood pressure (Korea), sleep analysis

## Battery Life
- **Apple Watch Ultra**: 36 hours
- **Samsung Galaxy Watch 6 Classic**: 5-7 days

## Ecosystem
- **Apple Watch Ultra**: Works best with iPhone
- **Samsung Galaxy Watch 6 Classic**: Best with Samsung phones, but compatible with most Android phones

## Verdict:
Choose Apple Watch Ultra for iOS users who want premium features and design. Choose Galaxy Watch 6 Classic for Android users who prefer longer battery life and more affordable pricing.'''
            },
            {
                'title': 'Tablet Buyer\'s Guide 2026: iPad vs Samsung vs Microsoft',
                'slug': 'tablet-buyers-guide-2026',
                'description': 'Tablets are more powerful than ever. Whether you need it for work, entertainment, or creation, find the perfect tablet in our comprehensive guide.',
                'content': '''# Ultimate Tablet Buyer's Guide 2026

Tablets have evolved into powerful devices that can replace laptops. Here's how to choose the right one.

## iPad Pro (Apple)
**Best For**: Creative professionals, content creators
- **Specs**: M2/M4 chip, ProMotion display, Apple Pencil support
- **Price**: Premium ($1,099+)
- **Ecosystem**: Seamless integration with Apple devices
- **Verdict**: Best overall tablet

## Samsung Galaxy Tab S9 Ultra
**Best For**: Media consumption, productivity
- **Specs**: AMOLED display, powerful processor, S Pen included
- **Price**: Mid-range ($899+)
- **Ecosystem**: Android, works with most devices
- **Verdict**: Best for Android fans

## Microsoft Surface Pro 9
**Best For**: Windows laptop replacement
- **Specs**: Intel processors, Windows 11, full operating system
- **Price**: Premium ($999+)
- **Ecosystem**: Full Windows software library
- **Verdict**: Best hybrid device

## Budget Options
- **iPad (10th Gen)**: Starting at $349
- **Samsung Galaxy Tab A**: Starting at $229
- **Lenovo Tab M10**: Starting at $199

## Comparison Table:
| Feature | iPad Pro | Galaxy Tab S9 Ultra | Surface Pro 9 |
|---------|----------|-------------------|---------------|
| Display | Excellent | Outstanding | Good |
| Performance | Exceptional | Very Good | Very Good |
| Accessories | Pricey | Affordable | Moderate |
| Software | iOS/iPadOS | Android | Windows |

## Conclusion:
Best Overall: iPad Pro
Best Value: Samsung Galaxy Tab S9 Ultra
Best Windows: Microsoft Surface Pro 9'''
            },
            {
                'title': 'Laptop Recommendations For Students And Professionals',
                'slug': 'laptop-recommendations-students-professionals',
                'description': 'Find the perfect laptop for your needs. We compare MacBooks, Windows laptops, and budget options for different use cases.',
                'content': '''# Best Laptops for Students and Professionals

Choosing a laptop can be challenging. Let's break down the best options for different needs.

## For Students
**Budget**: $500-$1000

### Best Choice: ASUS VivoBook 15
- **Processor**: Latest Intel/AMD
- **RAM**: 8GB-16GB
- **Storage**: 512GB SSD
- **Battery**: 10+ hours
- **Price**: Around $700

### Budget Option: Lenovo IdeaPad 5
- **Processor**: Ryzen 5
- **RAM**: 8GB
- **Storage**: 256GB SSD
- **Price**: Around $500

## For Professionals
**Budget**: $1500-$3000

### Best Choice: MacBook Pro 16"
- **Processor**: M3 Pro/Max chip
- **RAM**: 18GB-36GB
- **Storage**: 512GB-1TB SSD
- **Display**: Excellent color accuracy
- **Price**: Around $2,500

### Windows Alternative: Dell XPS 15
- **Processor**: Latest Intel Core i7/i9
- **RAM**: 16GB-32GB
- **Storage**: 512GB-1TB SSD
- **Display**: InfinityEdge, 4K options
- **Price**: Around $1,800

## For Creators
**Budget**: $2000+

### Video/Photo Editing: MacBook Pro 16" M3 Max
- Excellent for Final Cut Pro and Adobe CC
- Fast rendering times
- Color-accurate display

### Coding: ASUS ROG Book
- High-end gaming specs
- Great cooling system
- Perfect for development

## Comparison Checklist:
- [ ] Processor meets your needs
- [ ] RAM sufficient for multitasking
- [ ] Storage adequate (512GB minimum)
- [ ] Display quality for your work
- [ ] Battery life acceptable
- [ ] Build quality solid
- [ ] Warranty coverage good

## Final Verdict:
Students: ASUS VivoBook 15
Professionals: MacBook Pro 16"
Creators: Depends on software (Mac or Windows)
Budget: Lenovo IdeaPad 5'''
            },
            {
                'title': '5G Smartphones: Which Ones Are Worth Buying?',
                'slug': '5g-smartphones-worth-buying',
                'description': '5G is the future of mobile networks. We test 5G speeds and help you decide if a 5G phone is worth the investment.',
                'content': '''# 5G Smartphones: Worth The Premium?

5G is rolling out globally. But do you actually need a 5G phone? Let's find out.

## 5G Coverage Status
- **USA**: 5G available in major cities, expanding rapidly
- **Europe**: 5G networks active in most countries
- **Asia**: 5G leading adoption especially in East Asia
- **Coverage**: Check with your carrier before buying

## Benefits of 5G:
- Faster download speeds (up to 1Gbps)
- Lower latency (great for gaming)
- Better video streaming
- Improved cloud apps

## Top 5G Phones:
1. **iPhone 15 Pro Max** - Best overall
2. **Samsung Galaxy S24 Ultra** - Best Android
3. **OnePlus 12S** - Best value
4. **Google Pixel 8 Pro** - Best camera

## Current 5G Speeds:
- Average Download: 100-200 Mbps
- Peak Download: 500+ Mbps
- Upload: 20-50 Mbps

## Should You Buy 5G?
**Yes if**:
- 5G is available in your area
- You stream video frequently
- You game on mobile
- You want future-proofing

**No if**:
- 4G LTE is sufficient for your needs
- 5G not yet in your area
- You want to save money
- You don't stream heavy content

## Recommendation:
Buy 5G if available in your area. Most flagship phones now come with 5G anyway. The premium has become minimal.'''
            },
            {
                'title': 'Camera Showdown: Which Smartphone Has The Best Camera?',
                'slug': 'camera-showdown-best-smartphone',
                'description': 'We tested cameras on the latest flagship phones. Find out which smartphone takes the best photos and videos.',
                'content': '''# Smartphone Camera Showdown 2026

We tested cameras on 10 flagship phones. Here are the results.

## Best Overall Camera: iPhone 15 Pro Max
- Exceptional low-light performance
- Accurate color reproduction
- Excellent zoom capabilities
- Best video stabilization
- **Score: 9.5/10**

## Best Android Camera: Samsung Galaxy S24 Ultra
- Incredible 200MP sensor
- Versatile zoom range
- Great night mode
- Excellent detail
- **Score: 9.3/10**

## Best Value Camera: Google Pixel 8 Pro
- Outstanding computational photography
- Best night mode
- Most realistic colors
- Great zoom
- **Score: 9.1/10**

## Camera Specifications Comparison:
| Phone | Main | Ultra Wide | Telephoto | Front |
|-------|------|-----------|-----------|-------|
| iPhone 15 Pro Max | 48MP | 12MP | 12MP 5x | 12MP |
| Galaxy S24 Ultra | 200MP | 50MP | 50MP 5x | 40MP |
| Pixel 8 Pro | 50MP | 48MP | 48MP 5x | 42MP |

## What Matters:
- Sensor size (not just megapixels)
- Lens quality
- Computational photography
- Low-light performance
- Video stabilization

## Verdict:
For overall quality: iPhone 15 Pro Max
For versatility: Samsung Galaxy S24 Ultra
For value: Google Pixel 8 Pro

**Pro Tip**: Modern phones all take excellent photos. The differences are subtle. Choose based on ecosystem, not just camera.'''
            },
            {
                'title': 'Battery Technology 2026: Which Phones Have The Best Battery Life?',
                'slug': 'battery-technology-2026',
                'description': 'Battery life is crucial. We tested battery performance on the latest phones to find out which lasts the longest.',
                'content': '''# Best Battery Life 2026: Full Testing Results

We tested each phone's battery life with daily usage patterns.

## Battery Life Winners:
1. **Samsung Galaxy S24 Ultra**: 12+ hours heavy use
2. **iPhone 15 Pro Max**: 10+ hours heavy use
3. **Google Pixel 8 Pro**: 9+ hours heavy use
4. **OnePlus 12S**: 11+ hours heavy use

## Battery Specifications:
- **iPhone 15 Pro Max**: 4,685 mAh
- **Galaxy S24 Ultra**: 5,000 mAh
- **Pixel 8 Pro**: 5,050 mAh
- **OnePlus 12S**: 5,400 mAh

## Charging Speeds:
- **iPhone 15 Pro Max**: 27W wired, 15W wireless
- **Galaxy S24 Ultra**: 45W wired, 15W wireless
- **Pixel 8 Pro**: 30W wired, 23W wireless
- **OnePlus 12S**: 100W wired, 50W wireless

## Battery Optimization Features:
- AI battery management
- Thermal throttling
- Power modes (low power, smart switch)
- Fast charging with protection

## Tips for Better Battery Life:
1. Lower screen brightness
2. Use dark mode on AMOLED phones
3. Close background apps
4. Disable unnecessary features
5. Use battery saver mode

## Verdict:
If battery life is priority: Samsung Galaxy S24 Ultra
If fast charging matters: OnePlus 12S
If ecosystem matters more: iPhone 15 Pro Max'''
            },
            {
                'title': 'Tech News: Latest Announcements From Apple, Samsung, And Google',
                'slug': 'tech-news-latest-announcements',
                'description': 'Stay updated with the latest tech news. Major announcements from Apple, Samsung, Google, and other manufacturers.',
                'content': '''# Latest Tech News & Announcements

## Apple News:
- iPhone 16 expected late 2026 with new processor
- New MacBook Pro models with M4 chips coming soon
- Apple Watch 11 will have health features
- New iPad Pro models with OLED displays

## Samsung News:
- Galaxy S25 development underway
- Foldable phones getting thinner and lighter
- New Galaxy Tablets planned for 2026
- 50MP main camera becoming standard

## Google News:
- Pixel 10 with advanced AI features
- Project Ara modular phone coming
- Tensor G5 chip in development
- Better Android integration with wearables

## Industry Trends:
- Foldable phones becoming mainstream
- AI processing on-device becoming standard
- Battery tech improving rapidly
- Satellite connectivity expanding
- Sustainable manufacturing focus

## What To Expect in 2026:
- Processors 20% faster than 2025
- Better AI features on all phones
- Faster charging technology
- Improved camera sensors
- More foldable options

## Articles You Might Like:
- Best Foldable Phones 2026
- AI Features in Smartphones
- Upcoming Phone Releases
- Tech Predictions 2027'''
            },
            {
                'title': 'Foldable Phones: The Future of Smartphones?',
                'slug': 'foldable-phones-future',
                'description': 'Foldable phones are no longer sci-fi. We review the latest foldable technology and ask: are they the future?',
                'content': '''# Foldable Phones: Are They The Future?

Foldable phones are becoming more accessible and practical. Let's examine the current state of the technology.

## Current Foldable Options:
1. **Samsung Galaxy Z Fold 6**: Best all-around
2. **Samsung Galaxy Z Flip 6**: Most compact
3. **Google Pixel Fold**: Best software
4. **OnePlus Open**: Best value

## Pros of Foldables:
- Larger display when unfolded
- Compact when folded
- Unique multitasking possibilities
- Impressive technology showcase
- Gaming experience on tablet-sized screen

## Cons of Foldables:
- Expensive ($1,500-$2,000)
- Durability concerns
- Crease visible in center
- Battery life sometimes compromised
- Limited app optimization

## Durability Improvements:
- Better hinge technology
- More resistant screens
- Longer lifespan testing (300,000+ folds)
- Improved water resistance
- Better gap sealing

## Best For:
- Content creators
- Power users
- Tech enthusiasts
- Multitasking professionals
- Media consumption lovers

## Not Ideal For:
- Budget-conscious buyers
- Durability-focused users
- Simple phone users
- Those wanting proven technology

## Market Predictions:
- Foldables will represent 5% of market by 2027
- Prices will decrease significantly
- More manufacturers entering market
- Crease technology will improve
- Foldables will become mainstream in 2028-2030

## Verdict:
Exciting innovation, but not yet mainstream. Wait 1-2 years for better tech and lower prices, unless you're an early adopter.'''
            },
            {
                'title': 'Wireless Earbuds Comparison: AirPods vs Galaxy Buds vs Pixel Buds',
                'slug': 'wireless-earbuds-comparison',
                'description': 'Which wireless earbuds are best? We compare the top options from Apple, Samsung, and Google to help you choose.',
                'content': '''# Wireless Earbuds: The Ultimate Comparison

Wireless earbuds have become essential tech. Here's a comprehensive comparison.

## Top Contenders:

### AirPods Pro 2
- **Price**: $249
- **Features**: Noise cancellation, spatial audio, great battery
- **Best For**: iPhone users
- **Verdict**: Best overall for Apple ecosystem

### Samsung Galaxy Buds 3 Pro
- **Price**: $229
- **Features**: ANC, IPX7 rating, touch controls
- **Best For**: Samsung phones
- **Verdict**: Best value flagship earbuds

### Google Pixel Buds Pro
- **Price**: $199
- **Features**: Real-time translation, call screening, seal
- **Best For**: Pixel phone users
- **Verdict**: Best for Google Assistant

## Comparison Table:
| Feature | AirPods Pro 2 | Galaxy Buds 3 Pro | Pixel Buds Pro |
|---------|--------------|-----------------|----------------|
| ANC | Excellent | Excellent | Very Good |
| Battery | 6h | 5h | 6h |
| Charging | MagSafe | USB-C | USB-C |
| Price | $249 | $229 | $199 |
| Fit | Excellent | Excellent | Good |

## Which Should You Buy?

**Best Overall**: AirPods Pro 2
- Premium sound quality
- Excellent ANC
- Great ecosystem integration

**Best Value**: Google Pixel Buds Pro
- Lowest price
- Solid features
- Great translation

**Best for Android**: Galaxy Buds 3 Pro
- IPX7 rating
- Samsung integration
- Excellent sound

## Key Features to Consider:
- Noise cancellation quality
- Battery life
- Fit and comfort
- Sound quality
- Price
- Ecosystem compatibility

## Final Recommendation:
Choose based on your phone ecosystem. All three offer excellent audio quality at competitive prices.'''
            }
        ]
        
        created = 0
        for news in news_data:
            obj, created_new = NewsArticle.objects.get_or_create(
                slug=news['slug'],
                defaults={
                    'title': news['title'],
                    'excerpt': news['description'],
                    'content': news['content'],
                    'category': 'Tech News',
                }
            )
            if created_new:
                created += 1
                self.stdout.write(f'✓ {news["title"]}')
            else:
                self.stdout.write(f'- {news["title"]} (already exists)')
        
        self.stdout.write(f'\n{self.style.SUCCESS("Done!")} {created} new articles added.')
