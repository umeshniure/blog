from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template import context
from django.urls import reverse_lazy
from django.views import generic
from .forms import EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm


# Create your views here.
# class UserRegisterView(generic.CreateView):
#     form_class = UserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('Login')


def must_authenticate_view(request):
    if not request.user.is_authenticated:
        return render(request, 'must_authenticate.html', {})
    else:
        messages.info(request, 'Hurray! You are already logged in.')
        return redirect('home')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are successfully logged out! Please login to view blogs.')
    return redirect('home')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Welcome! to the world of blogs.')
            return redirect('/')
        else:
            messages.info(request, 'Invalid Username or Password!')
            return redirect('login')

    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists!')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                username=username, password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Password didn't match!")
            return redirect('register')

        return redirect('/')
    else:
        return render(request, 'register.html')


@login_required
def usereditview(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # context['success_message'] = "Updated!"
            messages.success(request, f'Congratulations! Your account has been successfully updated.')
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)

# class UserEditView(generic.UpdateView):
#     pass
# form_class = EditProfileForm
# template_name = 'accounts/edit_profile.html'
# success_url = reverse_lazy('home')
#
# def get_object(self):
#     return self.request.user
