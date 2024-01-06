from django.views import generic

from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ListProductView(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.all()
        context['products'] = product_list

        # product_variants = ProductVariant.objects.prefetch_related('prices').filter(product=product)

        productVariantPrice = [Product.objects.filter(productvariantprice__product=prod) for prod in product_list]

        for pvp in productVariantPrice:
            print(pvp)
        
        print("###")

        # prod_dict = { id: [prod, ] for id, prod in enumerate(product_list) }
        for prod in product_list:
            print(prod)
        return context
