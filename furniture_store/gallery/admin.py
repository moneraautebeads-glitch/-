from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Order, Review, ContactMessage

# إعدادات مظهر لوحة التحكم العامة
admin.site.site_header = "إدارة معرض منيرة العتيبي"
admin.site.site_title = "منيرة العتيبي للأثاث"
admin.site.index_title = "مرحباً بك في نظام إدارة المتجر"

# 1. نظام الصور المتعددة (Inline)
# يسمح لك برفع صور المعرض الإضافية من داخل صفحة المنتج نفسه
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5  # يظهر 5 خانات إضافية فارغة افتراضياً
    fields = ('image', 'alt_text')
    verbose_name = "صورة إضافية"
    verbose_name_plural = "معرض الصور الإضافية للمنتج"


# 2. إدارة الأقسام
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_product_count')
    prepopulated_fields = {'slug': ('name',)} # توليد الرابط تلقائياً من الاسم
    search_fields = ('name',)
    
    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = "عدد المنتجات بالقسم"


# 3. إدارة المنتجات (القلب النابض للموقع)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # إظهار صورة مصغرة في جدول المنتجات للسهولة
    def image_tag(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width: 50px; height:50px; border-radius: 5px;" />'.format(obj.main_image.url))
        return "لا توجد صورة"
    image_tag.short_description = 'صورة المنتج'

    list_display = ('image_tag', 'title', 'category', 'price', 'discount_price', 'is_available', 'stock_quantity')
    list_filter = ('category', 'is_available', 'created_at')
    list_editable = ('price', 'discount_price', 'is_available', 'stock_quantity') # تعديل سريع من الجدول
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    # دمج معرض الصور داخل صفحة إضافة المنتج
    inlines = [ProductImageInline]
    
    # تنظيم الحقول داخل صفحة التعديل
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'category', 'description')
        }),
        ('التسعير والمخزون', {
            'fields': (('price', 'discount_price'), ('stock_quantity', 'is_available'))
        }),
        ('الوسائط الرئيسية', {
            'fields': ('main_image',)
        }),
    )


# 4. إدارة الطلبات (تتبع المبيعات)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'product', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'address')
    readonly_fields = ('created_at',) # منع تعديل تاريخ الطلب لضمان الدقة
    
    # تمييز الحالات بالألوان في لوحة التحكم
    def get_status_display(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'canceled': 'red',
        }
        return format_html(
            '<b style="color:{};">{}</b>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    
    # استبدال حقل الحالة بالشكل الملون في العرض (اختياري)
    # list_display = ('id', 'customer_name', 'product', 'get_status_display', 'created_at')


# 5. إدارة التقييمات
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('name', 'comment')


# 6. إدارة رسائل التواصل
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('full_name', 'phone', 'message')
    
    # جعل الرسائل للقراءة فقط لمنع التلاعب بالبيانات الواردة
    def has_add_permission(self, request):
        return False
    
    # ترتيب الرسائل بحيث تظهر غير المقروءة أولاً
    ordering = ('is_read', '-created_at')
