from django.urls import path
from . import views 

app_name = 'ecommerce'

urlpatterns = [
    path('', views.product_list ,name = 'product'),
    path('base/', views.product_list ,name = 'base'),
    path('home/', views.product_list ,name = 'home'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart ,name = 'cart'),
    path('checkout/', views.checkout,name = 'checkout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
]