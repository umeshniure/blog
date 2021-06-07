from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User


# Create your views here.
# class UserRegisterView(generic.CreateView):
#     form_class = UserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('Login')


def must_authenticate_view(request):
    return render(request, 'must_authenticate.html', {})


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out! Please log in to continue.')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Welcome to the world of blogs!')
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
            print("password not matching!")
            messages.info(request, "Password didn't match!")
            return redirect('register')

        return redirect('/')
    else:
        return render(request, 'register.html')
