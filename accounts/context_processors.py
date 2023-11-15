from .models import Avatar, AvatarHashtag
from .forms import LoginForm, RegisterForm, ForgotForm

def get_hashtag(request):
    hashtags = AvatarHashtag.objects.all()
    return dict(hashtags=hashtags)

def get_form(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    forgot_form = ForgotForm()
    return dict(login_form=login_form,register_form=register_form,forgot_form=forgot_form)