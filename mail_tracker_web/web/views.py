import socket

from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.conf import settings

from .permissions import AnonymousRequiredPermission
from .forms import RegisterForm, LoginForm, SendEmailForm
from .models import BaseUser
from .utils import parse_list_message, send_email, EstablishConnection
from .mixins import ContextMixin


class RegisterView(AnonymousRequiredPermission, FormView):
    form_class = RegisterForm
    success_url = reverse_lazy('auth:login')
    template_name = 'register.html'

    def form_valid(self, form):
        try:
            BaseUser.objects.create_user(email=form.cleaned_data.get('email'),
                                         password=form.cleaned_data.get('password'),
                                         is_active=True)
        except IntegrityError as exc:
            form.add_error('email', 'This user already exists')
            return super().form_invalid(form)

        return super().form_valid(form)


class LoginView(AnonymousRequiredPermission, FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        user_qs = BaseUser.objects.filter(email=form.cleaned_data.get('email'))

        if user_qs.exists():
            user = user_qs.first()

            if user.check_password(form.cleaned_data.get('password')):
                login(self.request, user)

                return super().form_valid(form)

        form.add_error(field=None, error='Could not authenticate with the provided credentials')

        return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('index'))


class IndexView(LoginRequiredMixin, ContextMixin, TemplateView):
    login_url = reverse_lazy('auth:login')

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        with EstablishConnection() as connection:
            connection.send(settings.POP3_LIST_COMMAND.format(request.user.email.split('@')[0]).encode('utf-8'))
            data = connection.receive()
            parsed_data = parse_list_message(data.decode('utf-8'))

            self.context = {
                'response': parsed_data[0],
                'content': parsed_data[1]
            }

        return super().get(request, *args, **kwargs)


class MessageDetailView(LoginRequiredMixin, ContextMixin, TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'message_detail.html'

    def get(self, request, *args, **kwargs):
        with EstablishConnection() as connection:
            connection.send(settings.POP3_RETRIEVE_COMMAND.format(kwargs.get('message_id')).encode('utf-8'))
            data = connection.receive()

            self.context = {
                'received_data': data.decode('utf-8'),
                'message_id': kwargs.get('message_id')
            }

        return super().get(request, *args, **kwargs)


class DeleteMessageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        with EstablishConnection() as connection:
            connection.send(settings.POP3_DELETE_COMMAND.format(
                request.user.email.split('@')[0],
                kwargs.get('message_id')).encode('utf-8'))

        return redirect('index')


class SendEmailView(LoginRequiredMixin, FormView):
    form_class = SendEmailForm
    success_url = reverse_lazy('index')
    template_name = 'send_email.html'

    def form_valid(self, form):
        sender = self.request.user.email.split('@')[0] + '@localhost.com'
        send_email(sender,
                   form.cleaned_data.get('subject'),
                   [form.cleaned_data.get('recipient')],
                   form.cleaned_data.get('content'))

        return super().form_valid(form)
