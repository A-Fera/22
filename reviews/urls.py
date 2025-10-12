from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('destination/<int:destination_pk>/create/', views.destination_review_create, name='destination_review_create'),
    path('accommodation/<int:accommodation_pk>/create/', views.accommodation_review_create, name='accommodation_review_create'),
    path('<str:review_type>/<int:review_pk>/', views.review_detail, name='review_detail'),
]