from .models import Avatar, AvatarHashtag, Notification
from .forms import LoginForm, RegisterForm, ForgotForm

def get_hashtag(request):
    hashtags = AvatarHashtag.objects.all()
    return dict(hashtags=hashtags)

def get_form(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    forgot_form = ForgotForm()
    return dict(login_form=login_form,register_form=register_form,forgot_form=forgot_form)

def get_count_notifications(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, mark=False).all().count()
        return dict(noti_count=count)
    return dict(noti_count=None)