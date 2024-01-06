from django.db.models import Q

def filtration_cursor(**kwargs) -> tuple():
        print("Filtration cursor is called!")
        print("Product Title kwargs:", kwargs['product_title'])
        print("variant_id kwargs:", kwargs['variant_id'])
        print("price_from kwargs:", kwargs['price_from'])
        print("price_to kwargs:", kwargs['price_to'])
        print("product_enlisted_after_date kwargs:", kwargs['product_enlisted_after_date'])

        if kwargs['product_title'] != None \
            or kwargs['variant_id'] != None \
            or kwargs['price_from'] != None \
            or kwargs['price_to'] != None \
            or kwargs['product_enlisted_after_date'] != None:
            print("Any of them")

            # Only for product title
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] == None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query only using product title!")
                    return (
                        (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                    )

            # Only for variant
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] != None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query only using variant!")
                    return (
                        ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                          | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                          | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                    )

            # Only for Price Range
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] == None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query only using price_from or price_to range!")
                    # Only for price_from
                    if kwargs['price_from'] != None and kwargs['price_to'] == None:
                        print("Query (Only): price-from")
                        return (
                            (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                        )
                    # Only for price_to
                    if kwargs['price_to'] != None and kwargs['price_from'] == None:
                        print("Query (Only): price-to")
                        return (
                            (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
                    # Both for price_from & price_to
                    if kwargs['price_from'] != None and kwargs['price_to'] != None:
                        print("Query (Both): price-from & price-to")
                        return (
                            (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
            
            # Only for product-enlisted-date-after
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] == None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query only using date!")
                    return (
                        (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                    )
