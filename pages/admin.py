from django.contrib import admin
from .models import Laptop , Mobile , Accessories

# Register your models here.
    
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    list_editable = ['price']
    search_fields = ['name']

admin.site.register(Laptop,ProductsAdmin)
admin.site.register(Mobile,ProductsAdmin)
admin.site.register(Accessories,ProductsAdmin)

admin.site.site_header = 'Control'
admin.site.site_title = 'MyStore Admin'