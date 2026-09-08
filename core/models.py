import random

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from urllib.parse import quote



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الفئة")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name="الرابط المختصر")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
     if not self.slug:
        self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1

        while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

     super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])



class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image1 = models.ImageField(upload_to='products/', verbose_name="صورة المنتج")
    image2 = models.ImageField(upload_to='products/', verbose_name="صورة المنتج 2", blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', verbose_name="صورة المنتج 3", blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', verbose_name="صورة المنتج 4", blank=True, null=True)
    size = models.CharField(max_length=100, verbose_name="المقاس", blank=True, null=True)
    description = models.TextField(verbose_name="وصف المنتج")
    code = models.CharField(max_length=100, verbose_name="كود المنتج", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="الفئة", related_name='products')
    inquiry_count = models.IntegerField(default=0, verbose_name="عدد الاستفسارات")
    is_featured = models.BooleanField(default=False, verbose_name="منتج مميز")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    def get_whatsapp_url(self):
        phone = "218947710070"
        
        message = f"السلام عليكم، أريد الاستفسار عن المنتج التالي:\n"
        message += f"المنتج: {self.name}\n"
        if self.code:
            message += f"الكود: {self.code}\n"
        if self.size:
            message += f"المقاس: {self.size}"
        
        encoded_message = quote(message)
        
        return f"https://wa.me/{phone}?text={encoded_message}"    
    @staticmethod
    def generate_code():
        while True:
            code = ''.join(str(random.randint(0, 9)) for _ in range(5))
            if not Product.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
     if not self.code:
        self.code = self.generate_code()

     if not self.slug:
        self.slug = slugify(self.name, allow_unicode=True)

        original_slug = self.slug
        counter = 1

        while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

     super().save(*args, **kwargs) 
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    def increment_inquiry(self):
        self.inquiry_count += 1
        self.save(update_fields=['inquiry_count'])

    def get_sizes_list(self):
        if not self.size:
            return []
        import re
        sizes_text = re.sub(r'[\/\-_]', ',', self.size)
        sizes_list = [s.strip() for s in sizes_text.split(',') if s.strip()]
        return sizes_list

    def get_whatsapp_url(self, size=None):
        base_url = "https://wa.me/218947710070"
        message = f"استفسار عن منتج: {self.name}\n"
        
        if size:
            message += f"المقاس: {size}\n"
                
        
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        return f"{base_url}?text={encoded_message}"


class Handle(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المقبض")
    image = models.ImageField(upload_to='handles/', verbose_name="صورة المقبض")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مقبض"
        verbose_name_plural = "المقابض"
        ordering = ['-created_at']

    def __str__(self):
        return self.name