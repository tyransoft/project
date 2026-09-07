from django import forms
from .models import *
from django.utils import timezone

WIDGET_ATTRS = {
    'class': 'form-control',
    'placeholder': 'أدخل النص هنا'
}

SELECT_ATTRS = {
    'class': 'form-select'
}

DATE_ATTRS = {
    'class': 'form-control',
    'type': 'date'
      
}

class LoginForm(forms.Form):
    username = forms.CharField(
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المستخدم', 'autofocus': True})
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'أدخل كلمة المرور'})
    )



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'اسم الفئة'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'code', 'size', 'description', 'image1', 'image2', 'image3', 'image4', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'اسم المنتج'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'code': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'كود المنتج'}),
            'size': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'المقاس'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 5, 'placeholder': 'وصف المنتج'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4'}),
        }    