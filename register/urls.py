from django.urls import path
from . import views
urlpatterns = [
    # path('userCreation/',views.userCreation, name= "userCreation"),
    path('register/',views.register, name = "register"),
    path('otp/', views.otp, name= 'otp'),    
]