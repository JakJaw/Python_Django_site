from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#Weryfikacja konta
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        #Jeśli formularz ma wszystkie pola wypełnione
        if form.is_valid():
            #Używa czystych danych, aby pobrać wartości z request
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            # Aktywacja konta użytkownika za pomocą załącznika w emailu
            current_site = get_current_site(request)
            mail_subject = 'Prosze aktywować konto'
            mail_message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),               
            })
            email_destination = email
            send_email = EmailMessage(mail_subject, mail_message, to=[email_destination])
            send_email.send()
            
            messages.success(request, 'Wysłano link aktywacyjny na podany email')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
                
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)   


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Teraz jesteś zalogowany")
            return redirect('dashboard')
        else:
            messages.error(request, "Źle wprowadzone dane logowania")
            return redirect('login')
    
    return render(request, 'accounts/login.html')


@login_required(login_url='login') # sprawdza czy user jest zalogowany
def logout(request):
    auth.logout(request)
    messages.success(request, 'Wylogowano')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Aktywacja zakończona sukcesem')
        return redirect('login')
    else:
        messages.error(request, 'Zły link aktywacyjny')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) # sprawdza czy email jest taki jak w bazie (case sensitive)

            # Resetowanie hasła, email
            current_site = get_current_site(request)
            mail_subject = 'Resetowanie hasła'
            mail_message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),               
            })
            email_destination = email
            send_email = EmailMessage(mail_subject, mail_message, to=[email_destination])
            send_email.send()
            
            messages.success(request, 'Email resetujący hasło został wysłany')
            return redirect('login')
        else:
            messages.error(request, 'Podane konto nie istnieje')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Zresetuj swoje hasło')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Link wygasł')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password) #zapis w formacie zhaszowanym
            user.save()
            messages.success(request, 'Hasło zostało zmienione')
            return redirect('login')
        else:
            messages.error(request, 'Hasła nie są takie same!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')