from contextvars import Token
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import CustomUser, PendingUser, TokenTypes, Token
from django.contrib import messages
from django.utils.crypto import get_random_string   
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib import auth
from datetime import datetime, timezone
from common.tasks import send_email

def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("login")
        if user.check_password(password):
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")

        messages.error(request, "Invalid email or password.")
        return redirect("login")

    return render(request, "login.html")     

def logout(request: HttpRequest):   
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')  # Redirect to home page after logout  

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        cleaned_email = email.lower()
         # Here you would typically handle the registration logic,
        if CustomUser.objects.filter(email=cleaned_email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        else:
            verification_code = get_random_string(length=32)
            pending_user = PendingUser.objects.update_or_create(
                email=cleaned_email, # Ensure email uniqueness
                defaults={
                    'password': make_password(password),  # In a real app, hash the password before storing
                    'verification_code': verification_code,
                    'created_at': datetime.now(timezone.utc),  # Store the creation time
                }
            )    
            send_email(
                "Verify Your Account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context={"code": verification_code},
            )
                #send verification email logic would go here
            messages.success(request, f"Registration successful! Please check your email to verify {cleaned_email}.")
            return render(request, 'verify_account.html',context={"email": cleaned_email})
        # such as creating a PendingUser instance and sending a verification email.
        # return HttpResponse("Registration successful! Please check your email to verify your account.")

    else:
        return render(request, 'register.html')
    
def verify_account(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        code: str = request.POST["code"]
        email: str = request.POST["email"]
        pending_user: PendingUser = PendingUser.objects.filter(email=email, verification_code=code).first()   

        if pending_user and pending_user.is_valid():
            # Create the actual user account
            user = CustomUser.objects.create(
                username=pending_user.email,
                email=pending_user.email,
                # password=None,  # Set to None initially
            )
            user.set_password(pending_user.password)  # Hash and set the password
            user.save()
            # Delete the pending user entry
            pending_user.delete()
            auth.login(request,user) 
            messages.success(request, "Your account has been verified and created successfully!")
            return redirect('home')  # Redirect to home page or wherever appropriate
        else:
            messages.error(request, "Invalid or expired verification code.")
            return render(request,"verify_account.html",{"email": email}, status=400)  # Redirect back to registration or appropriate page

def reset_password(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the user exists
        try:
                user = get_user_model().objects.filter(email=email.lower()).first() # Use filter().first() to avoid exception
        except get_user_model().DoesNotExist:
                messages.error(request, "No account found with that email.")
                return render(request, "forgot_password.html")
        if user:
            # 🔴 Remove existing reset tokens
            Token.objects.filter(
                user=user,
                token_type=TokenTypes.PASSWORD_RESET
            ).delete()
            tokens, _ = Token.objects.update_or_create(
                user=user,
                token_type=TokenTypes.PASSWORD_RESET,
                defaults={  
                    'created_at': datetime.now(timezone.utc),
                    'token': get_random_string(length=64),  # Generate a new token string
                    },   
            )
            # Send password reset email
            email_data = {"email": email.lower(), "token": tokens.token}
            send_email(
                "Reset Your Password",
                [email],
                "emails/password_reset_template.html",
                email_data,
            )
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect('login')
        else:
            messages.error(request, "Please enter a valid email address.")
            return redirect('reset_password')
    else:
        return render(request, "forgot_password.html")



def reset_password_confirm(request: HttpRequest):
    email = request.GET.get('email')
    reset_token = request.GET.get('token')

    token : Token = Token.objects.filter(
        user__email=email,  
        token=reset_token,
        token_type=TokenTypes.PASSWORD_RESET
    ).first()
    print("Reset token:", token)
    if not token or not token.is_valid():
        messages.error(request, "Invalid or expired password reset token.")
        return redirect('reset_password')
    return render(request, "set_new_password_using_reset_token.html", {"email": email, "token": reset_token})

def set_new_password(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        reset_token = request.POST.get('token')
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "set_new_password_using_reset_token.html", {"email": email, "token": reset_token})

        token : Token = Token.objects.filter(
            user__email=email,  
            token=reset_token,
            token_type=TokenTypes.PASSWORD_RESET
        ).first()

        if not token or not token.is_valid():
            messages.error(request, "Invalid or expired password reset token.")
            return redirect('reset_password')

        # Update the user's password
        token.reset_user_password(new_password)
        token.delete()  # Invalidate the token after use

        messages.success(request, "Your password has been reset successfully. You can now log in with your new password.")
        return redirect('login')

    else:
        return redirect('home')