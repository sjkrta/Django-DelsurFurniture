from datetime import datetime
import re
from django.shortcuts import redirect, render
from app.models import Account, Carousel, Category, Order, Product, ProductImage
from django.contrib.auth import authenticate, login, logout
defaultProductImage = "/media/categories/products/default.png"

def index_view(request):
    productsByCategory = []
    categories =  Category.objects.all()
    for category in categories:
        products=[]
        for product in Category.objects.get(id=category.id).products.all():
            image = defaultProductImage
            try:
                image = Product.objects.get(id=product.id).images.first().image.url
            except:
                pass
            products.append({"product":product,"image":image})
        productsByCategory.append({"category":category, "products":products})
    context = {
        "Carousel": Carousel.objects.all(),
        "ProductsByCategory": productsByCategory
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.user.is_anonymous:
        formValues = {}
        formErrors = {}
        if request.method == "POST":
            formValues['email'] = request.POST['email']
            formValues['password'] = request.POST['password']
            if formValues['email'] == "":
                formErrors['email'] = "Please enter your email address."
            elif len(formValues['email']) > 125:
                formErrors['email'] = "Your email address is invalid."
            if formValues['password'] == "":
                formErrors['password'] = "Please enter a password."
            elif len(formValues['password']) < 4 or len(formValues['password']) > 20:
                formErrors['password'] = "Your password is invalid."
            if len(formErrors) == 0:
                user = authenticate(
                    request, username=formValues['email'], password=formValues['password'])
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        context = {"formValues": formValues, "formErrors": formErrors}
        return render(request, 'pages/accounts/login.html', context)
    else:
        return redirect('home')


def register_view(request):
    if request.user.is_anonymous:
        day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
               17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        year = []
        gender = [
            {"id": "M", "name": "Male"},
            {"id": "F", "name": "Female"},
            {"id": "O", "name": "Other"}
        ]
        formValues = {}
        formErrors = {}
        currentyear = datetime.now().year
        for i in range(120):
            year.append(currentyear)
            currentyear -= 1
        if request.method == "POST":
            formValues['first_name'] = request.POST['first_name'].capitalize()
            formValues['last_name'] = request.POST['last_name'].capitalize()
            formValues['email'] = request.POST['email']
            formValues['username'] = request.POST['username'].lower()
            formValues['password'] = request.POST['password']
            formValues['password2'] = request.POST['password2']
            formValues['day'] = int(request.POST['day'])
            formValues['month'] = int(request.POST['month'])
            formValues['year'] = int(request.POST['year'])
            formValues['gender'] = request.POST.get('gender', None)
            if formValues['first_name'] == "" and formValues['last_name'] == "":
                formErrors['names'] = "First and last names are required."
            elif formValues['first_name'] == "":
                formErrors['first_name'] = "First name is required."
            elif formValues['last_name'] == "":
                formErrors['last_name'] = "Last name is required."
            elif len(formValues['first_name']) > 20:
                formErrors['first_name'] = "First name must not exceed more than 20 characters."
            elif len(formValues['last_name']) > 20:
                formErrors['last_name'] = "Last name must not exceed more than 20 characters."
            if formValues['username'] == "":
                formErrors['username'] = "Username is a required field."
            elif not re.match("^[a-z0-9.]*$", formValues['username']):
                formErrors['username'] = "Ensure to use letters, numbers and period only"
            elif len(formValues['username']) < 4 or len(formValues['username']) > 20:
                formErrors['username'] = "Username must be between 4-20 characters."
            else:
                if len(Account.objects.filter(username=formValues['username'])) > 0:
                    formErrors['username'] = "User with that username already exists."
            if formValues['email'] == "":
                formErrors['email'] = "Email address is a required field."
            elif len(formValues['email']) > 125:
                formErrors['email'] = "Email must not exceed more than 125 characters."
            else:
                if len(Account.objects.filter(email=formValues['email'])) > 0:
                    formErrors['email'] = "User with that email already exists."
            if formValues['gender'] == None:
                formErrors['gender'] = "Please select your gender."
            if formValues['password'] == "":
                formErrors['password'] = "Please enter a password."
            elif len(formValues['password']) < 8 or len(formValues['password']) > 20:
                formErrors['password'] = "Password must be between 8-20 characters."
            elif formValues['password2'] == "":
                formErrors['password2'] = "Confirm your password."
            elif formValues['password2'] != formValues['password']:
                formErrors['password2'] = "Passwords do not match."
            try:
                x = datetime(formValues['year'],
                             formValues['month'], formValues['day'])
            except:
                formErrors['date_of_birth'] = "Enter valid date of birth."
            else:
                diff = datetime.now() - \
                    datetime(
                        formValues["year"], formValues["month"], formValues["day"], 0, 0)
                if diff.days < (365*5):
                    formErrors['date_of_birth'] = "Enter your real date of birth."
            if len(formErrors) == 0:
                user = Account.objects.create_user(
                    first_name=formValues['first_name'],
                    last_name=formValues['last_name'],
                    email=formValues['email'],
                    username=formValues['username'],
                    date_of_birth=f"{formValues['year']}-{formValues['month']}-{formValues['day']}",
                    gender=formValues['gender']
                )
                user.set_password(formValues['password'])
                user.save()
                login(request, user)
                return redirect("home")
        context = {"formValues": formValues, "day": day,
                   "month": month, "year": year, "formErrors": formErrors, "gender": gender}
        return render(request, 'pages/accounts/register.html', context)
    else:
        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')


def reset_view(request):
    context = {}
    return render(request, 'pages/accounts/reset.html', context)


def categories_view(request):
    context = {}
    return render(request, 'pages/products/categories.html', context)


def category_view(request, category):
    context = {}
    return render(request, 'pages/products/category.html', context)


def product_view(request, product):
    product = Product.objects.get(id=product)
    image = defaultProductImage
    images = product.images.all()
    try:
        image = images.first().image.url
    except:
        pass
    context = {
        "images":images,
        "image":image,
        "product":product,
    }
    print(product.colors)
    return render(request, 'pages/products/product.html', context)


def sales_view(request):
    context = {}
    return render(request, 'pages/products/sales.html', context)


def cart_view(request):
    cart = Order.objects.get(user_id=request.user)
    orders = []
    total = 0
    for order in cart.orders.all():
        productImage = defaultProductImage
        try:
            productImage = Product.objects.get(id=order.product_id.id).images.all().first().image.url
        except:
            pass
        orders.append({"order":order,"image":productImage})
        total = total + order.price
    print(orders)
    context = {
        "promocode": "SALES2022",
        "orders":orders,
        "lenCart":len(orders),
        "total": total
    }
    return render(request, 'pages/shopping/cart.html', context)


def checkout_view(request):
    context = {}
    return render(request, 'pages/shopping/checkout.html', context)


def profile_view(request, username):
    context = {}
    return render(request, 'pages/shopping/profile.html', context)
