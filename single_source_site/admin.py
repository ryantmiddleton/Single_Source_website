from django.contrib import admin
from single_source_site.models import Category, Product, Order, Package, PackageItem

class CategoryAdmin(admin.ModelAdmin):
      pass
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
      pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
      pass
admin.site.register(Order, OrderAdmin)

class PackageAdmin(admin.ModelAdmin):
      pass
admin.site.register(Package, PackageAdmin)

class PackageItemAdmin(admin.ModelAdmin):
      pass
admin.site.register(PackageItem, PackageItemAdmin)

# class RentedProductAdmin(admin.ModelAdmin):
#       pass
# admin.site.register(RentedProduct, RentedProductAdmin)

# class AccessoryAdmin(admin.ModelAdmin):
#       pass
# admin.site.register(Accessory, AccessoryAdmin)


