from django.views import generic

from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from product.helper_function.product_filtration_algorithm import filtration_cursor
from django.db.models import Q  # Required for testing in this file
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import json


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    def createProductVariantPrice(self, request, product, pv_one=None, pv_two=None, pv_three=None, price=0, stock=0, **kwargs):
        print("Create product!")
        print("product:", product)
        print("pv_one:", pv_one, "; type:", type(pv_one))
        print("pv_two:", pv_two, "; type:", type(pv_two))
        print("pv_three:", pv_three, "; type:", type(pv_three))
        print("price:", price)
        print("stock:", stock)

        ProductVariantPrice.objects.create(
            product_variant_one=pv_one,
            product_variant_two=pv_two,
            product_variant_three=pv_three,
            price=price,
            stock=stock,
            product=product,
        )
        self.context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        self.context['product'] = True
        self.context['variants'] = list(variants.all())
        return render(request, self.template_name, context=self.context)
        pass

    def post(self, request):
        print("Created post request!")
        received_json_data = request.body.decode('utf-8')
        received_json_data = json.loads(received_json_data)
        # return JsonResponse({'msg': 'Created post request!'})

        product_title = received_json_data.get('title')
        sku = received_json_data.get('sku')
        description = received_json_data.get('description')

        # Prohibit from leaving the product-name & sku empty before creating product record in db
        if len(product_title) and len(sku):
            # Create product instance
            product = Product.objects.create(
                title=product_title,
                sku=sku,
                description=description
            )
        else:
            return JsonResponse({'msg': 'Please provide a product-title & sku!'})

        product_image = received_json_data.get('product_image')     # not working on uploading image
        
        # # Create product variant instances
        product_variant = received_json_data.get('product_variant')
        print("product_variant:", product_variant)
        # Check if the prodcut contains the new-record-queryset before creating it's variant
        if product:
            print("Product queryset is not empty.")
            for prod_var in product_variant:
                # print(prod_var.get('option'), prod_var.get('tags'), ":", end=" ")
                variant = Variant.objects.get(id=prod_var.get('option'))
                if len(prod_var.get('tags')):
                    # print("Iterate tags!")
                    # print(Variant.objects.get(id=prod_var.get('option')))
                    
                    ProductVariant.objects.create(
                        variant_title=' -- '.join(tag for tag in prod_var.get('tags')),
                        # variant_title=[tag for tag in prod_var.get('tags')],
                        variant=variant,
                        product=product,
                    )
                    # for tag in prod_var.get('tags'):
                    #     # print(tag)
        else:
            print("Product queryset is empty or None.")
            return JsonResponse({'msg': 'Product record is not created in the db!'})
        
        product_variant_prices = received_json_data.get('product_variant_prices')
        # Create product variant price instance
        prodcut_variants = ProductVariant.objects.filter(product=product)
        print("prodcut_variants:", prodcut_variants)

        if len(prodcut_variants) == 3:
            # print("3 Product variant instances!", product_variant[0], product_variant[1], product_variant[2])
            self.createProductVariantPrice(
                request,
                product=product, 
                pv_one=prodcut_variants[0],
                pv_two=prodcut_variants[1],
                pv_three=prodcut_variants[2],
                price=product_variant_prices[0].get('price'),
                stock=product_variant_prices[0].get('stock'),
            )
        if len(prodcut_variants) == 2:
            # print("2 Product variant instances!", prodcut_variants[0], prodcut_variants[1])
            # print("type:", type(prodcut_variants[0]))
            self.createProductVariantPrice(
                request,
                product=product, 
                pv_one=prodcut_variants[0],
                pv_two=prodcut_variants[1],
                price=product_variant_prices[0].get('price'),
                stock=product_variant_prices[0].get('stock'),
            )
        if len(prodcut_variants) == 1:
            # print("1 Product variant instances!", prodcut_variants[0])
            self.createProductVariantPrice(
                request,
                product=product, 
                pv_one=prodcut_variants[0],
                price=product_variant_prices[0].get('price'),
                stock=product_variant_prices[0].get('stock'),
            )
        
        

        

        # print("Product Title:", received_json_data)

        return JsonResponse({'msg': 'Created post request!'})
        return redirect(reverse('product:list.product'))

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

            # # Any single query value  [Original Query Build Algorithm]
            # filtration_query = (
            #     (Q(productvariantprice__product__title__icontains=product_title) if product_title else Q())
            #     | ((Q(productvariantprice__product_variant_one__variant__pk=variant_id) | Q(productvariantprice__product_variant_two__variant__pk=variant_id) | Q(productvariantprice__product_variant_three__variant__pk=variant_id)) if variant_id else Q())
            #     | (Q(productvariantprice__price__gte=price_from) if price_from else Q())
            #     | (Q(productvariantprice__price__lte=price_to) if price_to else Q())
            #     | (Q(productvariantprice__product__created_at__gte=product_enlisted_after_date) if product_enlisted_after_date else Q())
            # )

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

            product_list = []

            for fp in filtered_products:
                if fp not in product_list:
                    product_list.append(fp)
                    # print(fp)
            
            # print("product_list:", product_list)
            page = self.request.GET.get('page', 1)
            items_per_page = 2
            paginator = Paginator(product_list, items_per_page)
            paginated_data = paginator.get_page(page)

            
            prod_dict = { id: [ prod, 
            [pvp for pvp in ProductVariantPrice.objects.filter(product=prod)]
            ] for id, prod in enumerate(product_list) }
        
            # print("Product Title (Datatype):", len(product_title))
            context = super().get_context_data(**kwargs)
            variants = Variant.objects.filter(active=True)
            context['variants'] = variants
            context['prod_dict'] = prod_dict
            context['paginated_data'] = paginated_data
            return render(request, self.template_name, context=context)

    
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class EditProductView(generic.TemplateView):
    template_name = 'products/edit.html'

    def get_context_data(self, id, **kwargs):
        context = super(EditProductView, self).get_context_data(**kwargs)
        product = Product.objects.get(id=id)
        # variants = Variant.objects.filter(active=True).values('id', 'title')
        productVariantPrice = ProductVariantPrice.objects.filter(product=product)
        context['product'] = product
        # context['variants'] = list(variants.all())
        print("product id:", id)
        print("productVariantPrice:", productVariantPrice)
        context['variants'] = productVariantPrice
        return context
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        print("Post request to edit the product information & then redirect the user to product list page")
        print("product id (edit):", id)
        # print("product title (edit):", request.POST.get("product_name"))
        # print("product sku (edit):", request.POST.get("product_sku"))
        # print("product description (edit):", request.POST.get("description")[:100])
        title = request.POST.get("product_name")
        sku = request.POST.get("product_sku")
        description = request.POST.get("description")
        product = Product.objects.get(id=id)
        product.title = title
        product.sku = sku
        product.description = description
        product.save()

        productVariantPriceList = request.POST.getlist('productVariantPrice')
        productVariantPriceIDList = request.POST.getlist('productVariantPriceID')
        productVariantStockList = request.POST.getlist('productVariantStock')

        print("product variant prices IDs (edit):", productVariantPriceIDList)
        print("product variant prices (edit):", productVariantPriceList)
        print("product variant stocks (edit):", productVariantStockList)

        productVariantPriceZip = list(zip(
            productVariantPriceIDList, 
            productVariantPriceList, 
            productVariantStockList
        ))

        # print("productVariantPriceZip:", productVariantPriceZip)
        print("productVariantPriceZip")
        for pvpz in productVariantPriceZip:
            pvp = ProductVariantPrice.objects.get(id=int(pvpz[0]))
            pvp.price = float(pvpz[1])
            pvp.stock = float(pvpz[2])
            pvp.save()
            # print(pvpz)

        
        return redirect('product:list.product')
