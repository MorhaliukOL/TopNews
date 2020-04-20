from django.shortcuts import reverse, render
from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm

User = get_user_model()


class UserRegistration(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Email Verification.'
            domain = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verif_link = str(domain) + reverse('verify_email', args=[uid, token])
            message = f"Hello! You registered on {domain}. " \
                      f"To complete registration confirm your email, " \
                      f"visiting this link:\n {verif_link}"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Confirmation link was sent on your email.\
                                Please confirm your email address to complete registration')
        else:
            return HttpResponse('Invalid data')


class EmailVerification(View):
    """Verify user's email"""
    def get(self, request, uid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return render(request, 'users/email_verification.html')
        else:
            return HttpResponse('Activation link is invalid!')