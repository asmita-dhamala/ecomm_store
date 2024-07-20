from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(slider)
admin.site.register(Ad)
admin.site.register(Brand)

@admin.register(product)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "label", "brand", "stock")
    ordering = ("id", "name", "price", "discounted_price")
    list_filter = ("category", "label", "brand", "stock" )

admin.site.register(Feedback)
admin.site.register(ContactInfo)
admin.site.register(Cart)
admin.site.register(productReview)
admin.site.register(Contact)
