from django.contrib import admin
from single_source_site.models import Category, Product, Order, Package, PackageItem, ProductsInOrder, PackagesInOrder

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

class ProductsInOrderAdmin(admin.ModelAdmin):
      pass
admin.site.register(ProductsInOrder, ProductsInOrderAdmin)

class PackagesInOrderAdmin(admin.ModelAdmin):
      pass
admin.site.register(PackagesInOrder, PackagesInOrderAdmin)
