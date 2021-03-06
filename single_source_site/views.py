import os
import Ryan_Middleton_Solo_Project.settings as settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from random import randint
from django.template.loader import render_to_string
from single_source_site.models import Category, Product, Order, Package, PackageItem, ProductsInOrder, PackagesInOrder

# Create your views here.
def index (request):
    # Get all images from img/set_photos
    photos = []
    photo_path = os.path.abspath(os.path.join(settings.STATICFILES_DIRS[0], 'img/set_photos'))
    for file in os.listdir(photo_path):
        photos.append(file)

    if not Order.objects.filter(customer_id=request.session.session_key).exists():
        cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    context = {
        'order' : cart,
        'photos': photos
    }
    return render (request, "index.html", context)

def build_quote(request):
    if not Order.objects.filter(customer_id=request.session.session_key).exists():
            cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    context={
        'grip_packages': Category.objects.get(name="Grip").packages.all().order_by('name'),
        'dolly_products': Category.objects.get(name="Dolly").products.all(),
        'hmi_products': Category.objects.get(name="HMI").products.all().order_by('name'),
        'tungsten_products': Category.objects.get(name="Tungsten").products.all().order_by('name'),
        'led_products': Category.objects.get(name="LED").products.all().order_by('name'),
        'distro_products': Category.objects.get(name="Distribution").products.all().order_by('name'),
        'acc_products': Category.objects.get(name="Accessories").products.all().order_by('name'),
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
        # print("My session ID: " + str(request.session.session_key))
        new_order = Order.objects.create(
            customer_id = request.session.session_key,
            customer_name = request.POST['name_txt'],
            email = request.POST['email_txt']
        )
        # print(new_order.customer_name + " email: " + new_order.email + " created a new order.")
        # Send verification 
        request.session["veri_code"] = randint(100000, 999999)
        print(request.session["veri_code"])
        context = {
            'order':new_order,
            'veri_code': request.session["veri_code"]
        }
        email_message = render_to_string('email_verification.html', context)
        send_mail(
            subject='Verify Email Address',
            message= 'Hi ' + new_order.customer_name + ', \nYour verifiaction code is ' + str(request.session["veri_code"]) + 'If you believe you have received this email in error, please contact SingleSourceGripAndLighting@gmail.com.',
            from_email='SingleSource@singlesourcelight.com',
            recipient_list=[new_order.email],
            fail_silently=False,
            html_message = email_message
        )
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                # Add the product to the newly created order and store the quantity
                # parse the product/package id out of the name of the 'number' element from the form 
                if "product" in key:
                    product_in_order_id = key.replace("product_", "").replace("_quantity", "")
                    product_in_order = Product.objects.get(id=int(product_in_order_id))
                    # print("adding " + product_in_order.quantity_in_order + " of product id " + product_in_order_id + " to order# " + str(new_order.id))
                    # add the product and quantity to the order
                    new_product_in_order = ProductsInOrder.objects.create(
                        order = new_order,
                        product = product_in_order,
                        quantity = request.POST[key]
                    )
                elif "package" in key:
                    package_in_order_id = key.replace("package_", "").replace("_quantity", "")
                    package_in_order = Package.objects.get(id=int(package_in_order_id))
                    # print("adding " + package_in_order.quantity_in_order + " of package id " + package_in_order_id + " to order# " + str(new_order.id))
                    # add the product and quantity to the order
                    new_package_in_order = PackagesInOrder.objects.create(
                        order = new_order,
                        package = package_in_order,
                        quantity = request.POST[key]
                    )
        context = {
            'order' : new_order,
            'order_packages': PackagesInOrder.objects.filter(order__id=new_order.id).order_by('package__name'),
            'order_products': ProductsInOrder.objects.filter(order__id=new_order.id).order_by('product__name'),
            'veri_code': request.session["veri_code"]
        }       
        return render(request, "cart.html", context)
    return redirect("/quote_page")

def get_order(request, order_id):
    context = {
            'order' : Order.objects.get(id=order_id),
            'order_packages': PackagesInOrder.objects.filter(order__id=order_id),
            'order_products': ProductsInOrder.objects.filter(order__id=order_id),
            'veri_code': request.session["veri_code"]
    }  
    return render(request, "cart.html", context)

def get_cart_order(request):
    if not Order.objects.filter(customer_id=request.session.session_key).exists():
            cart = None
    else:
        cart = Order.objects.filter(customer_id=request.session.session_key).last()
    return cart

def delete_order_item(request, order_id, item_id):
    # Get references to the order and product
    update_order = Order.objects.get(id=order_id)
    if "product" in item_id:
        item_id = item_id.replace("product_", "")
        delete_item = Product.objects.get(id=item_id)
        #Remove the product fromt he order
        update_order.products.remove(delete_item)
    elif "package" in item_id:
        item_id = item_id.replace("package_", "")
        delete_item = Package.objects.get(id=item_id)
        #Remove the product fromt he order
        update_order.packages.remove(delete_item)

    #Update any/all of the products in the order with  quantities from the form
    for key in request.POST:
        if "quantity" in key and int(request.POST[key]) > 0:
            if "product" in key:
                # parse the product id out of the name of the 'number' element from the form 
                product_in_order_id = key.replace("product_", "").replace("_quantity", "")
                product_in_order = Product.objects.get(id=int(product_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this product for the order
                product_in_order.quantity_in_order = request.POST[key]
                product_in_order.save()
            elif "package" in key:
                # parse the package id out of the name of the 'number' element from the form 
                package_in_order_id = key.replace("package_", "").replace("_quantity", "")
                package_in_order = Package.objects.get(id=int(package_in_order_id))
                # value of the 'number' element is the quantity ordered
                # Update the order quantity of this package for the order
                package_in_order.quantity_in_order = request.POST[key]
                package_in_order.save()

    return redirect("/get_order/"+ str(order_id))

def send_quote(request, order_id):
    if request.method == "POST":
        send_order = Order.objects.get(id=order_id)
        # First update the order with any edits the user may have made
        for key in request.POST:
            if "quantity" in key and int(request.POST[key]) > 0:
                if "product" in key:
                    # parse the product id out of the name of the 'number' element from the form 
                    product_in_order_id = key.replace("product_", "").replace("_quantity", "")
                    product_in_order = ProductsInOrder.objects.get(order__id=send_order.id, product__id=int(product_in_order_id))
                    # value of the 'number' element is the quantity ordered
                    # Update the order quantity of this product for the order
                    product_in_order.quantity = request.POST[key]
                    product_in_order.save()
                elif "package" in key:
                    # parse the package id out of the name of the 'number' element from the form 
                    package_in_order_id = key.replace("package_", "").replace("_quantity", "")
                    package_in_order = PackagesInOrder.objects.get(order__id=send_order.id, package__id=int(package_in_order_id))
                    # value of the 'number' element is the quantity ordered
                    # Update the order quantity of this package for the order
                    package_in_order.quantity = request.POST[key]
                    package_in_order.save()

        context = {
            'order' : send_order,
            'order_packages': PackagesInOrder.objects.filter(order__id=send_order.id),
            'order_products': ProductsInOrder.objects.filter(order__id=send_order.id),
            'veri_code': request.POST["veri_code_hdn"]
        }
        #Check if email is blacklisted
        for customer in settings.BLACKLIST:
            if customer["email"] == send_order.email:
                #Send an email to the blacklisted party
                #Build the html string to put into the email
                email_message = render_to_string('email_blacklist.html', context)
                send_mail(
                    subject='Unauthorized Request',
                    message='Sorry ' + send_order.customer_name + 
                    ", \nWe are unable to send you a quote at this time. Try back later.\nIf you believe this email has been incorrectly sent to you, please contact rtmiddleton7@gmail.com.",
                    from_email='SingleSource@singlesourcelight.com',
                    recipient_list=[send_order.email],
                    fail_silently=False,
                    html_message = email_message
                )
                email_message = render_to_string('email_blacklist_owner.html', context)
                send_mail(
                    subject='Attempted Quote Request from ' + send_order.customer_name,
                    message='Dude,\n' + send_order.customer_name + ": " + send_order.email + "\nTried to price check you. I say we go get the mutha fuckas.",
                    from_email='SingleSource@singlesourcelight.com',
                    recipient_list=['ryantmiddleton@gmail.com'],
                    fail_silently=False,
                    html_message = email_message
                )
                return render (request, "order_success.html", {'order':get_cart_order(request)})
        # Check if user has verified their email address
        if request.POST["veri_code_input"] != request.POST["veri_code_hdn"]:
            return render(request, "cart.html", context)

        #Send an email to the customer
        #Build the html string to put into the email
        email_message = render_to_string('email_cust.html', context)
        send_mail(
            subject='Single Source Order# ' + str(send_order.id),
            message='',
            from_email='SingleSource@singlesourcelight.com',
            recipient_list=[send_order.email],
            fail_silently=False,
            html_message = email_message
        )
        #Send the email to the owner
        #Build the html string to put into the email
        email_message = render_to_string('email_owner.html', context)
        send_mail(
            subject='Single Source Order# ' + str(send_order.id),
            message='',
            from_email='SingleSourceOrders@singlesourcelight.com',
            recipient_list=['ryantmiddleton@gmail.com'],
            fail_silently=False,
            html_message = email_message
        )
        # print("Order Sent to " + send_order.email)
        # request.session.flush()
        if settings.DEBUG == True:
            return render (request, "order_summary.html", context)
        else:
            return render (request, "order_success.html", context)
    else:
        return redirect ("/quote_page/")

def display_music_videos(request):
    return render(request, "music_videos.html", {'order':get_cart_order(request)})

def display_narrative(request):
    return render(request, "narrative.html", {'order':get_cart_order(request)})

def display_commercial(request):
    return render(request, "commercial.html", {'order':get_cart_order(request)})

def display_3_ton_list(request):
    context = {
        'order' : get_cart_order(request),
        'package': PackageItem.objects.filter(package__id=1).order_by('product__name')
    }

    return render(request, "3_ton.html", context)

def display_1_ton_list(request):
    context = {
        'order' : get_cart_order(request),
        'package': PackageItem.objects.filter(package__id=2).order_by('product__name')
    }
    return render(request, "1_ton.html", context)

def display_electric_list(request):
    context = {
        'order' : get_cart_order(request),
        'hmi_products': Category.objects.get(name="HMI").products.all().order_by('name'),
        'tungsten_products': Category.objects.get(name="Tungsten").products.all().order_by('name'),
        'led_products': Category.objects.get(name="LED").products.all().order_by('name'),
        'distro_products': Category.objects.get(name="Distribution").products.all().order_by('name'),
        'acc_products': Category.objects.get(name="Accessories").products.all().order_by('name')

    }
    return render(request, "electric.html", context)

def display_about(request):
    return render(request, "about.html", {'order':get_cart_order(request)})

def display_contact(request):
    return render(request, "contact.html", {'order':get_cart_order(request)})

def display_dolly_list(request):
    context = {
        'order' : get_cart_order(request),
        'dolly_products': Category.objects.get(name="Dolly").products.all()
    }
    return render(request, "dolly.html", context)

def contact_me(request):
    if request.method == "POST":
        send_mail(
            subject=request.POST["cust_subject"],
            message=request.POST["cust_name"] + ": " + request.POST["cust_email"] + "\nSent you the following message:\n" + request.POST["cust_msg"],
            from_email=request.POST["cust_email"],
            recipient_list=['ryantmiddleton@gmail.com'],
            fail_silently=False,
        )
        return render(request, "contact_success.html", {'order':get_cart_order(request)})
    else:
        return redirect ("/contact")

def get_sitemap(request):
    return render(request, "sitemap.txt")