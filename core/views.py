from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from .models import Category, Product
from .forms import *
from django.urls import reverse
from django.core.paginator import Paginator





def home(request):
    categories = Category.objects.all().order_by('created_at')
    products = Product.objects.all().order_by('-is_featured')
    
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'home.html', context)



def login_view(request):
    if request.user.is_authenticated:
        return redirect('statistics')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user :
                login(request, user)
                return redirect('home')
  
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def about(request):
    categories = Category.objects.all().order_by('created_at')
    
    
    context = {
        'categories': categories,
    }


    return render(request, 'about.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, 
    ).exclude(id=product.id)[:4]
    
    suggested_handles = Handle.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.all().order_by('created_at')
    
    
    context = {
        'categories': categories,   
   
        'product': product,
        'related_products': related_products,
        'suggested_handles': suggested_handles,
    }
    return render(request, 'product_detail.html', context)


def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all().order_by('created_at')
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products_by_category.html', context)


@csrf_exempt
def increment_inquiry(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        product.inquiry_count += 1
        product.save(update_fields=['inquiry_count'])
        return JsonResponse({
            'success': True,
            'inquiry_count': product.inquiry_count
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@staff_member_required
def dashboard(request):
    total_categories = Category.objects.count()
    total_products = Product.objects.count()
    
    top_inquired_products = Product.objects.order_by('-inquiry_count')[:5]
    
    categories_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_inquiries=Sum('products__inquiry_count')
    ).order_by('-product_count')
    
    
    context = {
        'total_categories': total_categories,
        'total_products': total_products,
        'top_inquired_products': top_inquired_products,
        'categories_stats': categories_stats,
    }
    return render(request, 'dashboard.html', context)


@staff_member_required
def category_list(request):
    categories = Category.objects.all().annotate(
        product_count=Count('products')
    ).order_by('name')
    return render(request, 'category_list.html', {'categories': categories})


@staff_member_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الفئة بنجاح')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'title': 'إضافة فئة جديدة'})


@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الفئة بنجاح')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'title': 'تعديل الفئة'})


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        product_count = category.products.count()
        if product_count > 0:
            messages.error(request, f'لا يمكن حذف الفئة لأنها تحتوي على {product_count} منتج')
            return redirect('category_list')
        category.delete()
        messages.success(request, 'تم حذف الفئة بنجاح')
        return redirect('category_list')
    return render(request, 'category_delete.html', {'category': category})


@staff_member_required
def product_list(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    return render(request, 'product_list.html', {'products': products})


@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'تم إضافة المنتج بنجاح')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'title': 'إضافة منتج جديد'})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المنتج بنجاح')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'title': 'تعديل المنتج'})


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح')
        return redirect('product_list')
    return render(request, 'product_delete.html', {'product': product})



def handles_public(request):
    handles = Handle.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        handles = handles.filter(name__icontains=search_query)
    
    paginator = Paginator(handles, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'handles': page_obj,
        'search_query': search_query,
        'total_count': Handle.objects.count(),
    }
    return render(request, 'handles.html', context)



@staff_member_required
def handles_admin(request):
    handles = Handle.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        handles = handles.filter(name__icontains=search_query)
    
    paginator = Paginator(handles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'handles': page_obj,
        'search_query': search_query,
        'total_count': Handle.objects.count(),
    }
    return render(request, 'handle_list.html', context)


@staff_member_required
def handle_add(request):
    if request.method == 'POST':
        form = HandleForm(request.POST, request.FILES)
        if form.is_valid():
            handle = form.save()
            messages.success(request, f'تم إضافة المقبض "{handle.name}" بنجاح!')
            return redirect('handles_admin')
        else:
            messages.error(request, 'حدث خطأ في إضافة المقبض. يرجى التحقق من البيانات.')
    else:
        form = HandleForm()
    
    context = {
        'form': form,
        'title': 'إضافة مقبض جديد',
    }
    return render(request, 'handle_form.html', context)


@staff_member_required
def handle_edit(request, pk):
    handle = get_object_or_404(Handle, pk=pk)
    
    if request.method == 'POST':
        form = HandleForm(request.POST, request.FILES, instance=handle)
        if form.is_valid():
            form.save()
            messages.success(request, f'تم تحديث المقبض "{handle.name}" بنجاح!')
            return redirect('handles_admin')
        else:
            messages.error(request, 'حدث خطأ في تحديث المقبض. يرجى التحقق من البيانات.')
    else:
        form = HandleForm(instance=handle)
    
    context = {
        'form': form,
        'handle': handle,
        'title': f'تعديل: {handle.name}',
    }
    return render(request, 'handle_form.html', context)


@staff_member_required
def handle_delete(request, pk):
    handle = get_object_or_404(Handle, pk=pk)
    
    if request.method == 'POST':
        handle_name = handle.name
        handle.delete()
        messages.success(request, f'تم حذف المقبض "{handle_name}" بنجاح!')
        return redirect('handles_admin')
    
    context = {
        'handle': handle,
        'title': f'حذف: {handle.name}',
    }
    return render(request, 'handle_confirm_delete.html', context)

