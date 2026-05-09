from django.contrib.sitemaps import Sitemap
from .models import Product
from django.urls import reverse

class ProductSitemap(Sitemap):
    changefreq = "weekly" # معدل التغيير المتوقع
    priority = 0.9        # الأهمية (من 0 إلى 1)

    def items(self):
        return Product.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        # تأكد أن لديك دالة get_absolute_url في الموديل أو استخدم مسار ثابت
        return f"/product/{obj.id}/" 

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['index', 'track_order'] # أسماء المسارات الثابتة لديك

    def location(self, item):
        return reverse(item)
