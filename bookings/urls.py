from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('accommodations/', views.AccommodationListView.as_view(), name='accommodation_list'),
    path('accommodations/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/create/', views.accommodation_create, name='accommodation_create'),
    path('accommodations/<int:pk>/book/', views.book_accommodation, name='book_accommodation'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
]