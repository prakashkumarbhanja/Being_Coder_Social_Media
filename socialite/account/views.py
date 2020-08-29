from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,  login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from .forms import Create_User_Form
from django.contrib.auth.models import User

from .tokens import account_activation_token


def sign_up_view(request):
    context = {}
    if request.method == 'GET':
        form = Create_User_Form()
        context['form'] = form
        return render(request, 'account/signup.html', context)
    # return render(request, 'account/signup.html')

    elif request.method == 'POST':
        form = Create_User_Form(request.POST or None)
        if form.is_valid():
           email = request.POST.get('email')
           username = request.POST.get('username')
           first_name = request.POST.get('first_name')
           password = request.POST.get('password')
           confirm_password = request.POST.get('confirm_password')

           if password == confirm_password:
               user = User.objects.create_user(email=email, username=username, first_name=first_name, password=password)
               user.is_active = True
               user.save()

               # current_site = get_current_site(request)
               # mail_subject = 'Activate your Socialite account.'
               # message = render_to_string('account/acc_active_email.html', {
               #     'user': user,
               #     'domain': current_site.domain,
               #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               #     'token': account_activation_token.make_token(user),
               # })
               # to_email = email
               # send_mail(
               #     mail_subject, message,settings.EMAIL_HOST_USER, [to_email]
               # )
               # # email.send()
               # return HttpResponse('Please confirm your email address to complete the registration')

               # send_mail(
               #     'Activate your Account',
               #     'Below have the link to activate our account, use it to activate',
               #     settings.EMAIL_HOST_USER,
               #     [email],
               #     fail_silently=True,
               # )

               # return HttpResponseRedirect(redirect_to='')
        context['form'] = form
        return render(request, 'account/signup.html', context)
    return render(request, 'account/signup.html')


#--------------Activate User---------------
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.sis_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


#----------------------------Login---------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        print(user, '----------------------')

        if user is not None:
            if user.is_active():
                login(request, user)
                return redirect('/userpage/homepage/')
        else:
            return HttpResponse('Invalid Credentials')
    return redirect('/login/')

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('sign_up')


