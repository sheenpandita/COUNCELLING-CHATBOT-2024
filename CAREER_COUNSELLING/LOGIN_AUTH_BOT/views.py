from django.shortcuts import render, redirect
from django.contrib import messages
from LOGIN_AUTH_BOT.forms import ProfileUser
from LOGIN_AUTH_BOT.models import User
from django.contrib.auth.hashers import make_password, check_password




def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = ProfileUser(request.POST)
        if form.is_valid():
            # Hash the password before saving
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = ProfileUser()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                messages.success(request, f'Welcome {user.name}, you have successfully logged in!')
                return redirect('dashboard')  # Redirect to a dashboard or homepage
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist. Please register first.')
    return render(request, 'login.html')



def user_logout(request):
    if 'user_id' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out successfully.')
    return redirect('login')



def dashboard(request):
    if 'user_id' in request.session:
        return render(request, 'dashboard.html', {'user_name': request.session['user_name']})
    else:
        return redirect('login')
