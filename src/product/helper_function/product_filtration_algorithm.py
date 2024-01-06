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

            # Input Count: 1
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
            
            # Input Count: 2
            # Query: product-title & variant
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] != None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query with product-title & variant!")
                    return (
                        (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                        & ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                          | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                          | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                    )
            
            # Query: product-title & price
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] == None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query with product-title & (price_from or price_to)!")
                    if kwargs['product_title'] != None and kwargs['price_from'] != None and kwargs['price_to'] == None:
                        print("Make query with product-title & price_from!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['price_from'] == None and kwargs['price_to'] != None:
                        print("Make query with product-title & price_to!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['price_from'] != None and kwargs['price_to'] != None:
                        print("Make query with product-title, price_from & price_to!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
                           
            # Query: product-title & date
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] == None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with product-title & date!")
                    return (
                        (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                        & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                    )

            # Query: variant & price
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] != None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query with variant & (price_from or price_to)!")
                    if kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] == None:
                        print("Make query with variant & price_from!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                        )
                    if kwargs['variant_id'] != None and kwargs['price_from'] == None and kwargs['price_to'] != None:
                        print("Make query with variant & price_to!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
                    if kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] != None:
                        print("Make query with variant, price_from & price_to!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                            | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
            
            # Query: variant & date
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] != None \
                and kwargs['price_from'] == None \
                and kwargs['price_to'] == None \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with variant & date!")
                    return (
                        ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                        | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                        | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                        & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                    )
            
            # Query: price & date
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] == None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with (price_from or price_to) & date!")
                    if kwargs['price_from'] != None and kwargs['price_to'] == None and kwargs['product_enlisted_after_date'] != None:
                        print("Make query with price_from & date!")
                        return (
                            (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['price_from'] == None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Make query with price_to & date!")
                        return (
                            (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['price_from'] != None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Make query with price_from, price_to & date!")
                        return (
                            (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    
            # Input Count: 3
            # Query: product-title, variant & price
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] != None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] == None:
                    print("Make query with product_title, variant & (price_from or price_to)!")
                    if kwargs['product_title'] != None and kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] == None:
                        print("Query: product_title, variant & price_from!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['variant_id'] != None and kwargs['price_from'] == None and kwargs['price_to'] != None:
                        print("Query: product_title, variant & price_to!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] != None:
                        print("Query: product_title, variant, price_from & price_to!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                        )
            
            # Query: product-title, price & date
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] == None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with product_title, (price_from or price_to) & date!")
                    if kwargs['product_title'] != None and kwargs['price_from'] != None and kwargs['price_to'] == None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: product_title, price_from & product_enlisted_after_date!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['price_from'] == None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: product_title, price_to & product_enlisted_after_date!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['product_title'] != None and kwargs['price_from'] != None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: product_title, price_from, price_to & product_enlisted_after_date!")
                        return (
                            (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
            
            # Query: variant, price & date
            if kwargs['product_title'] == None \
                and kwargs['variant_id'] != None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with variant, (price_from or price_to) & date!")
                    if kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] == None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: variant, price_from & product_enlisted_after_date!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['variant_id'] != None and kwargs['price_from'] == None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: variant, price_to & product_enlisted_after_date!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )
                    if kwargs['variant_id'] != None and kwargs['price_from'] != None and kwargs['price_to'] != None and kwargs['product_enlisted_after_date'] != None:
                        print("Query: variant, price_from, price_to & product_enlisted_after_date!")
                        return (
                            ((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                              | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                            & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                            & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                            & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                        )

            # Input Count: 4
            if kwargs['product_title'] != None \
                and kwargs['variant_id'] != None \
                and (kwargs['price_from'] != None \
                or kwargs['price_to'] != None) \
                and kwargs['product_enlisted_after_date'] != None:
                    print("Make query with all the inputs product_title, variant, (price_from or price_to) & date!")
                    if kwargs['product_title'] != None \
                        and kwargs['variant_id'] != None \
                        and kwargs['price_from'] != None \
                        and kwargs['price_to'] == None \
                        and kwargs['product_enlisted_after_date'] != None:
                            print("Query: product_title, variant, price_from & product_enlisted_after_date!")
                            return (
                                (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                                &((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                                & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                                & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                            )
                    if kwargs['product_title'] != None \
                        and kwargs['variant_id'] != None \
                        and kwargs['price_from'] == None \
                        and kwargs['price_to'] != None \
                        and kwargs['product_enlisted_after_date'] != None:
                            print("Query: product_title, variant, price_to & product_enlisted_after_date!")
                            return (
                                (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                                &((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                                & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                                & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                            )
                    if kwargs['product_title'] != None \
                        and kwargs['variant_id'] != None \
                        and kwargs['price_from'] != None \
                        and kwargs['price_to'] != None \
                        and kwargs['product_enlisted_after_date'] != None:
                            print("Query: product_title, variant, price_from, price_to & product_enlisted_after_date!")
                            return (
                                (Q(productvariantprice__product__title__icontains=kwargs['product_title']) if kwargs['product_title'] else Q())
                                &((Q(productvariantprice__product_variant_one__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_two__variant__pk=kwargs['variant_id']) 
                                    | Q(productvariantprice__product_variant_three__variant__pk=kwargs['variant_id'])) if kwargs['variant_id'] else Q())
                                & (Q(productvariantprice__price__gte=kwargs['price_from']) if kwargs['price_from'] else Q())
                                & (Q(productvariantprice__price__lte=kwargs['price_to']) if kwargs['price_to'] else Q())
                                & (Q(productvariantprice__product__created_at__gte=kwargs['product_enlisted_after_date']) if kwargs['product_enlisted_after_date'] else Q())
                            )
                            

                        
            