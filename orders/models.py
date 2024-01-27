from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    payment_id = models.CharField(max_length=100, verbose_name=_('Payment ID'))
    payment_method = models.CharField(max_length=100, verbose_name=_('Payment method'))
    amount_paid = models.CharField(max_length=100, verbose_name=_('Amount paid'))
    status = models.CharField(max_length=100, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
    
    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Payment'))
    order_number = models.CharField(max_length=20, verbose_name=_('Order number'))
    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    phone = models.CharField(max_length=15, verbose_name=_('Phone'))
    email = models.EmailField(max_length=50, verbose_name=_('Email'))
    address_line_1 = models.CharField(max_length=50, verbose_name=_('Address line 1'))
    address_line_2 = models.CharField(max_length=50, blank=True, verbose_name=_('Address line 2'))
    country = models.CharField(max_length=50, verbose_name=_('Country'))
    state = models.CharField(max_length=50, verbose_name=_('State'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    order_note = models.CharField(max_length=100, blank=True, verbose_name=_('Order note'))
    order_total = models.FloatField(verbose_name=_('Order total'))
    tax = models.FloatField(verbose_name=_('Tax'))
    status = models.CharField(max_length=10, choices=STATUS, default='New', verbose_name=_('Status'))
    ip = models.CharField(blank=True, max_length=20, verbose_name=_('IP'))
    is_ordered = models.BooleanField(default=False, verbose_name=_('Is ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'))
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Payment'))
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variations = models.ManyToManyField(Variation, blank=True, verbose_name=_('Variations'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    product_price = models.FloatField(verbose_name=_('Price'))
    ordered = models.BooleanField(default=False, verbose_name=_('Ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = _('Order product')
        verbose_name_plural = _('Order products')