from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.object.filter(username__iexact = username)
        if user.exists():
            raise forms.ValidationError("This username already exists")
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.object.filter(email__iexact = email)
        if user.exists():
            raise forms.ValidationError("This email is already used")
        return self.cleaned_data.get('email')
    
    def clean_password(self):
        pw = self.cleaned_data.get('password')
        c_pw = self.data.get('confirm_password')
        if pw != c_pw:
            raise forms.ValidationError("passwords do not match")
        return self.cleaned_data.get('password')



class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.object.filter(username__iexact = username).exclude(pk = self.instance.pk)
        if user.exists():
            raise forms.ValidationError("This username already exists")
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.object.filter(email__iexact = email).exclude(pk = self.instance.pk)
        if user.exists():
            raise forms.ValidationError("This email is already used")
        return self.cleaned_data.get('email')
    
    def change_password(self):
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_pw = self.data['new_password']
            confirm_pw = self.data['confirm_password']
            if new_pw != '' and confirm_pw != '':
                if new_pw != confirm_pw:
                    raise forms.ValidationError("Passwords do not match")
                else:
                    self.instance.set_password(new_pw)
                    self.instance.save()
    def clean(self):
        self.change_password()

class ProfilePictureUpdateForm(forms.Form):
    profile_picture = forms.ImageField(required=True)
