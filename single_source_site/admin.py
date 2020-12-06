from django.contrib import admin
from single_source_site.models import Category, Product, Order

class CategoryAdmin(admin.ModelAdmin):
      pass
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
      pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
      pass
admin.site.register(Order, OrderAdmin)

# class RentedProductAdmin(admin.ModelAdmin):
#       pass
# admin.site.register(RentedProduct, RentedProductAdmin)

# class AccessoryAdmin(admin.ModelAdmin):
#       pass
# admin.site.register(Accessory, AccessoryAdmin)


