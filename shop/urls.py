# from django.urls import path,include
#
# from . import views
#
# urlpatterns = [
#     path('',views.index),
#     path('about',views.about),
#     path('services',views.services),
#     path('contact',views.contact),
#
#
# ]

from django.urls import path,include
from . import views
from .middlewares.auth import auth_middleware
urlpatterns = [

    path('', views.index),
    path('about', views.about, name='about'),
    path('product', views.products.as_view(), name='product'),
    path('contact', views.contact, name='contact'),
    path('signup',views.signup.as_view(),name='signup'),
    path('login',views.login.as_view(),name='login'),
    path('logout',views.logout,name='logout'),
    path('cart', views.cart.as_view(), name='cart'),
    path('checkout', views.checkout.as_view(), name='checkout'),
    path('orders', auth_middleware(views.orders.as_view()), name='orders'),

]

