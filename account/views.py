from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import Login_User
from django.views.generic import View, CreateView
from .forms import RegisterForm, Login_User, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
User = get_user_model()
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _




class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = RegisterForm


    def get_success_url(self):
        return reverse("login")





def user_login(request):
    form = Login_User()
    if request.method == 'POST':
        form = Login_User(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # messages.info(request, "Royhatdan otdingiz.")
                return redirect('shop_product:home_page')
            form.add_error('password', "Username va/yoki parol noto'g'ri. ")

    return render(request, 'account/login.html', {'form': form})



def edit_profil(request):
    prof = User.objects.get(id=request.user.id)
    form = ProfileForm(instance=prof)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            return redirect("account:profil")
    context = {
        'form': form,

    }
    return render(request, 'account/update_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parolingiz muvaffaqiyatli yangilandi!')
            return redirect('account:profil')
        else:
            messages.error(request, 'Iltimos, pastdagi xatoni tuzating.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })


def profil(request):
    user_profile = User.objects.get(id=request.user.id)
    context = {
        "user_profile": user_profile
    }
    return render(request, 'account/profil.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdinggiz.")
    return redirect('/')