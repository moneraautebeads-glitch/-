from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# 1. موديل الأقسام (Categories)
# لتصنيف الأثاث: غرف نوم، غرف أطفال، صالونات، إلخ.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم القسم")
    slug = models.SlugField(unique=True, verbose_name="رابط فريد (Slug)", help_text="يظهر في رابط الموقع")
    description = models.TextField(blank=True, verbose_name="وصف القسم")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="صورة القسم")

    class Meta:
        db_table = 'gallery_category'
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

    def __str__(self):
        return self.name


# 2. موديل المنتجات (Products)
# المعلومات الأساسية لكل قطعة أثاث في معرض منيرة العتيبي.
class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products', 
        verbose_name="القسم"
    )
    title = models.CharField(max_length=200, verbose_name="اسم المنتج")
    description = models.TextField(verbose_name="وصف المنتج التفصيلي")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="السعر بعد الخصم"
    )
    # الصورة الرئيسية هي اللي بتظهر في الكروت بره
    main_image = models.ImageField(upload_to='products/', verbose_name="الصورة الرئيسية للمنتج")
    is_available = models.BooleanField(default=True, verbose_name="متوفر للعرض")
    stock_quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية المتاحة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gallery_product'
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# 3. موديل معرض الصور (Product Images Gallery)
# الحل النهائي لمشكلة "الصورة الواحدة" - يسمح برفع عدد غير محدود من الصور لكل منتج.
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name="المنتج"
    )
    image = models.ImageField(upload_to='products/gallery/', verbose_name="صورة إضافية")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="وصف الصورة (SEO)")

    class Meta:
        db_table = 'gallery_product_images'
        verbose_name = "صورة إضافية"
        verbose_name_plural = "معرض صور المنتجات"

    def __str__(self):
        return f"صورة لمنتج: {self.product.title}"


# 4. موديل الطلبات (Orders)
# لاستقبال طلبات الشراء من الزبائن وتتبع حالتها.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة ⏳'),
        ('processing', 'جاري التجهيز 🛠️'),
        ('shipped', 'تم الشحن 🚚'),
        ('delivered', 'تم التوصيل ✅'),
        ('canceled', 'طلب ملغي ❌'),
    ]

    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name='orders', 
        verbose_name="المنتج المطلوب"
    )
    customer_name = models.CharField(max_length=150, verbose_name="اسم العميل الكامل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    address = models.TextField(verbose_name="عنوان التوصيل بالتفصيل")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية المطلوبة")
    order_notes = models.TextField(blank=True, verbose_name="ملاحظات العميل")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="حالة الطلب"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        db_table = 'gallery_order'
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب #{self.id} من {self.customer_name}"


# 5. موديل التقييمات (Product Reviews)
# لزيادة مصداقية المعرض من خلال آراء الزبائن.
class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews', 
        verbose_name="المنتج"
    )
    name = models.CharField(max_length=100, verbose_name="اسم المعلق")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        verbose_name="التقييم (1-5)"
    )
    comment = models.TextField(verbose_name="التعليق")
    is_approved = models.BooleanField(default=True, verbose_name="تمت الموافقة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_review'
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"


# 6. موديل تواصل معنا (Contact Messages)
# لاستقبال الاستفسارات العامة من زوار الموقع.
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    subject = models.CharField(max_length=200, verbose_name="الموضوع")
    message = models.TextField(verbose_name="نص الرسالة")
    is_read = models.BooleanField(default=False, verbose_name="تمت القراءة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery_contact'
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"
        ordering = ['-created_at']

    def __str__(self):
        return f"رسالة من {self.full_name} - {self.subject}"
