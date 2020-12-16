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
    num_inventory = models.IntegerField(default=0)
    quantity_in_order = models.IntegerField(default=0);
    description = models.TextField(blank=True)
    #orders - a list of the orders that this product belongs to
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

    def __str__(self): 
         return self.name

    def get_total(self):
        return self.price * self.quantity_in_order



class OrderManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name_txt']) == 0:
             errors["name_txt"] = "The author must have at least 3 characters."
        if not EMAIL_REGEX.match(postData['email_txt']):
            errors['email'] = ("Invalid email address!")
        return errors  
    
class Order(models.Model):
    customer_id = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()
    
    def __str__(self): 
        return "Order# " + str(self.id) + " for " + self.email
        
    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.price * product.quantity_in_order
        return total

# class RentedProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete = models.CASCADE)
#     order = models.ForeignKey(Order, on_delete = models.CASCADE)
#     quantity = models.IntegerField(null=True)
    
#     def __str__(self): 
#         return "Order# " + str(self.order.id) + ": " + self.product.name + " (" + str(self.quantity) + ") for " + self.order.email 
