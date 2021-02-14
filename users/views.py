from django.shortcuts import render,redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def register(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, "users/register.html", {'form': form})

def welcome(request):
    return render(request, "users/welcome.html")
