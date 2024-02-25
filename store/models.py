from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, verbose_name=_('Product name'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    description = models.TextField(max_length=600, blank=True, verbose_name=_('Describtion'))
    price = models.FloatField(verbose_name=_('Price'))
    image = models.ImageField(upload_to='photos/products', verbose_name=_('Image'))
    stock = models.IntegerField(verbose_name=_('Stock'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is avaible'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Modification date'))
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
    
    def averageRating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews['average'])
        return avg
        
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews["count"] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):
    def kolory(self):
        return super(VariationManager, self).filter(variation_category='kolor', is_active=True) #colors
    
    def rozmiary(self):
        return super(VariationManager, self).filter(variation_category='rozmiar', is_active=True) #sizes


variation_category_choice = (
    ('kolor', 'kolor'), #color
    ('rozmiar', 'rozmiar'), #size
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variation_category = models.CharField(max_length=100, choices=variation_category_choice, verbose_name=_('Variation category'))
    variation_value = models.CharField(max_length=100, verbose_name=_('Variation value'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created_date = models.DateTimeField(auto_now=True, verbose_name=_('Creation date'))

    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
    class Meta:
        verbose_name = _('Variation')
        verbose_name_plural = _('Variations')
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    subject = models.CharField(max_length=200, blank=True, verbose_name=_('Subject'))
    review = models.TextField(max_length=400, blank=True, verbose_name=_('Review'))
    rating = models.FloatField(verbose_name=_('Rating'))
    ip = models.CharField(max_length=20, blank=True, verbose_name=_('IP'))
    status = models.BooleanField(default=True, verbose_name=_('Purchased'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
    
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = _('Rewiew rating')
        verbose_name_plural = _('Rewiews rating')
    
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name=_('Product'))
    image = models.ImageField(upload_to='store/products/', max_length=255, verbose_name=_('Image'))
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = _('Products Gallery')
        verbose_name_plural = _('Products Gallery')