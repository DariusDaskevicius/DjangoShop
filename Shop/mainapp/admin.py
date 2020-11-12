from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from .models import *
from PIL import Image

class IPhoneAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Add images only with low graphics {}x{}'.format(*self.MIN_RESOLUTION)

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Image resolution is less than minimum')
        return image

class IPhoneAdmin(admin.ModelAdmin):

    form = IPhoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category' :
            return ModelChoiceField(Category.objects.filter(slug='IPhone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class WatchesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category' :
            return ModelChoiceField(Category.objects.filter(slug='watches'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Iphone, IPhoneAdmin)
admin.site.register(Watch, WatchesAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
