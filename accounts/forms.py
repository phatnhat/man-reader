from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, PasswordChangeForm
from .models import User, UserProfile
from django import forms
from django.forms.widgets import TextInput, CheckboxInput, PasswordInput

class LoginForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['email', 'password', 'remember_me']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = TextInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'name': 'email',
            'placeholder': 'name@email.com'
        })
        self.fields['password'].widget = PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Password'
        })
        self.fields['remember_me'].widget = CheckboxInput(attrs={
            'id': 'remember',
            'class': 'custom-control-input',
            'name': 'remember'        
        })


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={
            'id': 're-name',
            'class': 'form-control',
            'name': 'name',
            'placeholder': 'Your name'
        })
        self.fields['email'].widget = TextInput(attrs={
            'id': 're-email',
            'class': 'form-control',
            'name': 'email',
            'placeholder': 'name@email.com'
        })
        self.fields['password'].widget = PasswordInput(attrs={
            'id': 're-password',
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Password'
        })
        self.fields['confirm_password'].widget = PasswordInput(attrs={
            'id': 're-confirmpassword',
            'class': 'form-control',
            'name': 're-password',
            'placeholder': 'Confirm Password'
        })

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
        

class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('name', 'current_password', 'new_password', 'confirm_new_password')


class ForgotForm(PasswordResetForm):    
    def __init__(self, *args, **kwargs):
        super(ForgotForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = TextInput(attrs={
            'id': 'forgot-email',
            'class': 'form-control',
            'name': 'email',
            'placeholder': 'name@email.com'
        })

    def clean_email(self):
        cleaned_data = super(ForgotForm, self).clean()
        email = cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if not exists:
            raise forms.ValidationError("Your email not exist.") 
        return email
    

class ResetPasswordForm(forms.Form): 
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())   

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = TextInput(attrs={
            'id': 'reset-email',
            'class': 'form-control',
            'name': 'email',
            'placeholder': 'name@email.com',
            'disabled': '',
        })
        self.fields['password'].widget = PasswordInput(attrs={
            'id': 'reset-password',
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Password'
        })
        self.fields['password_confirmation'].widget = PasswordInput(attrs={
            'id': 'reset-password_confirmation',
            'class': 'form-control',
            'name': 'password_confirmmation',
            'placeholder': 'Password Confirmation'
        })

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Password confirmatinon is invalid.") 


class UserCreationForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'is_active','is_superuser', 'is_staff', 
                'groups', 'user_permissions', 'last_login', 'date_joined')
        