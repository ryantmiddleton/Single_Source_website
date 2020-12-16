from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('music_videos', views.display_music_videos),
    path('quote_page', views.build_quote),
    path('add_accessories/<int:product_id>', views.get_accessories),
    path('add_to_cart', views.display_cart),
    path('get_order/<int:order_id>', views.get_order),
    path('delete_order_product/<int:order_id>/<int:product_id>', views.delete_order_product),
    path('send_quote/<int:order_id>', views.send_quote),
]