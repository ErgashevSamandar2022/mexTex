from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Bu joyda `views.signup` dan foydalanamiz

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]