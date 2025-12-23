from datetime import datetime, timezone
from http import client
from django.urls import reverse
from django.test.client import Client
from core.models import CustomUser, PendingUser, Token, TokenTypes
import pytest
from django.contrib.auth.hashers import check_password 
from django.contrib.messages import get_messages
from django.contrib.auth import get_user
from django.contrib.messages.storage.base import Message

pytestmark = pytest.mark.django_db # Use the Django database for these tests

# Create your tests here.
def test_register_user(client: Client):
     url = reverse("register")  
     request_data = {   
         "username": "testuser1",
         "email": "testuser1@example.com",
         "password": "testpassword123"
     }
     response = client.post(url, data=request_data) # post request to registration view 
     assert response.status_code == 200 # expecting OK status
     pending_user = PendingUser.objects.filter(email=request_data["email"]).first() # fetch the created pending user 
     assert pending_user  # ensure the pending user was created 
     assert check_password(request_data["password"], pending_user.password) # verify password is hashed and stored correctly 

     messages = list(get_messages(response.wsgi_request)) # fetch messages from the response 
     assert len(messages) == 1 # ensure one message is present
     assert messages[0].level_tag == "success"   # ensure the message is a success message
     assert "registration successful!" in messages[0].message.lower() # check message content 

def test_register_user_duplicate_email(client: Client, user_instance):
     url = reverse("register")  
     existing_email = user_instance.email
     # Try to register another user with the same email
     response = client.post(url, data={
         "username": "testuser2",
         "email": existing_email,
         "password": "testpassword123"
     })
     assert response.status_code == 302  # expecting redirect status
     assert response.url == reverse("register")  # ensure it redirects back to registration page
     messages = list(get_messages(response.wsgi_request)) # fetch messages from the response 
     assert len(messages) == 1 # ensure one message is present
     assert messages[0].level_tag == "error"   # ensure the message is an error message
     assert "already registered" in messages[0].message.lower() # check message content 

def test_verify_account_valid_code(client: Client): 
        url = reverse("verify_account")  
        pending_user = PendingUser.objects.create( 
          email="abc@gmail.com",
          password="hashedpassword123",      
          verification_code="validcode123",
        )
        response = client.post(url, data={
            "email": pending_user.email,
            "code": pending_user.verification_code
        })
        assert response.status_code == 302  # expecting redirect status
        assert response.url == reverse("home")  # ensure it redirects to home page
        user = get_user(response.wsgi_request)
        assert user.is_authenticated  # ensure the user is logged in
        assert user.email == pending_user.email  # ensure the logged-in user email matches
        



def test_verify_account_invalid_code(client: Client):
        url = reverse("verify_account")
        pending_user = PendingUser.objects.create(
          email="abc@gmail.com",
          password="hashedpassword123",
          verification_code="validcode123",
        )
        response = client.post(url, data={
            "email": pending_user.email,
            "code": "invalidcode"
        })
        assert response.status_code == 400  # expecting bad request status
        user = get_user(response.wsgi_request)
        assert CustomUser.objects.count() == 0  # ensure no user was created
        assert not user.is_authenticated  # ensure the user is not logged in
        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "error"   # ensure the message is an error message
        assert "invalid" in messages[0].message.lower() # check message content

def test_login_valid_credentials(client: Client, user_instance, auth_user_password):
        url = reverse("login")

        response = client.post(url, data={
                "email": user_instance.email,
                "password": auth_user_password,
        })
        print(response.wsgi_request.user.is_authenticated)

        assert response.status_code == 302 # expecting redirect status
        assert response.url == reverse("home")

        # Confirm the user is actually logged in
        response = client.get(reverse("home"))
        assert response.wsgi_request.user.is_authenticated # ensure the message is a success message

def test_login_invalid_credentials(client: Client, user_instance, auth_user_password):
        url = reverse("login")
        response = client.post(url, data={
                "email": user_instance.email,
                "password": "wrongpassword",
        })
        assert response.status_code == 302 # expecting redirect status
        assert response.url == reverse("login")
        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "error"   # ensure the message is an error message
        assert "invalid email or password" in messages[0].message.lower() # check message

def test_reset_password_request(client: Client, user_instance):
        url = reverse("reset_password")
        response = client.post(url, data={
                "email": user_instance.email,
        })
        assert response.status_code == 302 # expecting redirect status
        assert Token.objects.get(user__email=user_instance.email, token_type=TokenTypes.PASSWORD_RESET)# ensure a reset token was created
        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "success"   # ensure the message is a success message
        assert "password reset instructions" in messages[0].message.lower() # check message content

def test_reset_password_request_invalid_email(client: Client):
        url = reverse("reset_password")
        response = client.post(url, data={
                "email": "nonexistent@example.com",
        })
        assert response.status_code == 302 # expecting redirect status
        assert not Token.objects.filter(user__email="nonexistent@example.com", token_type=TokenTypes.PASSWORD_RESET).first() # ensure no reset token was created
        assert response.url == reverse("reset_password")  # ensure it redirects back to reset password page

        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "error"   # ensure the message is an error message
        assert "enter a valid email" in messages[0].message.lower() # check message content

def test_reset_password_request_valid_token(client: Client, user_instance):
        # Create a valid reset token
        url = reverse("set_new_password")
        token = Token.objects.create(
            user=user_instance,
            token="validresettoken123",
            token_type=TokenTypes.PASSWORD_RESET,  
            created_at=datetime.now(timezone.utc)
        )
        
        request_data = {
        "email": user_instance.email,
        "token": token.token,
        "password1": "newsecurepassword123",
        "password2": "newsecurepassword123",
        }
        response = client.post(url, data=request_data)
        assert response.status_code == 302 # expecting redirect status
        assert response.url == reverse("login")  # ensure it redirects to login page
        assert Token.objects.filter(id=token.id).count() == 0  # ensure the token was deleted after use
        # Verify the user's password was updated        
        user_instance.refresh_from_db()
        assert user_instance.check_password(request_data["password1"])  # ensure the password was updated
        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "success"   # ensure the message is a success message
        assert "password has been reset" in messages[0].message.lower() # check message

def test_reset_password_request_invalid_token(client: Client, user_instance):
        # Create an invalid/expired reset token
        token = Token.objects.create(
            user=user_instance,
            token="validresettoken123",
            token_type=TokenTypes.PASSWORD_RESET,       
            created_at=datetime.now(timezone.utc)
        ) 
        url = reverse("set_new_password")
        request_data = {
            "email": user_instance.email,
            "token": "invalidresettoken123",
            "new_password": "newsecurepassword123",
            "confirm_password": "newsecurepassword123",
        }       
        response = client.post(url, data=request_data)
        assert response.status_code == 302 # expecting redirect status
        assert response.url == reverse("reset_password")  # ensure it redirects back to reset password

        assert Token.objects.filter(id=token.id).count() == 1  # ensure the token still exists
        messages = list(get_messages(response.wsgi_request)) # fetch messages from the response
        assert len(messages) == 1 # ensure one message is present
        assert messages[0].level_tag == "error"   # ensure the message is an error message
        assert "invalid or expired" in messages[0].message.lower() # check message