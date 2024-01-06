from django.views import generic

from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from product.helper_function.product_filtration_algorithm import filtration_cursor
from django.db.models import Q  # Required for testing in this file


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
        # productVariantPrice = [ProductVariantPrice.objects.filter(product=prod) for prod in product_list]


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

    def post(self, request, **kwargs):
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

        if product_title == None and \
            variant_id == None and \
            price_from == None and \
            price_to == None and \
            product_enlisted_after_date == None:
            # print("SHow entire product list!")
            return redirect(reverse('product:list.product'))
        else:
            print("Make filtration!")
            # variant = Variant.objects.get(id=variant_id)
            # print("Variant:", variant.title)

            filtration_query = filtration_cursor(
                product_title=product_title,
                variant_id=variant_id,
                price_from=price_from,
                price_to=price_to,
                product_enlisted_after_date=product_enlisted_after_date
            )

            print("filtration query:", filtration_query)

            # Any single query value  [Original Query Build Algorithm]
            filtration_query = (
                (Q(productvariantprice__product__title__icontains=product_title) if product_title else Q())
                | ((Q(productvariantprice__product_variant_one__variant__pk=variant_id) | Q(productvariantprice__product_variant_two__variant__pk=variant_id) | Q(productvariantprice__product_variant_three__variant__pk=variant_id)) if variant_id else Q())
                | (Q(productvariantprice__price__gte=price_from) if price_from else Q())
                | (Q(productvariantprice__price__lte=price_to) if price_to else Q())
                | (Q(productvariantprice__product__created_at__gte=product_enlisted_after_date) if product_enlisted_after_date else Q())
            )

            filtered_products = Product.objects.filter(filtration_query)

            # # Deprecated ################################
            # filtration_query = (
            #     Q(productvariantprice__product__title__icontains=product_title) 
            #     | Q(productvariantprice__product_variant_two__variant__title=variant.title)
            #     # | (Q(productvariant__variant__id=variant_id) & Q(name__icontains=keyword))
            # )

            # filtered_products = ProductVariantPrice.objects.filter(filtration_query)
            # # ###########################################

            print("Query-result-length:", len(filtered_products))

            for fp in filtered_products:
                print(fp)
        
        # print("Product Title (Datatype):", len(product_title))
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True)
        context['variants'] = variants
        return render(request, self.template_name, context=context)

    


