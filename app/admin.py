from django.contrib import admin
from .models import Address, Carousel, Category, CategoryProduct, Color, Product, ProductImage, Review, Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(CategoryProduct)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Carousel)


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
