from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import register, login, logout, dashboard, activate, forgotPassword, resetpassword_validate, resetPassword, my_orders, edit_profile, change_password, order_detail

class TestUrls(SimpleTestCase):
    
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)
        
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout)
        
    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)
    
    def test_activate_url_resolves(self):
        url = reverse('activate', args=['uidb64','token'])
        self.assertEqual(resolve(url).func, activate)
    
    def test_forgotPassword_url_resolves(self):
        url = reverse('forgotPassword')
        self.assertEqual(resolve(url).func, forgotPassword)
    
    def test_resetPassword_url_resolves(self):
        url = reverse('resetPassword')
        self.assertEqual(resolve(url).func, resetPassword)

    def test_resetpassword_validate_url_resolves(self):
        url = reverse('resetpassword_validate', args=['uidb64','token'])
        self.assertEqual(resolve(url).func, resetpassword_validate)
        
    def test_my_orders_url_resolves(self):
        url = reverse('my_orders')
        self.assertEqual(resolve(url).func, my_orders)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)
        
    def test_change_password_url_resolves(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_order_detail_url_resolves(self):
        url = reverse('order_detail', args=["order_id"])
        self.assertEqual(resolve(url).func, order_detail)