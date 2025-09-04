from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password1", "password2"]
        labels = {
            "email": "E-mail",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email", "required": "required"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя", "required": "required"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Фамилия"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "+7", "required": "required"}
        )
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Пароль",
            "required": "required"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Подтверждение пароля",
            "required": "required"
        })


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
        REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Имя"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Фамилия"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "+7"}
        )


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    fields = ["email", "password"]

    labels = {
        "email": "E-mail",
        "password": "Пароль",
    }

    error_messages = {
        'invalid_login': "Неверный email или пароль. Проверьте правильность введенных данных.",
        'email_not_verified': "Ваш email не подтвержден. Пожалуйста, проверьте вашу почту.",
        'banned': "Ваша учетная запись заблокирована."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Пароль"


    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['email_not_verified'],
                code="email_not_verified",
            )
        if user.is_banned:
            raise forms.ValidationError(
                self.error_messages['banned'],
                code="banned",
            )


class PasswordRecoveryRequestForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]
        REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            return email
        except Exception:
            raise forms.ValidationError("Пользователя с таким email не существует")


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Новый пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Новый пароль"}
        )
