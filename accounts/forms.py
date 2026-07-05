from django import forms
from .models import MyUser


class MyUserForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ['username','fullname','email','password']
    
    

class EditProfile(forms.ModelForm):
    

    class Meta:
        model = MyUser
        fields = ['username','fullname','email','bio']
        

class PasswordForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput
    )
    
    password_again = forms.CharField(
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ['password','password_again']
        
        
    if password != password_again:
        print()

        
    
