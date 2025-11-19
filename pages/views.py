from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from . models import Laptop , Mobile , Accessories
from decimal import Decimal, InvalidOperation

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer , UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test

from shop_orders.models import Order

# Create your views here.

def about(request):
    return render(request,'pages/about.html')

def register(request):
    return render(request, 'pages/register.html')

def laptop(request):
    return render(request, 'product/laptop.html',{'lap':Laptop.objects.all()})

def mobile(request):
    return render(request, 'product/mobile.html',{'mob':Mobile.objects.all()})

def accessories(request):
    return render(request, 'product/accessories.html',{'acc':Accessories.objects.all()})

def login_User(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # إنشاء الجلسة
            # إذا كان مشرف/ادمن، اذهب للوحة التحكم
            if user.is_staff or user.is_superuser:
                return redirect('control')
            else:
                return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")
    return render(request, 'pages/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    category = request.GET.get('category', 'All')

    # اجمع كل المنتجات في قائمة واحدة
    products = list(Laptop.objects.all()) + list(Mobile.objects.all()) + list(Accessories.objects.all())

    # فلترة حسب قيمة category داخل المنتج نفسه
    if category != "All":
        category_lower = category.lower()
        products = [p for p in products if p.category.lower() == category_lower]

    return render(request, 'pages/home.html', {
        'product_list': products,
        'selected_category': category
    })

def is_admin(user):
    return user.is_staff or user.is_superuser

def control(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_superuser:
        return redirect('home')
    
    laptops = Laptop.objects.all()
    mobiles = Mobile.objects.all()
    accessories = Accessories.objects.all()
    
    products = list(laptops) + list(mobiles) + list(accessories)
    
    status_choices = Order.STATUS_CHOICES
    orders = Order.objects.all()
    orders = Order.objects.all().prefetch_related('items')
    
    return render(request, 'pages/admin.html', { 
    'products': products,
    'orders': orders,   # صحح الاسم هنا
    'status_choices': status_choices
    })

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('control')

def update_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES).keys():
            order.status = status
            order.save()
    return redirect('control')
    
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # تحويل السعر إلى Decimal مع معالجة الخطأ
        try:
            price = Decimal(price)
        except (InvalidOperation, TypeError):
            price = Decimal('0.00')  # قيمة افتراضية إذا كان غير صالح

        # إضافة المنتج حسب الفئة
        if category == 'Laptop':
            Laptop.objects.create(name=name, category=category, price=price, content=content, image=image)
        elif category == 'Mobile':
            Mobile.objects.create(name=name, category=category, price=price, content=content, image=image)
        elif category == 'Accessories':
            Accessories.objects.create(name=name, category=category, price=price, content=content, image=image)

        return redirect('control')
    return redirect('control')

def edit_product(request, product_id):
    # البحث عن المنتج في كل الجداول
    product = None
    for model in [Laptop, Mobile, Accessories]:
        try:
            product = model.objects.get(id=product_id)
            break
        except model.DoesNotExist:
            continue
    
    if not product:
        return redirect('control')

    # تعديل المنتج
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category = request.POST.get('category')
        product.price = request.POST.get('price')
        product.content = request.POST.get('content')

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('control')

    # إذا دخل هنا فهو GET → نعيده للوحة التحكم
    return redirect('control')

def delete_product(request, product_id):
    # تحقق أي نوع المنتج هو لتحديد الموديل الصحيح
    for model in [Laptop, Mobile, Accessories]:
        try:
            product = model.objects.get(id=product_id)
            product.delete()
            break
        except model.DoesNotExist:
            continue
    return redirect('control')

@api_view(['POST'])
def register_api(request):
    serializer = SignUpSerializer(data=request.data)
    
    if serializer.is_valid():
        if User.objects.filter(username=request.data['email']).exists():
            return Response({'error': 'This Email Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'details': 'Your Account Registered Successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)