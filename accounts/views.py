from django.shortcuts import render,redirect
from .forms import MyUserForm,EditProfile
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def register_user(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()

            login(request, user)  # log in
            messages.success(request, "Registered successfully!")
            return redirect('index')  #redirect

        else:
            print(form.errors)
            messages.error(request, "Something went wrong")

    else:
        form = MyUserForm()

    return render(request, 'accounts/register.html', {"form": form})


def login_user(request):
    if request.method == 'POST':

        form = AuthenticationForm(request,data=request.POST)
        #print(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,"Logged in succesfully")
            return redirect ('index')
        else:
            #print(form.errors)
            messages.warning(request,"Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})



def logout_user(request):
    logout(request)
    messages.info(request,"Logged out successfully.")
    return redirect('index')

@login_required
def edit_profile(request):
    user=request.user
    
    if request.method == 'POST':
        form = EditProfile(request.POST,instance=user)
        
        if form.is_valid():

            form.save()
            messages.success(request, "changes saved successfully!")
            return redirect('dashboard')
        else:
            messages.error(request,form.errors)
    else:
        form = EditProfile(instance=user)   
    return render(request,'accounts/edit.html',{"form":form})


def user_Profile(request):
    
    return render(request,'accounts/user_profile.html')

