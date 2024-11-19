from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, get_user_model
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)
 # Modificado
from django.urls import reverse  # Añadido
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView) 
from django.contrib.auth.mixins import UserPassesTestMixin

User = get_user_model()

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm 
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tasks:index")

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserDetail(OnlyYouMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_pw)
        if user is not None:
            login(self.request, user)
        return response
    
class UserUpdate(OnlyYouMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})
    
class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'
 
class UserDelete(OnlyYouMixin, DeleteView):
    model = User
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

# Create your views here.

