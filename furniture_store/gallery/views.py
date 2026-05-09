from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order

# الصفحة الرئيسية
def index(request):
    items = Product.objects.all()
    return render(request, 'gallery/index.html', {'furniture_items': items})

# صفحة تتبع الطلب (تم تصحيح الخطأ هنا)
def track_order(request):
    phone = request.GET.get('phone')
    orders_list = None
    if phone:
        # التعديل: order_by وليس order_back
        orders_list = Order.objects.filter(customer_phone=phone).order_by('-created_at')
    return render(request, 'gallery/track.html', {'orders': orders_list, 'phone': phone})

# صفحة إنشاء الطلب
def orders(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone = request.POST.get('customer_phone')
        address = request.POST.get('address')
        
        Order.objects.create(
            product=product, 
            customer_name=name, 
            customer_phone=phone, 
            address=address
        )
        return render(request, 'gallery/success.html', {'product': product})
        
    return render(request, 'gallery/order_form.html', {'product': product})
