from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required


from transaction.models import Transaction
from .models import User
from .forms import UserRegistrationForm, UserLoginForm


@login_required(login_url='user:login')
def profile(request):
    profile = request.user
    expenses = Transaction().monthly_expenses(request)
    income = Transaction().monthly_income(request)
    print(expenses)
    context = {
        'profile': profile,
        'monthly_expenses': expenses,
        'monthly_income': income,
    }
    return render(request, 'user/profile.html', context=context)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("transaction:main")
    template_name = 'user/register.html'


    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(self, email=email, password=password)

            if user is not None:
                login(self.request, user=user)

        return response


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            if user is not None and user.check_password(password):
                login(request, user)
                return redirect(reverse_lazy('user:profile'))

    form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('transaction:main')