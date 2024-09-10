from django.urls import path
from .views import base, custom_login_view, category_breakdown_view

urlpatterns = [
    path('', base, name="home"),
    path('customlogin', custom_login_view, name="custom_login"),
    path('category-breakdown/', category_breakdown_view, name='category_breakdown'),
]
