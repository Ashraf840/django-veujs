from django.db import models
from config.g_model import TimeStampMixin


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.URLField()

    def __str__(self):
        return self.product.title


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.variant.title} --- {self.product.title}'


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    stock = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __repr__(self):
        variant_one_title = self.product_variant_one.variant_title if self.product_variant_one else "N/A"
        variant_two_title = self.product_variant_two.variant_title if self.product_variant_two else "N/A"
        variant_three_title = self.product_variant_three.variant_title if self.product_variant_three else "N/A"

        return f"{variant_one_title} / " \
               f"{variant_two_title} / " \
               f"{variant_three_title}"
        
        
        # return f"{self.product_variant_one} / \
        #     {self.product_variant_two} / \
        #     {self.product_variant_three}"

    def __str__(self):
        return self.__repr__()
        return f'{self.product.title}: ({self.product_variant_one}, {self.product_variant_two}, {self.product_variant_three})'