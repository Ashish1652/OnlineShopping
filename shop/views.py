
# Create your views here.
from django.shortcuts import render, HttpResponse,redirect,HttpResponseRedirect
from .models import Product,Category,Customer,Order
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator

def error_404_view(request,exception):
    return render('about.html')


def index(request):
    # products = Product.ge_all_products();

    return render(request,'home.html')

class products(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:

                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] =cart
        print(request.session['cart'])
        return redirect('product')


    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None

        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.ge_all_products_by_categoryid(categoryID)
        else:
            products = Product.ge_all_products();

        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are :', request.session.get('email'))
        return render(request, 'product.html', data)


# def products(request):
    # products = None
    # categories = Category.get_all_categories()
    # categoryID = request.GET.get('category')
    # if categoryID:
    #     products = Product.ge_all_products_by_categoryid(categoryID)
    # else:
    #     products = Product.ge_all_products();
    #
    # data = {}
    # data['products'] = products
    # data['categories'] = categories
    # print('you are :',request.session.get('email'))
    # return render(request, 'product.html', data)

# def validateCustomer(customer):
#     error_messege =  None;
#     if (not customer.first_name):
#         error_messege = "First Name Required !!"
#     elif (not customer.last_name):
#         error_messege = "Last Name Required !!"
#     elif (not customer.phone):
#         error_messege = "Phone Number Required !!"
#     elif len(customer.first_name) < 4:
#         error_messege = "First Name Must be 4 char long or more"
#     elif len(customer.last_name) < 4:
#         error_messege = "Last Name Must be 4 char long or more"
#     elif len(customer.phone) < 10:
#         error_messege = "Phone Number Must be 10 digit long "
#     elif customer.isExist():
#
#         error_messege = 'Email Address already registered....'
#     return error_messege

# def regiseterUser(request):
    # postData = request.POST
    # first_name = postData.get('firstname')
    # last_name = postData.get('lastname')
    # phone = postData.get('phone')
    # email = postData.get('email')
    # password = postData.get('password')
    # value = {'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email': email}
    # error_messege = None
    # customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    #
    # error_messege = validateCustomer(customer)
    #
    #
    # if not error_messege:
    #
    #     print(first_name, last_name, phone, email, password)
    #     customer.password = make_password(customer.password)
    #     customer.register()
    #     return redirect('product')
    # else:
    #     data = {'error': error_messege, 'values': value}
    #     return render(request, 'signup.html', data)

# #
# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'signup.html')
#     else:
#         return regiseterUser(request)

class signup(View):
    def get(self,request):
        return render(request, 'signup.html')


    def post(self,request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email': email}
        error_messege = None
        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_messege = self.validateCustomer(customer)

        if not error_messege:

            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('product')
        else:
            data = {'error': error_messege, 'values': value}
            return render(request, 'signup.html', data)

    def validateCustomer(self,customer):
        error_messege = None;
        if (not customer.first_name):
            error_messege = "First Name Required !!"
        elif (not customer.last_name):
            error_messege = "Last Name Required !!"
        elif (not customer.phone):
            error_messege = "Phone Number Required !!"
        elif len(customer.first_name) < 4:
            error_messege = "First Name Must be 4 char long or more"
        elif len(customer.last_name) < 4:
            error_messege = "Last Name Must be 4 char long or more"
        elif len(customer.phone) < 10:
            error_messege = "Phone Number Must be 10 digit long "
        elif customer.isExist():

            error_messege = 'Email Address already registered....'
        return error_messege


class login(View):
    return_url = None
    def get(self,request):
        login.return_url = request.GET.get('return_url')
        return render(request,'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer']=customer.id
                request.session['email'] = customer.email
                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    return redirect('product')
            else:
                login.return_url = None
                error_message = 'Email or Password Invalid'

        else:
            error_message = 'Email or Password Invalid'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class cart(View):
    def get(self,request):
        ids =list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html',{'products':products})

class checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer,products)

        for product in  products:
            order = Order(customer = Customer(id = customer),product=product,price = product.price,
                          address = address,phone = phone,
                          quantity = cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('cart')

class orders(View):
    def get(self, request):
        customer = request.session.get('customer')
        order = Order.get_orders_by_customer(customer)
        print(order)
        # order = order.reverse()
        return render(request,'orders.html',{'orders':order})

# def services(request):
#     return render(request, 'about.html')
#
#
# def contact(request):
#     return render(request, 'contact.html')----------

#
# def index(request):
#     context = {'variable' : 'this is sent'}
#     return render(request,'home.html', context)
#     # return HttpResponse('Its Index PAeg')


def about(request):
    return render(request, 'about.html')

# def services(request):
#     return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')
