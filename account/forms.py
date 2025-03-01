from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
import re
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + CustomUser.REQUIRED_FIELDS + ["password1","password2"]

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        # パスワードの制約を追加
        if len(password) < 8:
            raise ValidationError("パスワードは8文字以上でなければなりません。")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("パスワードには大文字のアルファベットを含める必要があります。")
        if not re.search(r'[a-z]', password):
            raise ValidationError("パスワードには小文字のアルファベットを含める必要があります。")
        if not re.search(r'[0-9]', password):
            raise ValidationError("パスワードには数字を含める必要があります。")
        return password
    
    def clean_password2(self):
        # password1 と password2 の一致を確認
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # パスワードをハッシュ化
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + ["password"]