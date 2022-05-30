from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('reset/', views.reset_view, name='reset'),
    path('logout/', views.logout_view, name='logout'),
    path('browse/', views.categories_view, name='browse'),
    path('sales/', views.sales_view, name='sales'),
    path('category/<int:category>/', views.category_view, name='category'),
    path('product/<int:product>/', views.product_view, name='product'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('<str:username>/', views.profile_view, name='profile'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "Delsur Admin Site"  
admin.site.site_title  =  "Delsur"
admin.site.index_title  =  "Admin"