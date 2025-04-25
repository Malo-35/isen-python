from django.views.generic import ListView
from products.models import Product

class HomeView(ListView):
    '''
    Renders home page with all the products, with optional price sorting
    '''
    template_name = 'home.html'
    model = Product
    context_object_name = 'object_list'  # important pour le template

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            return Product.objects.all().order_by('price')
        elif sort == 'price_desc':
            return Product.objects.all().order_by('-price')
        return Product.objects.all()
