from .form import CreateUserForm,ChangeUserForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Change(generic.CreateView):
    form_class = ChangeUserForm
    success_url = reverse_lazy('/')
    template_name = 'change.html'