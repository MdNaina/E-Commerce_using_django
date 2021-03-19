from django.urls import path
from . import views
import re

urlpatterns = [
    path('', views.index,name="store"),
    path('cart/', views.cart,name="cart"),
    path('checkout/', views.checkout,name="checkout"),
    path('update_item/', views.update_item, name='update_item'),
    path('orderProcessed/', views.orderProcessed, name='orderProcessed'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
    path('addFeedback/', views.addFeedback, name='addFeedback'),
    path('viewproduct/<productId>/', views.showProduct, name='viewproduct'),
    path('catagory/<str:category>/', views.catagories, name='category')
]