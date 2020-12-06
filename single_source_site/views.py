from django.shortcuts import render, redirect
from single_source_site.models import Category, Product, Order

# Create your views here.
def index (request):
    return render (request, "index.html")

def build_quote(request):
    context={
        'products':Product.objects.filter(category=1)
    }
    return render(request, "quote_builder.html", context)

def get_accessories(request, product_id):
    context={
        'accessories':Product.objects.get(id=product_id).accessories
    }
    return render(request, "accessory_list.html", context)

def display_cart(request):
    if request.method == "POST":
        # Create a new Order
        new_order = Order.objects.create(
            customer_name = request.POST['name_txt'],
            email = request.POST['email_txt']
        )
        print(new_order.customer_name + " email: " + new_order.email + " created a new order.")
        for key in request.POST:
            # print(key)
            # print(request.POST[key])
            # curr_product_id = 0
            #if the key indicates a product, get that product and add it to the order
            # if "product" in key:
            #     sel_product = Product.objects.get(id=request.POST[key])
            #     print("adding " + sel_product.name + " id: " + str(sel_product.id) + " to a new order.")
            #     curr_product_id = sel_product.id
            #     new_order.products.add(sel_product)
            #if the key indicates a quantity and that quantity > 0
            if "quantity" in key and int(request.POST[key]) > 0:
                # Add the product to the newly created order and store the quantity
                # parse the product id out of the name of the 'number' element in the form 
                product_in_order_id = key.replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()
                print("adding " + product_in_order.quantity_in_order + " of product id " + product_in_order_id + " to the order.")
                # add the product to the order
                new_order.products.add(product_in_order)
                # products_in_order = RentedProduct.objects.create(
                #     product=rented_product, 
                #     order=new_order, 
                #     quantity=int(request.POST[key])
                # )

        #return the new_order as a context object 
        context = {
            'order' : new_order
        }       
        return render(request, "cart.html", context)
    return redirect("/quote_page")