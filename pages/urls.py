from django.urls import path , include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# قائمة الصفحات العامة (لا تحتاج تسجيل دخول)
PUBLIC_PATHS = [
    'login',            # اسم الـ url لصفحة تسجيل الدخول
    'logout_user',
    'register',         # صفحة التسجيل
    'register_api',     # API التسجيل
    'token_obtain_pair',# JWT الحصول على التوكن
    'token_refresh',    # JWT تحديث التوكن
]

urlpatterns = [
    # صفحات عامة
    path('', views.login_User, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # صفحات محمية
    path('home/', views.home, name='home'),
    path('control/', views.control, name='control'),
    path('about/', views.about, name='about'),
    path('laptop/', views.laptop, name='laptop'),
    path('mobile/', views.mobile, name='mobile'),
    path('accessories/', views.accessories, name='accessories'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    path('', include('shop_orders.urls')),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
