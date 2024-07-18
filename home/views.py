from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User

class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['contacts'] = ContactInfo.objects.all()

class HomeView(BaseView):
    def get(self,request):
        self.views
        try:
            username = request.user.username
            self.views['count_cart'] = Cart.objects.filter(username=username, checkout=False).count()
        except:
            pass
        self.views['sliders'] = slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['products'] = product.objects.all()
        self.views['hots'] = product.objects.filter(label = 'hot')
        self.views['news'] = product.objects.filter(label = 'new')
        self.views['sales'] = product.objects.filter(label = 'sale')
        return render(request,'index.html',self.views)

class ProductView(BaseView):
    def get(self,request,slug):
        self.views
        self.views['detail_product'] = product.objects.filter(slug = slug)
        cat_id = product.objects.get(slug = slug).category
        self.views['related_product'] = product.objects.filter(category_id = cat_id)
        self.views['product_reviews'] = productReview.objects.filter(slug = slug)
        try:
            username = request.user.username
            self.views['count_cart'] = Cart.objects.filter(username=username, checkout=False).count()
        except:
            pass
        return render(request,'product-detail.html',self.views)

class CategoryView(BaseView):
    def get(self,request,slug):
        self.views
        try:
            username = request.user.username
            self.views['count_cart'] = Cart.objects.filter(username=username, checkout=False).count()
        except:
            pass
        cat_id = Category.objects.get(slug = slug).id
        self.views['cat_product'] = product.objects.filter(category_id = cat_id)
        return render(request,'category.html',self.views)


class BrandView(BaseView):
    def get(self,request,slug):
        self.views
        try:
            username = request.user.username
            self.views['count_cart'] = Cart.objects.filter(username=username, checkout=False).count()
        except:
            pass
        b_id = Brand.objects.get(slug = slug).id
        self.views['brand_product'] = product.objects.filter(brand_id = b_id)
        return render(request,'brand.html',self.views)

class SearchView(BaseView):
    def get(self,request):
        if request.method == 'GET':
            query = request.GET['query']
            if query != "":
                self.views['search_product'] = product.objects.filter(name__icontains = query)
        return render(request,'search.html',self.views)
def signup(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Username already exists!")
                return redirect('/sighup')
            elif User.objects.filter(email = email).exists():
                messages.error(request, "Email already in use!")
                return redirect('/sighup')
            else:
                User.objects.create_user(
                    first_name = fname,
                    last_name = lname,
                    username = username,
                    email = email,
                    password = password
                ).save()
        else:
            messages.error(request, "Password does not match!")
            return redirect('/signup')
    return render(request,'signup.html')

def add_to_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(username = username, slug = slug,checkout = False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        quantity = quantity + 1
        price = product.objects.get(slug = slug).price
        discounted_price = product.objects.get(slug = slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
            total = original_price * quantity
        else:
            original_price = price
            total = original_price * quantity

        Cart.objects.filter(username=username, slug=slug, checkout=False).update(
            quantity = quantity,
            total = total
        )
    else:
        price = product.objects.get(slug=slug).price
        discounted_price = product.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        Cart.objects.create(
            username = username,
            slug = slug,
            total = original_price,
            item = product.objects.filter(slug = slug)[0]
        ).save()
    return redirect('/my_cart')

def reduce_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(username = username, slug = slug,checkout = False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        if quantity > 1:
            quantity = quantity - 1
            price = product.objects.get(slug = slug).price
            discounted_price = product.objects.get(slug = slug).discounted_price
            if discounted_price > 0:
                original_price = discounted_price
                total = original_price * quantity
            else:
                original_price = price
                total = original_price * quantity

            Cart.objects.filter(username=username, slug=slug, checkout=False).update(
                quantity = quantity,
                total = total
            )
    return redirect('/my_cart')

def delete_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        Cart.objects.filter(username=username, slug=slug, checkout=False).delete()

    return redirect('/my_cart')
class CartView(BaseView):
    def get(self,request):
        try:
            username = request.user.username
            self.views['count_cart'] = Cart.objects.filter(username=username, checkout=False).count()
        except:
            pass
        carts = Cart.objects.filter(username = username,checkout = False)
        self.views['cart_product'] = carts
        all_total = 0
        for i in carts:
            all_total = all_total + i.total
        self.views['all_total'] = all_total
        # self.views['delivery'] = 50
        self.views['grand_total'] = all_total + 50
        return render(request,'cart.html',self.views)

from django.core.mail import send_mail
def contact(request):
    if request.Method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Contact.objects.create(
            name = name,
            email = email,
            subject = subject,
            message = message
        ).save()
        send_mail(
            "Form submitted",
            f"Hello {name} having email {email}. I am very glad to say that your query will be replayed soon.",
            "from@example.com",
            [email],
            fail_silently=False,
        )
    return render(request,'contact.html')


def product_review(request,slug):
    if product.objects.filter(slug = slug):
        if request.method == 'POST':
            username = request.user.username
            star = request.POST['star']
            comment = request.POST['comment']
            productReview.objects.create(
                username = username,
                slug = slug,
                star = star,
                comment = comment
            ).save()
    else:
        return redirect(f'/product/{slug}')
    return redirect(f'/product/{slug}')