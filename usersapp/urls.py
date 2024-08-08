from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('listusers/', login_view, name='list_users'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # path('logout/', views.logout_view, name='logout'),
    # Other URL patterns
]