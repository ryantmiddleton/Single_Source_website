from django.db import models

class Category (models.Model):
    name = models.CharField(max_length=255)
    #products - a list of products that belong to this category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
         return self.name

# class Accessory (models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     num_inventory = models.IntegerField()
#     description = models.TextField()
#     #products - a list of products that this Accessory belongs to
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self): 
    #      return self.name

class ProductManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        # if len(postData['name']) < 3:
        #      errors["author_txt"] = "The author must have at least 3 characters."
        # if len(postData['content_txt']) < 10:
        #      errors["content_txt"] = "The quote must have at least 10 characters."
        return errors



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, related_name="products", on_delete = models.CASCADE)
    accessories = models.ManyToManyField('self', blank=True)
    num_inventory = models.IntegerField()
    quantity_in_order = models.IntegerField(default=0);
    description = models.TextField()
    #orders - a list of the orders that this product belongs to
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

    def __str__(self): 
         return self.name
         
class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    products = models.ForeignKey(Product, related_name="orders", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return "Order# " + str(self.id) + " for " + self.email

# class RentedProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     order = models.ForeignKey(Order, on_delete = models.CASCADE)
#     quantity = models.IntegerField(null=True)
    
#     def __str__(self): 
#         return "Order# " + str(self.order.id) + ": " + self.product.name + " (" + str(self.quantity) + ") for " + self.order.email 
