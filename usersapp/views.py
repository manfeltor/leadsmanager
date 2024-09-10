from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomPasswordChangeForm
from .forms import UserEditForm
from django.contrib.auth import update_session_auth_hash

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Usuario y/o contraseña inválidos'
            return render(request, 'landing.html', {'login_error': error_message})  # Pass the error message
    return redirect('home')

@login_required
def user_list_view(request):
    users = CustomUser.objects.all()  # Retrieve all users
    return render(request, 'list_users.html', {'users': users})


@login_required
def create_user_view(request):
    if not request.user.is_superuser:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or another relevant page after creating the user
    else:
        form = CustomUserCreationForm()

    return render(request, 'create_user.html', {'form': form})


def unauthorized_view(request):
    return render(request, 'unauthorized.html')

@login_required
def update_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Su perfil ha sido correctamente actualizado.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrije los problemas listados.')
    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Su contraseña fue cambiada de forma correcta.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrija los problemas listados.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'user_pass_edit.html', {'form': form})

@login_required
def profile_detail_view(request):
    # Get the logged-in user's information
    user = request.user

    return render(request, 'profile_detail.html', {'user': user})

@login_required
def user_edit_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if not request.user.is_management:
        return redirect('unauthorized')  # You can create an unauthorized view or redirect to home

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})

@staff_member_required  # Only allow staff/admins to delete users
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('list_users')

    return render(request, 'delete_user_confirmation.html', {'user': user})