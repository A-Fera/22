from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='destination_list'),
    path('<int:pk>/', views.destination_detail, name='destination_detail'),
    path('create/', views.destination_create, name='destination_create'),
    path('<int:pk>/update/', views.destination_update, name='destination_update'),
    path('<int:destination_pk>/photo/upload/', views.photo_upload, name='photo_upload'),
]