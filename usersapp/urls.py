from django.contrib.auth import views as auth_views
from django.urls import path
from .views import login_view, user_list_view, create_user_view, unauthorized_view, update_profile_view
from .views import profile_detail_view, change_password_view, user_edit_view, delete_user

urlpatterns = [
    path('login/', login_view, name='login'),
    path('listusers/', user_list_view, name='list_users'),
    path('edituser/<int:user_id>/', user_edit_view, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create_user/', create_user_view, name='create_user'),
    path('unauthorized/', unauthorized_view , name='unauthorized'),
    path('unauthorized/', unauthorized_view , name='unauthorized'),
    path('updateprofile/', update_profile_view, name='update_profile'),
    path('profile/', profile_detail_view, name='profile'),
    path('profile/change_password/', change_password_view, name='change_password'),
    # path('logout/', views.logout_view, name='logout'),
    # Other URL patterns
]