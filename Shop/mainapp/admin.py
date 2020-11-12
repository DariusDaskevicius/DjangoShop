from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from .models import *
from PIL import Image
from django.utils.safestring import mark_safe

class IPhoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">Add an image at least {}x{}</span>'.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Image size should not exceed 3MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Image resolution is less than minimum')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Image resolution is more than maximum')
        return image

class IPhoneAdmin(admin.ModelAdmin):

    form = IPhoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='iphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class WatchesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='watch'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Iphone, IPhoneAdmin)
admin.site.register(Watch, WatchesAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
