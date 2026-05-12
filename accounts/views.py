from django.shortcuts import render,redirect
from .forms import MyUserForm
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # 🔐 correct
            user.save()

            login(request, user)  # log in
            messages.success(request, "Registered successfully!")
            return redirect('index')  #redirect

        else:
            messages.error(request, "Something went wrong")

    else:
        form = MyUserForm()

    return render(request, 'accounts/register.html', {"form": form})


def login_user(request):
    if request.method == 'POST':

        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,"Logged in succesfully")
            return redirect ('index')
        else:

            messages.warning(request,"Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request,'accounts/login.html',{'form':form})



def logout_user(request):
    logout(request)
    messages.info(request,"Logged out successfully.")
    return redirect('index')
