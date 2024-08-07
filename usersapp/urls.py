from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='base.html'), name="logout"),

    # path('logout/', views.logout_view, name='logout'),
    # Other URL patterns
]