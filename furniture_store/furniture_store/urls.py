from django.contrib import admin
from django.urls import path, include
from gallery import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.contrib.sitemaps.views import sitemap
from gallery.sitemaps import ProductSitemap, StaticViewSitemap

# إعداد خريطة الموقع
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

# دالة إنشاء الحساب التلقائي
def create_admin_user():
    try:
        if not User.objects.filter(username='manager_monera').exists():
            User.objects.create_superuser('manager_monera', 'admin@furniture.com', 'Mona@Password2026')
    except:
        pass

create_admin_user()

urlpatterns = [
    # السطر اللي كان ناقص عشان الصفحة تشتغل
    path('gana/', admin.site.urls), 
    
    # خريطة الموقع
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # روابط الموقع الرئيسية
    path('', include('gallery.urls')),
]

# تفعيل عرض الصور من ميديا Cloudinary أو الملفات الثابتة
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
