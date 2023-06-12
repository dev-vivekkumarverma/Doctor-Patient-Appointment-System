from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('user_registration_view'), {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com','confirm_password':'testpass'})
    assert response.status_code == 302  # Check for successful redirect
    assert User.objects.filter(username='testuser').exists()  # Check if user is added to the database

@pytest.mark.django_db
def test_user_login(client):
    User.objects.create_user(username='testuser', password='testpass')
    response = client.post(reverse('user_login_view'), {'username': 'testuser', 'password': 'testpass'})
    print("response: ",response.status_code)
    assert response.status_code == 200  # Check for successful redirect
    assert '_auth_user_id' in client.session  # Check if user is authenticated

@pytest.mark.django_db
def test_invalid_user_login(client):
    response = client.post(reverse('user_login_view'), {'username': 'testuser', 'password': 'wrongpass'})
    assert response.status_code == 302  # Check for unsuccessful login attempt
    assert '_auth_user_id' not in client.session  # Check if user is not authenticated

@pytest.mark.django_db
def test_user_logout(client):
    User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    response = client.get(reverse('user_logout_view'))
    assert response.status_code == 302  # Check for successful redirect
    assert '_auth_user_id' not in client.session  # Check if user is logged out

def test_access_restriction(client):
    response = client.get(reverse('all_doctor_view'))
    assert response.status_code == 302  # Check for redirect to login page
    assert 'login' in response.url  # Check if redirected to login page URL
