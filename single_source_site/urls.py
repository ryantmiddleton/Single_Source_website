from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('quote_page', views.build_quote),
    path('add_accessories/<int:product_id>', views.get_accessories),
    path('add_to_cart', views.display_cart),
    path('send_quote/<int:order_id>', views.send_quote),
]