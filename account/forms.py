from django import forms
from shop_settings.validators import PhoneValidator
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "phone")
        field_classes = {'username': UsernameField}



class Login_User(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


# from django.contrib.auth.forms import PasswordChangeForm
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'image']



class ProfileImage(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'parolga mos kelmaslik': ("Ikkita parol maydoni mos kelmadi."),
    }
    new_password1 = forms.CharField(label=("Yangi Parol"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Yangi parolni tasdiqlash"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        "parol_ noto'g'ri": ("Sizning eski parolingiz noto'g'ri kiritilgan. "
                                "Iltimos, uni qayta kiriting."),
    })
    old_password = forms.CharField(label=("Eski parol"),
                                   widget=forms.PasswordInput)