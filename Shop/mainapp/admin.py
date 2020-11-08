from django.contrib import admin
from django.forms import ModelChoiceField
from .models import *

class IPhoneAdmin(admin.ModelAdmin) :

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category' :
            return ModelChoiceField(Category.objects.filter(slug='IPhone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class WatchesAdmin(admin.ModelAdmin) :

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
