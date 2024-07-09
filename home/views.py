from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products':products, 'categories':categories})


class ProductDetailView(View):
    template_name = 'home/product_detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm
        return render(request, self.template_name, {'product':product, 'form':form})