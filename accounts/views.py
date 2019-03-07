from .form import CreateUserForm,ChangeUserForm,UserCreationMultiform
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect


class SignUp(generic.CreateView):
    form_class = UserCreationMultiform
    success_url = reverse_lazy('singup_success')
    template_name = 'signup.html'

    def form_valid(self, form):
    	user=form['user'].save()
    	profile = form['profile'].save(commit=False)
    	profile.user=user
    	profile.save()
    	return redirect(self.success_url)


class Change(generic.CreateView):
    form_class = ChangeUserForm
    success_url = reverse_lazy('/')
    template_name = 'change.html'


class SignUp_success(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'singup_success.html'