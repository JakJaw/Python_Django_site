from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    category_name = models.CharField(max_length=15, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    describtion = models.TextField(max_length=255, blank=True, verbose_name=_('Describtion'))
    
    #Possible extension for user click on category image in shop
    #category_image = models.ImageField(upload_to='photos/categories/', blank=True, verbose_name=_('Category Image'))
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name