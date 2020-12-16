from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from single_source_site.models import Category, Product, Order

# Create your views here.
def index (request):

    if not Order.objects.filter(customer_id=request.session.session_key).exists():
        cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    context = {
        'order' : cart
    }
    return render (request, "index.html", context)

def build_quote(request):
    if not Order.objects.filter(customer_id=request.session.session_key).exists():
            cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    context={
        'products':Product.objects.all(),
        'order' : cart
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
        print(request.session.session_key)
        new_order = Order.objects.create(
            customer_id = request.session.session_key,
            customer_name = request.POST['name_txt'],
            email = request.POST['email_txt']
        )
        # print(new_order.customer_name + " email: " + new_order.email + " created a new order.")
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                # Add the product to the newly created order and store the quantity
                # parse the product id out of the name of the 'number' element from the form 
                product_in_order_id = key.replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()
                # print("adding " + product_in_order.quantity_in_order + " of product id " + product_in_order_id + " to order# " + str(new_order.id))
                # add the product to the order 
                new_order.products.add(product_in_order)

        context = {
            'order' : new_order
        }       
        return render(request, "cart.html", context)
    return redirect("/quote_page")

def get_order(request, order_id):
    context = {
        'order' : Order.objects.get(id=order_id)
    }
    return render(request, "cart.html", context)

def get_cart_order(request):
    if not Order.objects.filter(customer_id=request.session.session_key).exists():
            cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    context = {
        'order' : cart
    }
    return context

def delete_order_product(request, order_id, product_id):
    # Get references to the order and product
    update_order = Order.objects.get(id=order_id)
    delete_product = Product.objects.get(id=product_id)
    #Remove the product fromt he order
    update_order.products.remove(delete_product)

    #Update any/all of the products in the order with  quantities from the form
    for key in request.POST:
        if "quantity" in key and int(request.POST[key]) > 0:
            # parse the product id out of the name of the 'number' element from the form 
            product_in_order_id = key.replace("_quantity", "")
            product_in_order = Product.objects.get(id=int(product_in_order_id))
            # value of the 'number' element is the quantity ordered
            # Update the order quantity of this product for the order
            product_in_order.quantity_in_order = request.POST[key]
            product_in_order.save()

    return redirect("/get_order/"+ str(order_id))

def send_quote(request, order_id):
    if request.method == "POST":
        send_order = Order.objects.get(id=order_id)
        # First update the order with any edits the user may have made
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                # parse the product id out of the name of the 'number' element from the form 
                product_in_order_id = key.replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()

        #Build the html string to put into the email
        email_message = render_to_string('email.html',{'order': send_order})
        send_mail(
            'Order# ' + str(send_order.id),
            'Hi ' + send_order.customer_name + ', \nThank-you for your inquiry. Please see your quote below.',
            '',
            [send_order.email, 'ryantmiddleton@gmail.com'],
            fail_silently=False,
            html_message = email_message
        )
    return render (request, "order_success.html", {'order': send_order})

def display_music_videos(request):
    return render(request, "music_videos.html", get_cart_order(request))

def display_narrative(request):
    return render(request, "narrative.html", get_cart_order(request))

def display_commercial(request):
    return render(request, "commercial.html", get_cart_order(request))

def display_3_ton_list(request):
    return render(request, "3_ton.html", get_cart_order(request))

def display_1_ton_list(request):
    return render(request, "1_ton.html", get_cart_order(request))

def display_electric_list(request):
    return render(request, "electric.html", get_cart_order(request))

def display_about(request):
    return render(request, "about.html", get_cart_order(request))

def display_contact(request):
    return render(request, "contact.html", get_cart_order(request))

def display_dolly_list(request):
    return render(request, "dolly.html", get_cart_order(request))



