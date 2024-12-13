from django.urls import path,include

from . import views
from  .views import *
from django.contrib import admin
#from mpesa.urls import mpesa_urls
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home , name='home'),
    path('register/', register, name='register'),
    path('login/',login_user,name ='login'),
    path('home/billing_info/login/',login_user,name ='login1'),
    path('daraja/stk_push',stk_push_callback,name='stk_push_callback'),
    path('index/', index, name='index'),
    path('login/home/billing_info/', billing_info, name='billing_info2'),
    path('home/billing_info/', billing_info, name='billing_info1'),
    path('register/home/billing_info/', billing_info, name='billing_info'),
    path('billing/', billing, name='billing'),
    # path('login/', my_login_view, name='my_login'),

    path('book-parking/', views.book_parking, name='book_parking'),
    path('register-parking-spot/', views.register_parking_spot, name='register_parking_spot'),
     path('view-bookings/', views.view_bookings, name='view_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('mpesa/payment/', views.billing, name='mpesa_payment'),  # View to process Mpesa payment
    path('mpesa/callback/', views.mpesa_payment_callback, name='mpesa_callback'),
    path('home/billing_info/', views.billing_info, name='billing_info'),




]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







