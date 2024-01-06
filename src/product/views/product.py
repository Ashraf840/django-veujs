from django.views import generic

from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator
from django.shortcuts import render


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
        variants = Variant.objects.filter(active=True)
        context['variants'] = variants

        # print("variants")
        # for var in variants:
        #     print(var)

        page = self.request.GET.get('page', 1)
        items_per_page = 2
        paginator = Paginator(product_list, items_per_page)
        paginated_data = paginator.get_page(page)

        context['paginated_data'] = paginated_data


        # product_variants = ProductVariant.objects.prefetch_related('prices').filter(product=product)

        # productVariantPrice = [Product.objects.filter(productvariantprice__product=prod) for prod in product_list]
        productVariantPrice = [ProductVariantPrice.objects.filter(product=prod) for prod in product_list]


        # for pvp in productVariantPrice:
        #     print(pvp)
        
        # print("###")

        prod_dict = { id: [ prod, 
            # {'product_variant_price': [pvp for pvp in Product.objects.filter(productvariantprice__product=prod)]} 
            # {'product_variant_price': [pvp for pvp in ProductVariantPrice.objects.filter(product=prod)]} 
            [pvp for pvp in ProductVariantPrice.objects.filter(product=prod)]
            ] for id, prod in enumerate(product_list) }
        
        # for key, prod in prod_dict.items():
        #     print(f"Key: {key}, prod: {prod}")
        #     for j in prod[1]:
        #         print('pvp:', j, 'price:', j.price)
        #         # print('pvp:', j)

        # for prod in product_list:
        #     print(prod)
            
        context['prod_dict'] = prod_dict
        return context

    def post(self, request):
        print("This is a post request")
        product_title = request.POST.get('title')
        variant_id = request.POST.get('variant_select')
        price_from = request.POST.get('price_from')
        price_to = request.POST.get('price_to')
        product_enlisted_after_date = request.POST.get('date')

        product_title = product_title if len(product_title) != 0 else None
        price_from = price_from if len(price_from) != 0 else None
        price_to = price_to if len(price_to) != 0 else None
        product_enlisted_after_date = product_enlisted_after_date if len(product_enlisted_after_date) != 0 else None

        # print("Product Title:", product_title)
        # print("variant_id:", variant_id)
        # print("price_from:", price_from)
        # print("price_to:", price_to)
        # print("product_enlisted_after_date:", product_enlisted_after_date)
        
        # print("Product Title (Datatype):", len(product_title))
        return render(request, self.template_name)

