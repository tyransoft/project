from django.urls import path,include
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticViewSitemap,
    ProductSitemap,
    CategorySitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    path('captin-dashboard/',dashboard, name='dashboard'),

    path('', home, name='home'),
    path('product/(?P<slug>[-\w]+)/$',product_detail, name='product_detail'),
    path('category/(?P<slug>[-\w]+)/$',products_by_category, name='products_by_category'),
    path('increment-inquiry/(?P<slug>[-\w]+)/$',increment_inquiry, name='increment_inquiry'),
    path('about/', about, name='about'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/login/', login_view, name='user_login'),

    
    path('captin-categories/',category_list, name='category_list'),
    path('captin-categories/add/',category_add, name='category_add'),
    path('captin-categories/edit/<int:pk>/',category_edit, name='category_edit'),
    path('captin-categories/delete/<int:pk>/',category_delete, name='category_delete'),
    
    path('captin-products/',product_list, name='product_list'),
    path('captin-products/add/',product_add, name='product_add'),
    path('captin-products/edit/<int:pk>/',product_edit, name='product_edit'),
    path('captin-products/delete/<int:pk>/',product_delete, name='product_delete'),

    path('handles/', handles_public, name='handles'),
    
    path('captin-handles/', handles_admin, name='handles_admin'),
    path('captin-handles/add/', handle_add, name='handles_add'),
    path('captin-handles/<int:pk>/edit/', handle_edit, name='handles_edit'),
    path('captin-handles/<int:pk>/delete/', handle_delete, name='handles_delete'),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django_sitemap",
),
]
