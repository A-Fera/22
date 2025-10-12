from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),

    # Public guide views
    path('guides/', views.GuideListView.as_view(), name='guide_list'),
    path('guides/<int:pk>/', views.guide_detail, name='guide_detail'),

    # Admin-only guide management
    path('admin/guides/create/', views.guide_create, name='guide_create'),
    path('admin/guides/<int:pk>/update/', views.guide_update, name='guide_update'),
    path('admin/guides/<int:pk>/delete/', views.guide_delete, name='guide_delete'),
]