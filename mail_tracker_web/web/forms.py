from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class SendEmailForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())
