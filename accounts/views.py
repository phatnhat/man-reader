from django.shortcuts import render, redirect, get_object_or_404
from .models import Avatar, User, UserProfile, UserReading, ContinueReading, Notification
from django.contrib import messages, auth
from django.http import HttpResponse, JsonResponse
import json
from .forms import LoginForm, RegisterForm, ProfileForm, ForgotForm, ResetPasswordForm
from django.http import QueryDict
from .utils import send_verification_email, send_reset_password_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from book.models import Book, Chapter, ReadingList
from django.contrib.auth.decorators import login_required
from book.utils import sort_by, sort_list
from book.models import Subquery, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def login(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            serialized_form_data = request.POST.get('form')
            form_data = QueryDict(serialized_form_data)
            email = form_data.get('email')
            password = form_data.get('password')
            remember_me = form_data.get('remember')

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                if not remember_me:
                        request.session.set_expiry(0)
                return HttpResponse(json.dumps({
                    'errorCode': 1, 'message': 'You are now logged in.',
                }))
            else:
                return HttpResponse(json.dumps({
                    'errorCode': 0, 'message': 'Invalid login credentials.',
                }))
        except:
            return HttpResponse(json.dumps({
                    'errorCode': 0, 'message': 'Something went wrong. Please try again!',
                }))
        
    return redirect('home')

def register(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            form_data = QueryDict(request.POST['form'].encode('ASCII'))
            form = RegisterForm(form_data)
            if form.is_valid():
                password = form.cleaned_data['password']
                user = form.save(commit=False)
                user.set_password(password)
                user.is_active = False
                user.save()

                mail_subject = 'Please activate your account'
                email_template = 'accounts/emails/account-verification-email.html'
                send_verification_email(request, user, mail_subject, email_template)

                return HttpResponse(json.dumps({
                    'errorCode': 1, 'message': 'Please check your email to activate your account!',
                }))
            else:
                error = [item[1] for item in form.errors.items()][0]
                return HttpResponse(json.dumps({
                    'errorCode': 0, 'message': error,
                }))
        except:
            return HttpResponse(json.dumps({
                    'errorCode': 0, 'message': 'Something went wrong. Please try again!',
                }))
        
    return redirect('home')
        
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('home')
    else:
        return redirect('home')
    

def forgot(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            form_data = QueryDict(request.POST['form'].encode('ASCII'))
            form = ForgotForm(form_data)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)

                mail_subject = 'Reset Password Notification'
                email_template = 'accounts/emails/password-reset-email.html'
                send_reset_password_email(request, user, mail_subject, email_template)

                return HttpResponse(json.dumps({'errorCode': 1, 'message': 'We have emailed your password reset link!',}))
            else:
                error = [item[1] for item in form.errors.items()][0]
                return HttpResponse(json.dumps({'errorCode': 0, 'message': error,}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'errorCode': 0, 'message': 'Something went wrong. Please try again!',}))
        
    return redirect('home')


def password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form_data = QueryDict(request.POST['form'].encode('ASCII'))
            form = ResetPasswordForm(form_data)
            if form.is_valid():
                new_password = form.cleaned_data['password']
                user.set_password(new_password)
                user.save()
                return HttpResponse(json.dumps({'errorCode': 1, 'message': 'Your password has been reset!',}))
            else:
                error = [item[1] for item in form.errors.items()][0]
                return HttpResponse(json.dumps({'errorCode': 0, 'message': error,}))
        return HttpResponse(json.dumps({'errorCode': 0, 'message': 'This password reset token is invalid.',}))
    else:
        form = ResetPasswordForm(request.GET)

        context = {
            'reset_form': form,
        }

        return render(request, 'accounts/password-reset-confirm.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')

@csrf_exempt
def profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']
                confirm_new_password = form.cleaned_data['confirm_new_password']
                email = request.user.email
                user = form.save(commit=False)
                if current_password and new_password and confirm_new_password:
                    password_match = check_password(current_password, request.user.password)
                    if not password_match:
                        return JsonResponse({'status': False, 'message': 'Current password is invalid.'})
                    if new_password != confirm_new_password:
                        return JsonResponse({'status': False, 'message': 'Confirm password is invalid.'})
                    user.set_password(new_password)
                    # request.session.set_expiry(0)
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                user.save()
                return JsonResponse({'status': True, 'message': 'Update profile successfully.'})
            else:
                error = [field for field in form.errors.items()][0]
                return JsonResponse({'status': False, 'message': error})
        except Exception as e:
            return JsonResponse({'status': False, 'message': f'Something went wrong. Please try again! {e}',})
    
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'accounts/profile.html', context)
    return redirect('home')


def continue_reading(request):
    if request.user.is_authenticated:
        continue_reading_list = ContinueReading.objects.filter(user=request.user).order_by('-created_at')

        paginator = Paginator(continue_reading_list, 16)
        page_number = request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'accounts/continue-reading.html', context)
    return redirect('home')


@csrf_exempt
def change_avatar(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            avatar_id = request.POST.get('avatar_id')
            avatar = Avatar.objects.get(pk=avatar_id)
            profile = UserProfile.objects.get(user=request.user)
            profile.avatar = avatar
            profile.save()
            return JsonResponse({'status': True, 'message': 'Update profile successfully.',})
        except:
            return JsonResponse({'status': False, 'message': 'Something went wrong. Please try again!',})
    return redirect('home')


def reading_list(request):
    if request.user.is_authenticated:
        type = request.GET.get('type', '')
        sort = request.GET.get('sort', 'default')
        sort_name = [s['name'] for s in sort_list() if s['slug'] == sort][0]
        if type == '':
            user_reading = request.user.users_reading.all() #UserReading.objects.filter(user=request.user)
        else:
            type = int(type)
            reading_list = get_object_or_404(ReadingList, pk=type)
            user_reading = request.user.users_reading.filter(reading_list=reading_list).all()
        books = Book.objects.filter(books_reading__in=user_reading).annotate(reading_list=F("books_reading__reading_list"))
        books = books.order_by('-created_at') if sort == 'default' else sort_by(books, sort)

        paginator = Paginator(books, 16)
        page_number = request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'user_reading': user_reading,
            'books': books,
            'type': type,
            'sort_name': sort_name,
            'sort': sort,
            'sort_list': sort_list(),
            'page_obj': page_obj,
        }
        return render(request, 'accounts/reading-list.html', context)
    return redirect('home')


@csrf_exempt
def add_reading_list(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            book_id, action_type, page = request.POST.dict().values()

            try: user_reading = UserReading.objects.get(user=request.user, book__id=book_id)
            except(UserReading.DoesNotExist): user_reading = None
            try: 
                if int(action_type) != 0: reading_list = ReadingList.objects.get(pk=action_type)
            except(ReadingList.DoesNotExist): return JsonResponse({'status': False, 'message': 'Reading List does not exist.',})
            try: book = Book.objects.get(pk=book_id)
            except(Book.DoesNotExist): return JsonResponse({'status': False, 'message': 'Book does not exist.',})

            if user_reading:
                if int(action_type) == 0:
                    user_reading.delete()
                    msg = "This book has been removed from Reading List."
                else:
                    user_reading.reading_list = reading_list
                    user_reading.save()
                    msg = "This book has been added from Reading List."
            else:
                user_reading = UserReading.objects.create(book=book, user=request.user, reading_list=reading_list,)
                user_reading.save()
                msg = "This book has been added from Reading List."
            context = {
                    'reading_list': ReadingList.objects.all(),
                    'book': book,
                    'action_type': int(action_type),
                    'page': page,
                }
            html = render_to_string('includes/reading-list-info.html', context)
            return JsonResponse({'status': True, 'message': msg, 'html': html})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Something went wrong. Please try again!',})
    return redirect('home')


@csrf_exempt
def log_reading(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            book_id, chapter_id = request.POST.dict().values()
            continue_reading = ContinueReading.objects.filter(user=request.user, book__id=book_id)

            try: book = Book.objects.get(pk=book_id)
            except(Book.DoesNotExist): return JsonResponse({'status': False, 'message': 'Book does not exist.',})
            try: chapter = Chapter.objects.get(pk=chapter_id)
            except(Chapter.DoesNotExist): return JsonResponse({'status': False, 'message': 'Chapter does not exist.',})

            if continue_reading:
                continue_reading = continue_reading.first()
                continue_reading.chapter = Chapter.objects.get(pk=chapter_id)
            else:
                continue_reading = ContinueReading(user=request.user, book=book, chapter=chapter)
            continue_reading.save()

            return JsonResponse({'status': True, 'message': 'Success'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Something went wrong. Please try again!',})
    return redirect('home')

@csrf_exempt
def remove_continue_reading(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            if request.user.is_authenticated:
                id = request.POST.get('id')
                try: continue_reading = ContinueReading.objects.get(pk=id)
                except(ContinueReading.DoesNotExist): return JsonResponse({'status': False, 'message': 'Continue Reading does not exist.',})
                continue_reading.delete()
                return JsonResponse({'status': True, 'message': "Remove continue reading success."})
            else:
                return JsonResponse({'status': False, 'message': 'Need authenticate.',})
        except:
            return JsonResponse({'status': False, 'message': 'Something went wrong. Please try again!',})
    return redirect('home')


def continue_reading_home(request):
    try:
        if request.user.is_authenticated:
            continue_reading_list = ContinueReading.objects.filter(user=request.user).order_by('-created_at')[:20]
                #books = Book.objects.filter(books_continue_reading__in=continue_reading).annotate(chapter=F("books_continue_reading__chapter__chap"))
            return JsonResponse({'status': True, 'html': render_to_string('includes/book-continue.html', {'continue_reading_list': continue_reading_list})})
        else:
            return JsonResponse({'status': False})
    except Exception as e:
        return JsonResponse({'status': False})
    return redirect('home')
    

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).all().order_by('-created_at')

        paginator = Paginator(notifications, 16)
        page_number = request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'notifications': notifications,
            'page_obj': page_obj,
        }
        return render(request, 'accounts/notifications.html', context)
    return redirect('home')


@csrf_exempt
def notification_seen_all(request):
    try:
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(user=request.user)
            notifications.update(mark=True)
            return JsonResponse({'status': True, 'message': 'All notifications have been successfully marked.',})
    except:
        return JsonResponse({'status': False, 'message': 'Something went wrong. Please try again!',})
    return redirect('home')