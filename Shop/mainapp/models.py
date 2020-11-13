from django.db import models
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__.meta.model.name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

class MinResolutionErrorException(Exception):
    pass

class MaxResolutionErrorException(Exception):
    pass

class LatestProductsManager:

    @staticmethod
    def getProductsForMainPage(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        return products

class LatestProducts:

    objects = LatestProductsManager()

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product title')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # image = self.image
        # img = Image.open(image)
        # min_height, min_width = self.MIN_RESOLUTION
        # max_height, max_width = self.MAX_RESOLUTION
        # if img.height < min_height or img.width < min_width:
        #     raise MinResolutionErrorException('Image resolution is less than minimum')     // commented side bock imgage bigger than 800x800
        # if img.height > max_height or img.width > max_width:
        #     raise MaxResolutionErrorException('Image resolution is more than maximum')
        # return image
        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_image = new_img.resize((800, 800), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_image.save(filestream, 'JPEG', quality=90)                      ## This code crops image if it is  bigger then 800x800
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )

        super().save(*args, **kwargs)


class Iphone(Product):

    model = models.CharField(max_length=100, verbose_name='IPhone')
    display = models.CharField(max_length=1000, verbose_name='Display')
    processor = models.CharField(max_length=1000, verbose_name='Processor')
    memorySize = models.CharField(max_length=1000, verbose_name='Memory size')
    battery = models.CharField(max_length=1000, verbose_name='Battery')
    weight = models.CharField(max_length=1000, verbose_name='Weight')
    otherInfo = models.CharField(max_length=1000, verbose_name='Other information')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class Watch(Product):

    model = models.CharField(max_length=100, verbose_name='Apple Watch')
    compatibility = models.CharField(max_length=100, verbose_name='Compatibility')
    battery = models.CharField(max_length=1000, verbose_name='Battery')
    moistureResistance = models.CharField(max_length=1000, verbose_name='Moisture resistance')
    otherInfo = models.CharField(max_length=1000, verbose_name='Other information')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class CartProduct(models.Model):

    User = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    objectId = models.PositiveIntegerField()
    contentObject = GenericForeignKey('contentType', 'objectId')
    qty = models.PositiveBigIntegerField(default=1)
    finalPrice = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final price')

    def __str__(self):
        return 'Cart product: {} (for cart)'.format(self.product.title)

class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    totalProducts = models.PositiveIntegerField(default=0)
    finalPrice = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final price')

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    User = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name='Phone number')
    adress = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return 'Customer: {} {}'.format(self.user.firstName, self.user.lastName)