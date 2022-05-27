from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, gender, date_of_birth, email, username, password=None):
        if not first_name and last_name:
            raise ValueError("First and last names are missing!")
        if not first_name:
            raise ValueError("First name is missing!")
        if not last_name:
            raise ValueError("Last name is missing!")
        if not email:
            raise ValueError("Valid email address is missing!")
        if not username:
            raise ValueError("Username is missing!")
        if not date_of_birth:
            raise ValueError("Please enter your date of birth.")
        if not gender:
            raise ValueError("Please choose a gender.")

        user = self.model(
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            email=self.normalize_email(email),
            username=username,
            date_of_birth=date_of_birth,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, gender, date_of_birth, email, username, password=None):
        user = self.create_user(
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            email=self.normalize_email(email),
            username=username,
            date_of_birth=date_of_birth,
            gender=gender,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", 'Male'),
            ("F", 'Female'),
            ("O", 'Other'),
        ]
    )
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    profile_pic = models.ImageField(
        max_length="255", upload_to=f"users/{id}", null=True, blank=True, default="users/profilepic.jpg")
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'date_of_birth', 'gender', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Carousel(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='carousel')
    bg_color = models.CharField(max_length=50, default='#ffffff')
    featured = models.BooleanField(default=False)
    link_to = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.title


class Address(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    State_choices = [
        ('ACT', 'Australian Capital Territory'),
        ('NSW', 'New South Wales'),
        ('Qld', 'Queensland'),
        ('SA', 'South Australia'),
        ('Vic', 'Victoria'),
        ('Tas', 'Tasmania'),
        ('WA', 'Western Australia'),
    ]
    state = models.CharField(max_length=3, choices=State_choices)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.user_id.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories")
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class CategoryProduct(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="categories/products")
    createdDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category_product_id = models.ForeignKey(
        CategoryProduct, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    stock = models.IntegerField()
    warranty = models.CharField(max_length=100)
    description = RichTextField()
    specification = RichTextField()
    soldNum = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings")
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(max_length=500, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)


class Color(models.Model):
    color = models.CharField(max_length=100)
    product_id = models.ForeignKey(
        Product, related_name='colors', on_delete=models.CASCADE)

    def __str__(self):
        return self.color


class ProductImage(models.Model):
    product_id = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="categories/products/product")

    def __str__(self):
        return self.product_id.name


class Order(models.Model):
    Status_choices = [
        ('P', 'Pending'),
        ('C', 'Canceled'),
        ('D', 'Delivered'),
    ]
    Delivery_choices = [
        ('P', 'Pick Up'),
        ('D', 'Delivered'),
    ]
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_uuid = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=200, blank=True, null=True)
    shippingPrice = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_choice = models.CharField(max_length=1, choices=Delivery_choices)
    status = models.CharField(
        max_length=1, choices=Status_choices, default=Status_choices[0])
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    delivered_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.order_uuid


class OrderItem(models.Model):
    order_id = models.ForeignKey(
        Order, related_name='orderItem', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
