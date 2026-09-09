from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product, Category


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse("product_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)


class CategorySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse(
            "products_by_category",
            kwargs={"slug": obj.slug}
        )

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)