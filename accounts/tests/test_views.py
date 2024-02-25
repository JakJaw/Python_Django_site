from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Account, Myaccountmanager, UserProfile
import json


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.forgotPassword_url = reverse('forgotPassword')
        self.resetPassword_url = reverse('resetPassword')
        self.dashboard_url = reverse('dashboard')
    
    def tests_register_GET(self):
        response = self.client.get(self.register_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        
    def tests_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def tests_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)
       
    def tests_forgot_password_GET(self):
        response = self.client.get(self.forgotPassword_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/forgotPassword.html')

    def tests_reset_password_GET(self):
        response = self.client.get(self.resetPassword_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/resetPassword.html')
    
    def test_dashboard_GET(self):
        response = self.client.get(self.dashboard_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')


class LoginTest(TestViews):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
